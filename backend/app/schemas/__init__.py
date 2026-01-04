"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Video Schemas
class VideoBase(BaseModel):
    youtube_url: str


class VideoCreate(VideoBase):
    pass


class VideoResponse(VideoBase):
    id: str
    youtube_video_id: str
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VideoDetailResponse(VideoResponse):
    transcript: Optional[str] = None
    chunks: List['VideoChunkResponse'] = []
    reels: List['ReelResponse'] = []


# VideoChunk Schemas
class VideoChunkResponse(BaseModel):
    id: str
    chunk_index: int
    start_time: int
    end_time: int
    duration: int
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True


# Reel Schemas
class ReelCreate(BaseModel):
    chunk_id: str
    chunk_index: int
    title: str
    caption: str
    hashtags: str
    topics: str
    quality_score: float


class ReelResponse(BaseModel):
    id: str
    chunk_index: int
    title: str
    caption: str
    hashtags: str
    topics: str
    quality_score: float
    publish_status: str
    ig_media_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Instagram Settings Schemas
class InstagramTokenBase(BaseModel):
    fb_page_id: str
    fb_page_name: str
    fb_user_id: str
    ig_user_id: str
    long_lived_access_token: str
    token_expires_at: datetime


class InstagramTokenCreate(InstagramTokenBase):
    pass


class InstagramTokenResponse(InstagramTokenBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Social/OAuth Schemas
class FacebookOAuthCallbackRequest(BaseModel):
    code: str


class SocialStatusResponse(BaseModel):
    connected: bool
    ig_user_id: Optional[str] = None
    fb_page_name: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class SocialDisconnectResponse(BaseModel):
    success: bool
    message: str


# Job Schemas
class JobResponse(BaseModel):
    id: str
    job_type: str
    status: str
    progress: float
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Processing Log Schemas
class ProcessingLogResponse(BaseModel):
    id: int
    level: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
