"""Application configuration using pydantic-settings"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "GRAVIXAI Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Server
    server_host: str = os.getenv("API_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("API_PORT", 8000))
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./gravixai.db")
    database_echo: bool = False
    
    # Redis & Caching
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_timeout: int = 300
    
    # Security
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Facebook OAuth v19
    facebook_app_id: str = os.getenv("FACEBOOK_APP_ID", "")
    facebook_app_secret: str = os.getenv("FACEBOOK_APP_SECRET", "")
    facebook_redirect_uri: str = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8000/api/social/facebook/callback")
    facebook_api_version: str = "v19.0"
    
    # Gemini AI
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = "gemini-1.5-pro"
    
    # Instagram
    instagram_graph_api_version: str = "v19.0"
    
    # Storage & Files
    videos_dir: str = os.getenv("VIDEOS_DIR", "./videos")
    chunk_duration: int = 35
    reel_width: int = 1080
    reel_height: int = 1920
    
    # Tools
    yt_dlp_path: str = os.getenv("YT_DLP_PATH", "yt-dlp")
    ffmpeg_path: str = os.getenv("FFMPEG_PATH", "ffmpeg")
    
    # CORS
    allowed_origins: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://10.0.0.11:3000").split(",")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Instagram API
    instagram_api_url: str = "https://graph.instagram.com"
    
    # Storage Paths
    storage_base_path: str = "./videos"
    temp_path: str = "./temp"
    
    # FFmpeg
    ffprobe_path: str = os.getenv("FFPROBE_PATH", "ffprobe")
    
    # Video Processing
    video_quality: str = "high"
    max_video_size_mb: int = 500
    
    # Job Configuration
    max_retries: int = 3
    job_timeout: int = 3600
    queue_name: str = "default"
    
    # Celery
    celery_broker_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = Settings()
