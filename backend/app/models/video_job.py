"""Video processing job model for database"""

from sqlalchemy import Column, String, Integer, Float, Enum as SQLEnum, ForeignKey
from enum import Enum
from app.db.base import Base, IDMixin, TimestampMixin


class JobStatus(str, Enum):
    """Video processing job status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoJob(IDMixin, TimestampMixin, Base):
    """Video processing job model"""
    
    __tablename__ = "video_jobs"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    youtube_url = Column(String(500), nullable=False)
    job_status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False)
    
    # Video metadata
    video_title = Column(String(500), nullable=True)
    video_duration = Column(Float, nullable=True)  # in seconds
    num_reels = Column(Integer, nullable=True)
    
    # Processing details
    error_message = Column(String(500), nullable=True)
    progress_percentage = Column(Integer, default=0, nullable=False)
    
    # Storage
    celery_task_id = Column(String(255), nullable=True, unique=True)
    
    def __repr__(self) -> str:
        return f"<VideoJob {self.id} - {self.job_status}>"
