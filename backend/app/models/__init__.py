"""SQLAlchemy ORM models"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class InstagramAccount(Base):
    """Instagram account registry for manual upload queue"""
    __tablename__ = "instagram_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    label = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False, index=True)
    
    automation_enabled = Column(Boolean, default=False)
    last_used_at = Column(DateTime, nullable=True)
    
    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    upload_queue = relationship("UploadQueue", back_populates="instagram_account")


class UploadQueue(Base):
    """Manual upload queue for reels"""
    __tablename__ = "upload_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    reel_id = Column(String, ForeignKey("reels.id"), nullable=False, index=True)
    instagram_account_id = Column(Integer, ForeignKey("instagram_accounts.id"), nullable=False, index=True)
    
    upload_status = Column(String, default="pending", nullable=False, index=True)
    upload_error = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)
    
    instagram_post_id = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reel = relationship("Reel")
    instagram_account = relationship("InstagramAccount", back_populates="upload_queue")


class InstagramSettings(Base):
    """Instagram OAuth and account settings"""
    __tablename__ = "instagram_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    fb_page_id = Column(String, unique=True, index=True)
    fb_page_name = Column(String)
    fb_user_id = Column(String, index=True)
    ig_user_id = Column(String, unique=True, index=True)
    long_lived_access_token = Column(String)
    token_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    videos = relationship("Video", back_populates="instagram_account")


class Video(Base):
    """YouTube video record"""
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, index=True)
    youtube_url = Column(String, index=True)
    youtube_video_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    thumbnail_url = Column(String)
    duration = Column(Integer, nullable=True)  # in seconds
    download_path = Column(String)
    transcript = Column(Text)
    
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text)
    
    instagram_account_id = Column(Integer, ForeignKey("instagram_settings.id"))
    instagram_account = relationship("InstagramSettings", back_populates="videos")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chunks = relationship("VideoChunk", back_populates="video", cascade="all, delete-orphan")
    reels = relationship("Reel", back_populates="video", cascade="all, delete-orphan")
    logs = relationship("ProcessingLog", back_populates="video", cascade="all, delete-orphan")


class VideoChunk(Base):
    """35-second video chunks cut from original"""
    __tablename__ = "video_chunks"
    
    id = Column(String, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.id"))
    video = relationship("Video", back_populates="chunks")
    
    chunk_index = Column(Integer)  # 0, 1, 2, ...
    start_time = Column(Integer)  # in seconds
    end_time = Column(Integer)
    duration = Column(Integer)
    file_path = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Reel(Base):
    """Processed Instagram Reel (1080x1920)"""
    __tablename__ = "reels"
    
    id = Column(String, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.id"))
    video = relationship("Video", back_populates="reels")
    
    chunk_id = Column(String)
    chunk_index = Column(Integer)
    
    title = Column(String)
    caption = Column(Text)
    hashtags = Column(String)
    topics = Column(String)
    quality_score = Column(Float)
    
    file_path = Column(String)
    duration = Column(Integer)
    
    # Instagram Publishing
    ig_media_id = Column(String, unique=True, nullable=True)
    publish_status = Column(String, default="pending")  # pending, uploaded, published, failed
    publish_error = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Job(Base):
    """Background job tracking"""
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, index=True)
    job_type = Column(String)  # yt_download, video_cutting, vertical_convert, ai_generate, publish
    video_id = Column(String, ForeignKey("videos.id"), nullable=True)
    
    status = Column(String, default="queued")  # queued, processing, completed, failed
    progress = Column(Float, default=0.0)
    
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessingLog(Base):
    """Detailed processing logs"""
    __tablename__ = "processing_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.id"))
    video = relationship("Video", back_populates="logs")
    
    level = Column(String)  # INFO, WARNING, ERROR
    message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


__all__ = ["Base", "InstagramAccount", "UploadQueue", "InstagramSettings", "Video", "VideoChunk", "Reel", "Job", "ProcessingLog"]
