from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from typing import Optional

class OSSConfig(BaseModel):
    bucket_name: str = ""
    access_key_id: str = ""
    access_key_secret: str = ""
    endpoint: str = ""
    region: Optional[str] = None

class Settings(BaseSettings):
    IS_CAPCUT_ENV: bool = Field(default=True, alias="is_capcut_env")
    DRAFT_DOMAIN: str = Field(default="http://localhost:9001", alias="draft_domain")
    PORT: int = Field(default=9001, alias="port")
    PREVIEW_ROUTER: str = Field(default="/draft/downloader", alias="preview_router")
    IS_UPLOAD_DRAFT: bool = Field(default=False, alias="is_upload_draft")
    
    OSS_CONFIG: OSSConfig = Field(default_factory=OSSConfig, alias="oss_config")
    MP4_OSS_CONFIG: OSSConfig = Field(default_factory=OSSConfig, alias="mp4_oss_config")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__"
    )

# Instantiate
settings = Settings()
