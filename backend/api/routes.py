from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
import shutil
import json
import os
from services.save_draft_impl import download_script
from infra.cache_service import draft_cache
from typing import Any
from api.dto import (
    AddVideoRequest,
    AddAudioRequest,
    CreateDraftRequest,
    AddSubtitleRequest,
    AddTextRequest,
    AddImageRequest,
    AddVideoKeyframeRequest,
    AddEffectRequest,
    QueryScriptRequest,
    SaveDraftRequest,
    QueryDraftStatusRequest,
    GenerateDraftUrlRequest,
    GenerateBatchDraftRequest,
)
from services import (
    add_video_track,
    add_audio_track,
    add_text_impl,
    add_subtitle_impl,
    add_image_impl,
    add_video_keyframe_impl,
    add_effect_impl,
    add_sticker_impl,
    save_draft_impl,
    query_task_status,
    query_script_impl,
    create_draft,
    generate_batch_draft,
)
from domain.pyJianYingDraft.text_segment import TextStyleRange, Text_style, Text_border
from domain.pyJianYingDraft.metadata.animation_meta import Intro_type, Outro_type
from domain.pyJianYingDraft.metadata.capcut_animation_meta import CapCut_Intro_type, CapCut_Outro_type
from domain.pyJianYingDraft.metadata.video_effect_meta import Video_scene_effect_type, Video_character_effect_type
from domain.pyJianYingDraft.metadata.capcut_effect_meta import CapCut_Video_scene_effect_type, CapCut_Video_character_effect_type
from domain.pyJianYingDraft.metadata.font_meta import Font_type
from domain.pyJianYingDraft.metadata.animation_meta import Text_intro, Text_outro, Text_loop_anim
from domain.pyJianYingDraft.metadata.capcut_text_animation_meta import CapCut_Text_intro, CapCut_Text_outro, CapCut_Text_loop_anim
from config import settings
from infra.util import generate_draft_url as utilgenerate_draft_url, hex_to_rgb
from infra.logger import logger

router = APIRouter()

