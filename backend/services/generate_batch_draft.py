import os
import glob
import shutil
import json
import time
from typing import List, Optional
from domain.pyJianYingDraft import Script_file, Video_material, Audio_material, Video_segment, Audio_segment, trange, Clip_settings, Crop_settings
from domain.pyJianYingDraft import Track_type
from domain.pyJianYingDraft.text_segment import TextStyleRange, Text_style, Text_border
from services.create_draft import get_or_create_draft
from .add_text_impl import add_text_impl
from .add_effect_impl import add_effect_impl
from services.template_service import template_service
from infra.cache_service import draft_cache
from infra.util import hex_to_rgb
from config import settings
from infra.logger import logger

def generate_draft_from_local_materials(
    video_dir: str,
    audio_dir: str,
    draft_folder: str,
    image_dir: Optional[str] = None,
    draft_name: Optional[str] = None,
    image_crop_settings: Optional[dict] = None,
    template_id: Optional[str] = None
):
    """
    Generate a draft from local video and audio directories.
    If image_dir is provided and audio is longer than video, images will fill the gap.
    """
    logger.info(f"Starting batch draft generation. Video dir: {video_dir}, Audio dir: {audio_dir}, Image dir: {image_dir}, Draft folder: {draft_folder}")
    # 1. Create a new draft in memory
    draft_id, script = get_or_create_draft()
    
    # 2. Scan directories
    video_extensions = ['*.mp4', '*.mov', '*.avi', '*.mkv']
    audio_extensions = ['*.mp3', '*.wav', '*.aac', '*.m4a']
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.webp']
    
    video_files = []
    if os.path.exists(video_dir):
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(video_dir, ext)))
    
    audio_files = []
    if os.path.exists(audio_dir):
        for ext in audio_extensions:
            audio_files.extend(glob.glob(os.path.join(audio_dir, ext)))
            
    image_files = []
    if image_dir and os.path.exists(image_dir):
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(image_dir, ext)))
        
    video_files.sort()
    audio_files.sort()
    image_files.sort()
    logger.info(f"Found {len(video_files)} video files, {len(audio_files)} audio files, and {len(image_files)} image files.")
    
    # 3. Pre-process materials to calculate durations
    video_materials = []
    total_video_duration = 0
    
    for v_path in video_files:
        try:
            v_path = os.path.abspath(v_path)
            logger.info(f"Processing video file: {v_path}")
            material = Video_material(
                material_type="video",
                path=v_path,
                replace_path=v_path 
            )
            video_materials.append(material)
            total_video_duration += material.duration
        except Exception as e:
            logger.error(f"Skipping video {v_path}: {e}")
            continue

    audio_materials = []
    total_audio_duration = 0
    
    for a_path in audio_files:
        try:
            a_path = os.path.abspath(a_path)
            logger.info(f"Processing audio file: {a_path}")
            material = Audio_material(
                path=a_path,
                replace_path=a_path
            )
            audio_materials.append(material)
            total_audio_duration += material.duration
        except Exception as e:
            logger.error(f"Skipping audio {a_path}: {e}")
            continue

    # 4. Calculate image duration if needed
    image_materials_config = [] # List of (path, duration_us)
    
    if image_files and total_audio_duration > total_video_duration:
        remaining_duration = total_audio_duration - total_video_duration
        num_images = len(image_files)
        per_image_duration = remaining_duration // num_images
        remainder = remaining_duration % num_images
        
        logger.info(f"Audio duration ({total_audio_duration}us) > Video duration ({total_video_duration}us). Filling gap ({remaining_duration}us) with {num_images} images.")
        
        for idx, img_path in enumerate(image_files):
            duration = per_image_duration
            if idx == num_images - 1:
                duration += remainder # Add remainder to last image
            
            image_materials_config.append((img_path, duration))
            
    elif image_files:
        logger.info("Images found but audio duration is not longer than video duration, or no audio. Images will not be added.")
    
    # 5. Add Video Track (Videos + Images)
    total_video_duration_us = 0
    if video_materials or image_materials_config:
        try:
            script.get_track(Track_type.video)
        except:
            script.add_track(Track_type.video)
            
        current_time = 0 # microseconds
        
        # Add Videos
        for material in video_materials:
            duration_us = material.duration
            logger.info(f"Adding video segment: {material.material_name}, Duration: {duration_us}us")
            
            source_timerange = trange(0, duration_us)
            target_timerange = trange(current_time, duration_us)
            
            segment = Video_segment(
                material=material,
                source_timerange=source_timerange,
                target_timerange=target_timerange
            )
            
            script.add_segment(segment)
            current_time += duration_us
            
        # Add Images
        for img_path, duration_us in image_materials_config:
            try:
                img_path = os.path.abspath(img_path)
                logger.info(f"Processing image file: {img_path}")
                
                # Create crop settings if provided
                crop = Crop_settings()
                if image_crop_settings:
                    crop = Crop_settings(
                        upper_left_x=image_crop_settings.get("upper_left_x", 0.0),
                        upper_left_y=image_crop_settings.get("upper_left_y", 0.0),
                        upper_right_x=image_crop_settings.get("upper_right_x", 1.0),
                        upper_right_y=image_crop_settings.get("upper_right_y", 0.0),
                        lower_left_x=image_crop_settings.get("lower_left_x", 0.0),
                        lower_left_y=image_crop_settings.get("lower_left_y", 1.0),
                        lower_right_x=image_crop_settings.get("lower_right_x", 1.0),
                        lower_right_y=image_crop_settings.get("lower_right_y", 1.0)
                    )

                # Create material
                material = Video_material(
                    material_type="photo",
                    path=img_path,
                    replace_path=img_path,
                    crop_settings=crop
                )
                
                logger.info(f"Adding image segment: {material.material_name}, Duration: {duration_us}us")
                
                # For images, source timerange starts at 0 and has length of target duration
                source_timerange = trange(0, duration_us)
                target_timerange = trange(current_time, duration_us)
                
                segment = Video_segment(
                    material=material,
                    source_timerange=source_timerange,
                    target_timerange=target_timerange
                )
                
                script.add_segment(segment)
                current_time += duration_us
                
            except Exception as e:
                logger.error(f"Skipping image {img_path}: {e}")
                continue
        
        total_video_duration_us = current_time

    # 6. Add Audio Track
    if audio_materials:
        try:
            script.get_track(Track_type.audio)
        except:
            script.add_track(Track_type.audio)
            
        current_time = 0
        
        for material in audio_materials:
            duration_us = material.duration
            logger.info(f"Adding audio segment: {material.material_name}, Duration: {duration_us}us")
            
            source_timerange = trange(0, duration_us)
            target_timerange = trange(current_time, duration_us)
            
            segment = Audio_segment(
                material=material,
                source_timerange=source_timerange,
                target_timerange=target_timerange
            )
            
            script.add_segment(segment)
            current_time += duration_us

    # 6.5 Add Rich Elements (Watermark, Disclaimer, Effects, Filter)
    # Ensure duration covers both video and audio
    max_duration_us = max(total_video_duration_us, total_audio_duration)
    total_duration_sec = max_duration_us / 1000000.0

    template = None
    if template_id:
        template = template_service.get_template(template_id)
        if not template:
            logger.warning(f"Template {template_id} not found, falling back to default rich elements.")

    if template:
        logger.info(f"Applying template: {template['name']}")
        tracks = template.get("tracks", {})
        
        # Apply Text Tracks
        for i, track in enumerate(tracks.get("texts", [])):
             try:
                # Determine end time
                end_time = track.get("end", 0)
                if track.get("is_full_duration", False) or end_time <= 0:
                    end_time = total_duration_sec
                
                # Handle text styles if present
                text_styles = None
                if track.get("text_styles"):
                    text_styles = []
                    for style_data in track.get("text_styles"):
                        style_dict = style_data.get("style", {})
                        border_dict = style_data.get("border", {})
                        
                        style = Text_style(
                            size=style_dict.get('size', track.get("font_size", 8.0)),
                            bold=style_dict.get('bold', False),
                            italic=style_dict.get('italic', False),
                            underline=style_dict.get('underline', False),
                            color=hex_to_rgb(style_dict.get('color', track.get("font_color", "#FFFFFF"))),
                            alpha=style_dict.get('alpha', track.get("font_alpha", 1.0)),
                            align=style_dict.get('align', 1),
                            vertical=style_dict.get('vertical', track.get("vertical", False)),
                            letter_spacing=style_dict.get('letter_spacing', 0),
                            line_spacing=style_dict.get('line_spacing', 0)
                        )
                        
                        border = None
                        if border_dict.get('width', 0) > 0:
                            border = Text_border(
                                alpha=border_dict.get('alpha', 1.0),
                                color=hex_to_rgb(border_dict.get('color', "#000000")),
                                width=border_dict.get('width', 0)
                            )
                            
                        style_range = TextStyleRange(
                            start=style_data.get("start", 0),
                            end=style_data.get("end", len(track.get("text", ""))),
                            style=style,
                            border=border,
                            font_str=style_data.get("font", track.get("font"))
                        )
                        text_styles.append(style_range)

                add_text_impl(
                    text=track.get("text", "Text"),
                    start=track.get("start", 0),
                    end=end_time,
                    draft_id=draft_id,
                    transform_x=track.get("transform_x", 0),
                    transform_y=track.get("transform_y", 0),
                    font=track.get("font", None),
                    font_size=track.get("font_size", 8.0),
                    font_color=track.get("font_color", "#FFFFFF"),
                    font_alpha=track.get("font_alpha", 1.0),
                    track_name=track.get("track_name", f"template_text_{i}"),
                    vertical=track.get("vertical", False),
                    text_styles=text_styles,
                    background_color=track.get("background_color", "#000000"),
                    background_alpha=track.get("background_alpha", 0.0),
                    border_color=track.get("border_color", "#000000"),
                    border_width=track.get("border_width", 0.0),
                    shadow_enabled=track.get("shadow_enabled", False),
                    shadow_color=track.get("shadow_color", "#000000"),
                    shadow_distance=track.get("shadow_distance", 5.0),
                    shadow_alpha=track.get("shadow_alpha", 0.9)
                )
             except Exception as e:
                 logger.error(f"Failed to apply template text: {e}")

        # Apply Effect Tracks
        for i, track in enumerate(tracks.get("effects", [])):
             try:
                # Determine end time
                end_time = track.get("end", 0)
                if track.get("is_full_duration", False) or end_time <= 0:
                    end_time = total_duration_sec

                add_effect_impl(
                    effect_type=track.get("effect_type"),
                    effect_category=track.get("effect_category", "scene"),
                    start=track.get("start", 0),
                    end=end_time,
                    draft_id=draft_id,
                    track_name=track.get("track_name", f"template_effect_{i}")
                )
             except Exception as e:
                 logger.error(f"Failed to apply template effect: {e}")

        # Apply Filter Tracks
        for i, track in enumerate(tracks.get("filters", [])):
             try:
                # Determine end time
                end_time = track.get("end", 0)
                if track.get("is_full_duration", False) or end_time <= 0:
                    end_time = total_duration_sec

                add_effect_impl(
                    effect_type=track.get("effect_type"),
                    effect_category="filter",
                    start=track.get("start", 0),
                    end=end_time,
                    draft_id=draft_id,
                    track_name=track.get("track_name", f"template_filter_{i}")
                )
             except Exception as e:
                 logger.error(f"Failed to apply template filter: {e}")

    elif total_duration_sec > 0:
        logger.info(f"Adding rich draft elements. Duration: {total_duration_sec}s")
        
        # Add Watermark
        try:
            add_text_impl(
                text="@水印",
                start=0,
                end=total_duration_sec,
                draft_id=draft_id,
                transform_y=0.8,
                transform_x=0.8, # Bottom right
                font=None,
                font_color="#FFFFFF",
                font_alpha=0.5,
                track_name="watermark"
            )
        except Exception as e:
            logger.error(f"Failed to add watermark: {e}")

        # Add Disclaimer
        try:
            add_text_impl(
                text="故事虚构 请勿模仿",
                start=0,
                end=total_duration_sec,
                draft_id=draft_id,
                transform_y=0.85, # Bottom center
                font=None,
                font_size=6.0,
                font_color="#CCCCCC",
                track_name="disclaimer"
            )
        except Exception as e:
            logger.error(f"Failed to add disclaimer: {e}")

        # Add Common Template Text
        try:
            add_text_impl(
                text="通用模板",
                start=0,
                end=total_duration_sec,
                draft_id=draft_id,
                transform_y=-0.8, # Top
                font=None,
                font_color="#FFFFFF",
                track_name="template_text"
            )
        except Exception as e:
            logger.error(f"Failed to add template text: {e}")

        # Add Filter (HD)
        try:
            add_effect_impl(
                effect_type="高清",
                effect_category="filter",
                start=0,
                end=total_duration_sec,
                draft_id=draft_id,
                track_name="filter_hd"
            )
        except Exception as e:
             logger.error(f"Failed to add filter: {e}")

        # Add Effects
        try:
            add_effect_impl(
                effect_type="圣诞星光", # Sparkle substitute (Valid in Video_scene_effect_type)
                effect_category="scene",
                start=0,
                end=total_duration_sec,
                draft_id=draft_id,
                track_name="effect_sparkle"
            )
        except Exception as e:
            logger.error(f"Failed to add sparkle effect: {e}")
            
        try:
            add_effect_impl(
                effect_type="_1998", # Retro substitute
                effect_category="scene",
                start=0,
                end=total_duration_sec,
                draft_id=draft_id,
                track_name="effect_retro"
            )
        except Exception as e:
            logger.error(f"Failed to add retro effect: {e}")

    # 7. Save Draft to Disk
    # Determine template directory
    # Go up 2 levels from this file (services) -> backend -> template_jianying
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(current_dir)
    template_dir_name = "template_jianying" # Force Jianying for desktop usage usually
    template_path = os.path.join(backend_dir, template_dir_name)
    
    target_draft_path = os.path.join(draft_folder, draft_id)
    
    if os.path.exists(target_draft_path):
        shutil.rmtree(target_draft_path)
        
    shutil.copytree(template_path, target_draft_path)
    
    # Update draft_content.json
    script.dump(os.path.join(target_draft_path, "draft_content.json"))
    
    # Update draft_meta_info.json
    meta_path = os.path.join(target_draft_path, "draft_meta_info.json")
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            
        meta['draft_id'] = draft_id
        meta['draft_name'] = draft_name if draft_name else f"AutoDraft_{draft_id}"
        meta['tm_draft_create'] = int(time.time() * 1000000)
        meta['tm_draft_modified'] = int(time.time() * 1000000)
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=4)
            
    logger.info(f"Draft generation completed successfully. ID: {draft_id}")
    return draft_id, script
