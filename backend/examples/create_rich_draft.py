import os
import sys
import json
import time

# Add parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from example import add_video_impl, add_text_impl, add_effect, make_request, save_draft_impl

def create_rich_draft():
    """
    Create a rich draft with watermark, disclaimer, effects, etc.
    """
    print("Creating rich draft...")
    
    # 1. Add Main Video
    # Using a sample video URL (replace with actual if needed)
    video_url = "https://pan.superbed.cn/share/1nbrg1fl/jimeng_daweidai.mp4"
    
    print("1. Adding Main Video...")
    video_result = add_video_impl(
        video_url=video_url,
        start=0,
        end=10.0,
        target_start=0,
        width=1080,
        height=1920
    )
    
    if not video_result.get('success'):
        print(f"Failed to add video: {video_result.get('error')}")
        return
        
    draft_id = video_result['output']['draft_id']
    print(f"Draft created with ID: {draft_id}")
    
    # 2. Add Watermark Text
    print("2. Adding Watermark...")
    add_text_impl(
        text="@水印",
        start=0,
        end=10.0,
        draft_id=draft_id,
        track_name="watermark_track",
        transform_y=0.8,  # Position near bottom
        font="系统默认",
        font_size=10.0,
        font_color="#FFFFFF",
        font_alpha=0.8
    )
    
    # 3. Add Disclaimer Text
    print("3. Adding Disclaimer...")
    add_text_impl(
        text="故事虚构 请勿模仿",
        start=0,
        end=10.0,
        draft_id=draft_id,
        track_name="disclaimer_track",
        transform_y=0.85, # Below watermark
        font="系统默认",
        font_size=6.0,
        font_color="#CCCCCC"
    )
    
    # 4. Add "Common Template" Text
    print("4. Adding 'Common Template' text...")
    add_text_impl(
        text="通用模板",
        start=0,
        end=10.0,
        draft_id=draft_id,
        track_name="template_track",
        transform_y=-0.8, # Top
        font="系统默认",
        font_color="#FFFFFF",
        font_size=8.0
    )
    
    # 5. Add "Image Quality Enhancement" (Using '高清' filter as proxy)
    print("5. Adding 'Image Quality Enhancement' (高清 Filter)...")
    add_effect(
        effect_type="高清",
        effect_category="filter",
        start=0,
        end=10.0,
        draft_id=draft_id,
        track_name="filter_hd"
    )
    
    # 6. Add "Sparkle" Effect (星火)
    print("6. Adding 'Sparkle' Effect...")
    add_effect(
        effect_type="星火",
        effect_category="scene",
        start=0,
        end=10.0,
        draft_id=draft_id,
        track_name="effect_sparkle"
    )
    
    # 7. Add "Ripple Distortion" Effect (波纹扭曲)
    print("7. Adding 'Ripple Distortion' Effect...")
    add_effect(
        effect_type="波纹扭曲",
        effect_category="scene",
        start=0,
        end=10.0,
        draft_id=draft_id,
        track_name="effect_ripple"
    )
    
    print("\nDraft generation complete!")
    print(f"Draft ID: {draft_id}")
    
    # Save draft (optional, but good to ensure it's written to disk)
    # Note: save_draft_impl usually downloads materials.
    # If we are running locally and just modifying the draft object in memory/cache, we might need to trigger a save.
    # The 'add_*' functions usually update the draft in cache.
    # The 'save_draft_impl' downloads it.
    
    # Assuming the user wants to open it in JianYing/CapCut.
    # We should output the draft path.
    
    # Define a local output folder for the draft
    output_folder = os.path.join(os.getcwd(), "output_drafts")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Saving draft to: {output_folder}")
    save_res = save_draft_impl(draft_id, output_folder)
    print(f"Save result: {save_res}")

if __name__ == "__main__":
    create_rich_draft()