@router.post('/add_video')
def add_video(body: AddVideoRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.video_url:
        result["error"] = "Hi, the required parameters 'video_url' are missing."
        return result
    try:
        draft_result = add_video_track(
            draft_folder=body.draft_folder,
            video_url=body.video_url,
            width=body.width,
            height=body.height,
            start=body.start,
            end=body.end,
            target_start=body.target_start,
            draft_id=body.draft_id,
            transform_y=body.transform_y,
            scale_x=body.scale_x,
            scale_y=body.scale_y,
            transform_x=body.transform_x,
            speed=body.speed,
            track_name=body.track_name,
            relative_index=body.relative_index,
            duration=body.duration,
            transition=body.transition,
            transition_duration=body.transition_duration,
            volume=body.volume,
            mask_type=body.mask_type,
            mask_center_x=body.mask_center_x,
            mask_center_y=body.mask_center_y,
            mask_size=body.mask_size,
            mask_rotation=body.mask_rotation,
            mask_feather=body.mask_feather,
            mask_invert=body.mask_invert,
            mask_rect_width=body.mask_rect_width,
            mask_round_corner=body.mask_round_corner,
            background_blur=body.background_blur
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while processing video: {str(e)}."
        return result

@router.post('/add_audio')
def add_audio(body: AddAudioRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.audio_url:
        result["error"] = "Hi, the required parameters 'audio_url' are missing."
        return result
    try:
        sound_effects = None
        if body.effect_type is not None:
            sound_effects = [(body.effect_type, body.effect_params)]
        draft_result = add_audio_track(
            draft_folder=body.draft_folder,
            audio_url=body.audio_url,
            start=body.start,
            end=body.end,
            target_start=body.target_start,
            draft_id=body.draft_id,
            volume=body.volume,
            track_name=body.track_name,
            speed=body.speed,
            sound_effects=sound_effects,
            width=body.width,
            height=body.height,
            duration=body.duration
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while processing audio: {str(e)}."
        return result

@router.post('/create_draft')
def create_draft_service(body: CreateDraftRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    try:
        script, draft_id = create_draft(width=body.width, height=body.height)
        result["success"] = True
        result["output"] = {"draft_id": draft_id, "draft_url": utilgenerate_draft_url(draft_id)}
        return result
    except Exception as e:
        result["error"] = f"Error occurred while creating draft: {str(e)}."
        return result

@router.post('/add_subtitle')
def add_subtitle(body: AddSubtitleRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.srt:
        result["error"] = "Hi, the required parameters 'srt' are missing."
        return result
    try:
        draft_result = add_subtitle_impl(
            srt_path=body.srt,
            draft_id=body.draft_id,
            track_name=body.track_name,
            time_offset=body.time_offset,
            font=body.font,
            font_size=body.font_size,
            bold=body.bold,
            italic=body.italic,
            underline=body.underline,
            font_color=body.font_color,
            vertical=body.vertical,
            alpha=body.alpha,
            border_alpha=body.border_alpha,
            border_color=body.border_color,
            border_width=body.border_width,
            background_color=body.background_color,
            background_style=body.background_style,
            background_alpha=body.background_alpha,
            transform_x=body.transform_x,
            transform_y=body.transform_y,
            scale_x=body.scale_x,
            scale_y=body.scale_y,
            rotation=body.rotation,
            width=body.width,
            height=body.height
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while processing subtitle: {str(e)}."
        return result

@router.post('/add_text')
def add_text(body: AddTextRequest) -> dict[str, Any]:
    text = body.text
    start = body.start
    end = body.end
    font = body.font
    font_color = body.color if body.color is not None else (body.font_color if body.font_color is not None else "#FF0000")
    font_size = body.size if body.size is not None else (body.font_size if body.font_size is not None else 8.0)
    font_alpha = body.alpha if body.alpha is not None else (body.font_alpha if body.font_alpha is not None else 1.0)
    text_styles = None
    if body.text_styles:
        text_styles = []
        for style_data in body.text_styles:
            start_pos = style_data.start
            end_pos = style_data.end
            style = Text_style(
                size=(style_data.style or {}).get('size', font_size),
                bold=(style_data.style or {}).get('bold', False),
                italic=(style_data.style or {}).get('italic', False),
                underline=(style_data.style or {}).get('underline', False),
                color=hex_to_rgb((style_data.style or {}).get('color', font_color)),
                alpha=(style_data.style or {}).get('alpha', font_alpha),
                align=(style_data.style or {}).get('align', 1),
                vertical=(style_data.style or {}).get('vertical', body.vertical),
                letter_spacing=(style_data.style or {}).get('letter_spacing', 0),
                line_spacing=(style_data.style or {}).get('line_spacing', 0)
            )
            border = None
            if (style_data.border or {}).get('width', 0) > 0:
                border = Text_border(
                    alpha=(style_data.border or {}).get('alpha', body.border_alpha),
                    color=hex_to_rgb((style_data.border or {}).get('color', body.border_color)),
                    width=(style_data.border or {}).get('width', body.border_width)
                )
            style_range = TextStyleRange(
                start=start_pos,
                end=end_pos,
                style=style,
                border=border,
                font_str=style_data.font or font
            )
            text_styles.append(style_range)
    result = {"success": False, "output": "", "error": ""}
    if not text or start is None or end is None:
        result["error"] = "Hi, the required parameters 'text', 'start' or 'end' are missing. "
        return result
    try:
        draft_result = add_text_impl(
            text=text,
            start=start,
            end=end,
            draft_id=body.draft_id,
            transform_y=body.transform_y,
            transform_x=body.transform_x,
            font=font,
            font_color=font_color,
            font_size=font_size,
            track_name=body.track_name,
            vertical=body.vertical,
            font_alpha=font_alpha,
            border_alpha=body.border_alpha,
            border_color=body.border_color,
            border_width=body.border_width,
            background_color=body.background_color,
            background_style=body.background_style,
            background_alpha=body.background_alpha,
            background_round_radius=body.background_round_radius,
            background_height=body.background_height,
            background_width=body.background_width,
            background_horizontal_offset=body.background_horizontal_offset,
            background_vertical_offset=body.background_vertical_offset,
            shadow_enabled=body.shadow_enabled,
            shadow_alpha=body.shadow_alpha,
            shadow_angle=body.shadow_angle,
            shadow_color=body.shadow_color,
            shadow_distance=body.shadow_distance,
            shadow_smoothing=body.shadow_smoothing,
            bubble_effect_id=body.bubble_effect_id,
            bubble_resource_id=body.bubble_resource_id,
            effect_effect_id=body.effect_effect_id,
            intro_animation=body.intro_animation,
            intro_duration=body.intro_duration,
            outro_animation=body.outro_animation,
            outro_duration=body.outro_duration,
            width=body.width,
            height=body.height,
            fixed_width=body.fixed_width,
            fixed_height=body.fixed_height,
            text_styles=text_styles
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while processing text: {str(e)}. You can click the link below for help: "
        return result

@router.post('/add_image')
def add_image(body: AddImageRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.image_url:
        result["error"] = "Hi, the required parameters 'image_url' are missing."
        return result
    try:
        draft_result = add_image_impl(
            draft_folder=body.draft_folder,
            image_url=body.image_url,
            width=body.width,
            height=body.height,
            start=body.start,
            end=body.end,
            draft_id=body.draft_id,
            transform_y=body.transform_y,
            scale_x=body.scale_x,
            scale_y=body.scale_y,
            transform_x=body.transform_x,
            track_name=body.track_name,
            relative_index=body.relative_index,
            animation=body.animation,
            animation_duration=body.animation_duration,
            intro_animation=body.intro_animation,
            intro_animation_duration=body.intro_animation_duration,
            outro_animation=body.outro_animation,
            outro_animation_duration=body.outro_animation_duration,
            combo_animation=body.combo_animation,
            combo_animation_duration=body.combo_animation_duration,
            transition=body.transition,
            transition_duration=body.transition_duration,
            mask_type=body.mask_type,
            mask_center_x=body.mask_center_x,
            mask_center_y=body.mask_center_y,
            mask_size=body.mask_size,
            mask_rotation=body.mask_rotation,
            mask_feather=body.mask_feather,
            mask_invert=body.mask_invert,
            mask_rect_width=body.mask_rect_width,
            mask_round_corner=body.mask_round_corner,
            background_blur=body.background_blur
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while processing image: {str(e)}."
        return result

@router.post('/add_video_keyframe')
def add_video_keyframe(body: AddVideoKeyframeRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    try:
        draft_result = add_video_keyframe_impl(
            draft_id=body.draft_id,
            track_name=body.track_name,
            property_type=body.property_type,
            time=body.time,
            value=body.value,
            property_types=body.property_types,
            times=body.times,
            values=body.values
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while adding keyframe: {str(e)}."
        return result

@router.post('/add_effect')
def add_effect(body: AddEffectRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.effect_type:
        result["error"] = "Hi, the required parameters 'effect_type' are missing. Please add them and try again."
        return result
    try:
        draft_result = add_effect_impl(
            effect_type=body.effect_type,
            effect_category=body.effect_category,
            start=body.start,
            end=body.end,
            draft_id=body.draft_id,
            track_name=body.track_name,
            params=body.params,
            width=body.width,
            height=body.height
        )
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while adding effect: {str(e)}. "
        return result

@router.post('/query_script')
def query_script(body: QueryScriptRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.draft_id:
        result["error"] = "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
        return result
    try:
        script = query_script_impl(draft_id=body.draft_id, force_update=body.force_update)
        if script is None:
            result["error"] = f"Draft {body.draft_id} does not exist in cache."
            return result
        script_str = script.dumps()
        result["success"] = True
        result["output"] = script_str
        return result
    except Exception as e:
        result["error"] = f"Error occurred while querying script: {str(e)}. "
        return result

@router.post('/save_draft')
def save_draft(body: SaveDraftRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.draft_id:
        result["error"] = "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
        return result
    try:
        draft_result = save_draft_impl(body.draft_id, body.draft_folder)
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while saving draft: {str(e)}. "
        return result

@router.post('/query_draft_status')
def query_draft_status(body: QueryDraftStatusRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.task_id:
        result["error"] = "Hi, the required parameter 'task_id' is missing. Please add it and try again."
        return result
    try:
        task_status = query_task_status(body.task_id)
        if task_status["status"] == "not_found":
            result["error"] = f"Task with ID {body.task_id} not found. Please check if the task ID is correct."
            return result
        result["success"] = True
        result["output"] = task_status
        return result
    except Exception as e:
        result["error"] = f"Error occurred while querying task status: {str(e)}."
        return result

@router.post('/generate_draft_url')
def generate_draft_url(body: GenerateDraftUrlRequest) -> dict[str, Any]:
    result = {"success": False, "output": "", "error": ""}
    if not body.draft_id:
        result["error"] = "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
        return result
    try:
        draft_result = {"draft_url": f"{DRAFT_DOMAIN}{settings.PREVIEW_ROUTER}?={body.draft_id}"}
        result["success"] = True
        result["output"] = draft_result
        return result
    except Exception as e:
        result["error"] = f"Error occurred while saving draft: {str(e)}."
        return result

@router.post('/add_sticker')
def add_sticker(body: GenerateDraftUrlRequest) -> dict[str, Any]:
    return {"success": False, "output": "", "error": "Not implemented in new routing"}

@router.post('/generate_batch_draft')
def generate_batch_draft_endpoint(body: GenerateBatchDraftRequest) -> dict[str, Any]:
    logger.info(f"Received generate_batch_draft request: {body}")
    result = {"success": False, "output": "", "error": ""}
    if not body.video_dir or not body.audio_dir or not body.draft_folder:
        error_msg = "Hi, the required parameters 'video_dir', 'audio_dir', or 'draft_folder' are missing."
        logger.warning(error_msg)
        result["error"] = error_msg
        return result
    try:
        draft_id, script = generate_batch_draft.generate_draft_from_local_materials(
            video_dir=body.video_dir,
            audio_dir=body.audio_dir,
            draft_folder=body.draft_folder,
            draft_name=body.draft_name,
            image_dir=body.image_dir,
            image_crop_settings=body.image_crop_settings
        )
        logger.info(f"Successfully generated batch draft with ID: {draft_id}")
        result["success"] = True
        result["output"] = {"draft_id": draft_id}
        return result
    except Exception as e:
        logger.error(f"Error occurred while generating batch draft: {str(e)}", exc_info=True)
        result["error"] = f"Error occurred while generating batch draft: {str(e)}."
        return result

@router.get('/get_intro_animation_types')
def get_intro_animation_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        animation_types = []
        if settings.IS_CAPCUT_ENV:
            for name, member in CapCut_Intro_type.__members__.items():
                animation_types.append({"name": name})
        else:
            for name, member in Intro_type.__members__.items():
                animation_types.append({"name": name})
        result["output"] = animation_types
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting entrance animation types: {str(e)}"
        return result

@router.get('/get_outro_animation_types')
def get_outro_animation_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        types = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Outro_type.__members__.items():
                types.append({"name": name})
        else:
            for name, member in Outro_type.__members__.items():
                types.append({"name": name})
        result["output"] = types
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting text entrance animation types: {str(e)}"
        return result

@router.get('/get_text_intro_types')
def get_text_intro_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        lst = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Text_intro.__members__.items():
                lst.append({"name": name})
        else:
            for name, member in Text_intro.__members__.items():
                lst.append({"name": name})
        result["output"] = lst
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting text entrance animation types: {str(e)}"
        return result

@router.get('/get_text_outro_types')
def get_text_outro_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        lst = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Text_outro.__members__.items():
                lst.append({"name": name})
        else:
            for name, member in Text_outro.__members__.items():
                lst.append({"name": name})
        result["output"] = lst
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting text exit animation types: {str(e)}"
        return result

@router.get('/get_text_loop_anim_types')
def get_text_loop_anim_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        lst = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Text_loop_anim.__members__.items():
                lst.append({"name": name})
        else:
            for name, member in Text_loop_anim.__members__.items():
                lst.append({"name": name})
        result["output"] = lst
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting text loop animation types: {str(e)}"
        return result

@router.get('/get_video_scene_effect_types')
def get_video_scene_effect_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        effect_types = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Video_scene_effect_type.__members__.items():
                effect_types.append({"name": name})
        else:
            for name, member in Video_scene_effect_type.__members__.items():
                effect_types.append({"name": name})
        result["output"] = effect_types
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting scene effect types: {str(e)}"
        return result

@router.get('/get_video_character_effect_types')
def get_video_character_effect_types() -> dict[str, Any]:
    result = {"success": True, "output": "", "error": ""}
    try:
        effect_types = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Video_character_effect_type.__members__.items():
                effect_types.append({"name": name})
        else:
            for name, member in Video_character_effect_type.__members__.items():
                effect_types.append({"name": name})
        result["output"] = effect_types
        return result
    except Exception as e:
        result["success"] = False
        result["error"] = f"Error occurred while getting character effect types: {str(e)}"
        return result

@router.get('/draft/downloader')
def download_draft(draft_id: str, is_capcut: int = 1, background_tasks: BackgroundTasks = None):
    # Check cache
    script = draft_cache.get(draft_id)
    if not script:
         return {"success": False, "error": "Draft not found in cache. Please verify the draft_id."}
    
    # Prepare temp dir
    temp_dir = os.path.join("tmp", "downloads", draft_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Convert script to dict
        script_data = json.loads(script.dumps())
        
        # Download assets and generate draft structure
        # We pass temp_dir as draft_folder. download_script will create {temp_dir}/{draft_id}
        dl_result = download_script(draft_id, temp_dir, script_data, is_capcut=bool(is_capcut))
        
        if not dl_result.get("success", False):
            # If download failed, clean up and return error
            shutil.rmtree(temp_dir, ignore_errors=True)
            return dl_result

        # Path to the generated draft folder
        draft_path = os.path.join(temp_dir, draft_id)
        
        # Zip it
        # output filename without extension
        zip_base_name = os.path.join("tmp", "zips", draft_id)
        os.makedirs(os.path.dirname(zip_base_name), exist_ok=True)
        
        zip_path = shutil.make_archive(zip_base_name, 'zip', root_dir=temp_dir, base_dir=draft_id)
        
        # Cleanup temp dir (source files) immediately
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        # Schedule zip deletion
        if background_tasks:
            background_tasks.add_task(os.remove, zip_path)
            
        return FileResponse(zip_path, filename=f"{draft_id}.zip", media_type='application/zip')
        
    except Exception as e:
        logger.error(f"Download failed: {e}", exc_info=True)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {"success": False, "error": str(e)}
