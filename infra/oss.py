import oss2
import os
from config import settings
from infra.logger import logger

class OSSConfigurationError(Exception):
    pass

def validate_oss_config(config_type: str = "general"):
    config = settings.OSS_CONFIG if config_type == "general" else settings.MP4_OSS_CONFIG
    
    # Check if config object is populated (Pydantic model)
    if not config.access_key_id or not config.access_key_secret or not config.bucket_name or not config.endpoint:
        error_msg = f"Missing required OSS configuration for {config_type}. Check your .env file or environment variables."
        logger.error(error_msg)
        raise OSSConfigurationError(error_msg)
    return config

def upload_to_oss(path):
    try:
        config = validate_oss_config("general")
        
        # Create OSS client
        auth = oss2.Auth(config.access_key_id, config.access_key_secret)
        bucket = oss2.Bucket(auth, config.endpoint, config.bucket_name)
        
        # Upload file
        object_name = os.path.basename(path)
        bucket.put_object_from_file(object_name, path)
        
        # Generate signed URL (valid for 24 hours)
        url = bucket.sign_url('GET', object_name, 24 * 60 * 60)
        
        # Clean up temporary file
        if os.path.exists(path):
            os.remove(path)
        
        return url
    except Exception as e:
        logger.error(f"Failed to upload to OSS: {e}")
        raise

def upload_mp4_to_oss(path):
    """Special method for uploading MP4 files, using custom domain and v4 signature"""
    try:
        config = validate_oss_config("mp4")
        
        # Directly use credentials from the configuration file
        auth = oss2.AuthV4(config.access_key_id, config.access_key_secret)
        
        # Create OSS client with custom domain
        bucket = oss2.Bucket(
            auth, 
            config.endpoint, 
            config.bucket_name, 
            region=config.region, 
            is_cname=True
        )
        
        # Upload file
        object_name = os.path.basename(path)
        bucket.put_object_from_file(object_name, path)
        
        # Generate pre-signed URL (valid for 24 hours), set slash_safe to True to avoid path escaping
        url = bucket.sign_url('GET', object_name, 24 * 60 * 60, slash_safe=True)
        
        # Clean up temporary file
        if os.path.exists(path):
            os.remove(path)
        
        return url
    except Exception as e:
        logger.error(f"Failed to upload MP4 to OSS: {e}")
        raise
