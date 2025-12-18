from pydantic import BaseModel
from typing import Optional, List, Any

class AddVideoRequest(BaseModel):
    draft_folder: Optional[str] = None
    video_url: str
    start: float = 0
    end: float = 0
    width: int = 1080
    height: int = 1920
    draft_id: Optional[str] = None
    transform_y: float = 0
    scale_x: float = 1
    scale_y: float = 1
    transform_x: float = 0
    speed: float = 1.0
    target_start: float = 0
    track_name: str = "video_main"
    relative_index: int = 0
    duration: Optional[float] = None
    transition: Optional[str] = None
    transition_duration: float = 0.5
    volume: float = 1.0
    mask_type: Optional[str] = None
    mask_center_x: float = 0.5
    mask_center_y: float = 0.5
    mask_size: float = 1.0
    mask_rotation: float = 0.0
    mask_feather: float = 0.0
    mask_invert: bool = False
    mask_rect_width: Optional[float] = None
    mask_round_corner: Optional[float] = None
    background_blur: Optional[int] = None

class AddAudioRequest(BaseModel):
    draft_folder: Optional[str] = None
    audio_url: str
    start: float = 0
    end: Optional[float] = None
    draft_id: Optional[str] = None
    volume: float = 1.0
    target_start: float = 0
    speed: float = 1.0
    track_name: str = 'audio_main'
    duration: Optional[float] = None
    effect_type: Optional[str] = None
    effect_params: Optional[List[Any]] = None
    width: int = 1080
    height: int = 1920

class CreateDraftRequest(BaseModel):
    width: int = 1080
    height: int = 1920

class AddSubtitleRequest(BaseModel):
    srt: str
    draft_id: Optional[str] = None
    time_offset: float = 0.0
    font: str = "思源粗宋"
    font_size: float = 5.0
    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_color: str = '#FFFFFF'
    vertical: bool = False
    alpha: float = 1
    border_alpha: float = 1.0
    border_color: str = '#000000'
    border_width: float = 0.0
    background_color: str = '#000000'
    background_style: int = 0
    background_alpha: float = 0.0
    transform_x: float = 0.0
    transform_y: float = -0.8
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation: float = 0.0
    track_name: str = 'subtitle'
    width: int = 1080
    height: int = 1920

class TextStyleItem(BaseModel):
    start: int = 0
    end: int = 0
    style: Optional[dict] = None
    border: Optional[dict] = None
    font: Optional[str] = None

class AddTextRequest(BaseModel):
    text: str
    start: float = 0
    end: float = 5
    draft_id: Optional[str] = None
    transform_y: float = 0
    transform_x: float = 0
    font: str = "文轩体"
    color: Optional[str] = None
    font_color: Optional[str] = None
    size: Optional[float] = None
    font_size: Optional[float] = None
    track_name: str = "text_main"
    vertical: bool = False
    alpha: Optional[float] = None
    font_alpha: Optional[float] = None
    outro_animation: Optional[str] = None
    outro_duration: float = 0.5
    width: int = 1080
    height: int = 1920
    fixed_width: float = -1
    fixed_height: float = -1
    border_alpha: float = 1.0
    border_color: str = "#000000"
    border_width: float = 0.0
    background_color: str = "#000000"
    background_style: int = 0
    background_alpha: float = 0.0
    background_round_radius: float = 0.0
    background_height: float = 0.14
    background_width: float = 0.14
    background_horizontal_offset: float = 0.5
    background_vertical_offset: float = 0.5
    shadow_enabled: bool = False
    shadow_alpha: float = 0.9
    shadow_angle: float = -45.0
    shadow_color: str = "#000000"
    shadow_distance: float = 5.0
    shadow_smoothing: float = 0.15
    bubble_effect_id: Optional[str] = None
    bubble_resource_id: Optional[str] = None
    effect_effect_id: Optional[str] = None
    intro_animation: Optional[str] = None
    intro_duration: float = 0.5
    text_styles: Optional[List[TextStyleItem]] = None

class AddImageRequest(BaseModel):
    draft_folder: Optional[str] = None
    image_url: str
    width: int = 1080
    height: int = 1920
    start: float = 0
    end: float = 3.0
    draft_id: Optional[str] = None
    transform_y: float = 0
    scale_x: float = 1
    scale_y: float = 1
    transform_x: float = 0
    track_name: str = "image_main"
    relative_index: int = 0
    animation: Optional[str] = None
    animation_duration: float = 0.5
    intro_animation: Optional[str] = None
    intro_animation_duration: float = 0.5
    outro_animation: Optional[str] = None
    outro_animation_duration: float = 0.5
    combo_animation: Optional[str] = None
    combo_animation_duration: float = 0.5
    transition: Optional[str] = None
    transition_duration: float = 0.5
    mask_type: Optional[str] = None
    mask_center_x: float = 0.0
    mask_center_y: float = 0.0
    mask_size: float = 0.5
    mask_rotation: float = 0.0
    mask_feather: float = 0.0
    mask_invert: bool = False
    mask_rect_width: Optional[float] = None
    mask_round_corner: Optional[float] = None
    background_blur: Optional[int] = None

class AddVideoKeyframeRequest(BaseModel):
    draft_id: Optional[str] = None
    track_name: str = 'video_main'
    property_type: str = 'alpha'
    time: float = 0.0
    value: str = '1.0'
    property_types: Optional[List[str]] = None
    times: Optional[List[float]] = None
    values: Optional[List[str]] = None

class AddEffectRequest(BaseModel):
    effect_type: Optional[str] = None
    start: float = 0
    effect_category: str = "scene"
    end: float = 3.0
    draft_id: Optional[str] = None
    track_name: str = "effect_01"
    params: Optional[List[Any]] = None
    width: int = 1080
    height: int = 1920

class QueryScriptRequest(BaseModel):
    draft_id: Optional[str] = None
    force_update: bool = True

class SaveDraftRequest(BaseModel):
    draft_id: Optional[str] = None
    draft_folder: Optional[str] = None

class QueryDraftStatusRequest(BaseModel):
    task_id: Optional[str] = None

class GenerateDraftUrlRequest(BaseModel):
    draft_id: Optional[str] = None
    draft_folder: Optional[str] = None
