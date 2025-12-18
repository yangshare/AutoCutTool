import os
import glob
import shutil
import json
import time
from typing import List, Optional
from domain.pyJianYingDraft import Script_file, Video_material, Audio_material, Video_segment, Audio_segment, trange, Clip_settings
from domain.pyJianYingDraft import Track_type
from services.create_draft import get_or_create_draft
from infra.cache_service import draft_cache
from config import settings

def generate_draft_from_local_materials(
    video_dir: str,
    audio_dir: str,
    draft_folder: str,
    draft_name: Optional[str] = None
):
    """
    Generate a draft from local video and audio directories.
    """
    # 1. Create a new draft in memory
    draft_id, script = get_or_create_draft()
    
    # 2. Scan directories
    video_extensions = ['*.mp4', '*.mov', '*.avi', '*.mkv']
    audio_extensions = ['*.mp3', '*.wav', '*.aac', '*.m4a']
    
    video_files = []
    if os.path.exists(video_dir):
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(video_dir, ext)))
    
    audio_files = []
    if os.path.exists(audio_dir):
        for ext in audio_extensions:
            audio_files.extend(glob.glob(os.path.join(audio_dir, ext)))
        
    video_files.sort()
    audio_files.sort()
    
    # 3. Add Video Track
    if video_files:
        try:
            script.get_track(Track_type.video)
        except:
            script.add_track(Track_type.video)
            
        current_time = 0 # microseconds
        
        for v_path in video_files:
            try:
                # normalize path
                v_path = os.path.abspath(v_path)
                material = Video_material(
                    material_type="video",
                    path=v_path,
                    replace_path=v_path 
                )
            except Exception as e:
                print(f"Skipping video {v_path}: {e}")
                continue
            
            duration_us = material.duration
            
            source_timerange = trange(0, duration_us)
            target_timerange = trange(current_time, current_time + duration_us)
            
            segment = Video_segment(
                material=material,
                source_timerange=source_timerange,
                target_timerange=target_timerange
            )
            
            script.add_segment(segment)
            current_time += duration_us

    # 4. Add Audio Track
    if audio_files:
        try:
            script.get_track(Track_type.audio)
        except:
            script.add_track(Track_type.audio)
            
        current_time = 0
        
        for a_path in audio_files:
            try:
                a_path = os.path.abspath(a_path)
                material = Audio_material(
                    path=a_path,
                    replace_path=a_path
                )
            except Exception as e:
                print(f"Skipping audio {a_path}: {e}")
                continue
                
            duration_us = material.duration
            
            source_timerange = trange(0, duration_us)
            target_timerange = trange(current_time, current_time + duration_us)
            
            segment = Audio_segment(
                material=material,
                source_timerange=source_timerange,
                target_timerange=target_timerange
            )
            
            script.add_segment(segment)
            current_time += duration_us

    # 5. Save Draft to Disk
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
            
    return draft_id, script
