"""Pydantic schemas for video jobs and reels"""

from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


class JobStatusEnum(str, Enum):
    """Job status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReelSchema(BaseModel):
    """Schema for individual reel"""
    id: int
    reel_number: int
    start_time: float
    end_time: float
    duration: float
    is_uploaded: bool
    instagram_post_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class VideoJobCreate(BaseModel):
    """Schema for creating video job"""
    youtube_url: str


class VideoJobResponse(BaseModel):
    """Schema for video job response"""
    id: int
    youtube_url: str
    job_status: JobStatusEnum
    video_title: Optional[str] = None
    video_duration: Optional[float] = None
    num_reels: Optional[int] = None
    progress_percentage: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VideoJobDetail(VideoJobResponse):
    """Detailed video job schema with reels"""
    error_message: Optional[str] = None
    reels: List[ReelSchema] = []
