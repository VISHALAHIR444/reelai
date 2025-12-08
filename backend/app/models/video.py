"""Video and Video Chunk models"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base, IDMixin, TimestampMixin


class VideoStatus(str, enum.Enum):
    """Video processing status"""
    UPLOADED = "uploaded"
    DOWNLOADING = "downloading"
    DOWNLOADED = "downloaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Video(Base, IDMixin, TimestampMixin):
    """Video model for YouTube videos"""
    __tablename__ = "videos"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    youtube_url = Column(String(500), nullable=False)
    youtube_video_id = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    duration = Column(Float, nullable=True)  # in seconds
    thumbnail_url = Column(String(500), nullable=True)
    
    status = Column(Enum(VideoStatus), default=VideoStatus.UPLOADED, index=True)
    error_message = Column(Text, nullable=True)
    
    # File paths
    video_file_path = Column(String(500), nullable=True)
    audio_file_path = Column(String(500), nullable=True)
    transcript = Column(Text, nullable=True)
    transcript_source = Column(String(50), nullable=True)  # youtube, google_speech
    
    # Metadata
    metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Relationships
    user = relationship("User", back_populates="videos")
    chunks = relationship("VideoChunk", back_populates="video", cascade="all, delete-orphan")
    reels = relationship("Reel", back_populates="video", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="video", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Video(id={self.id}, youtube_id={self.youtube_video_id}, status={self.status})>"


class VideoChunk(Base, IDMixin, TimestampMixin):
    """Video chunk model - sequential cuts from video"""
    __tablename__ = "video_chunks"
    
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False, index=True)
    chunk_number = Column(Integer, nullable=False)  # Sequential: 1, 2, 3...
    start_time = Column(Float, nullable=False)  # in seconds
    end_time = Column(Float, nullable=False)  # in seconds
    duration = Column(Float, nullable=False)  # in seconds
    
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)  # in bytes
    
    # Relationships
    video = relationship("Video", back_populates="chunks")
    reels = relationship("Reel", back_populates="chunk")
    
    def __repr__(self):
        return f"<VideoChunk(video_id={self.video_id}, chunk={self.chunk_number}, {self.start_time}s-{self.end_time}s)>"
