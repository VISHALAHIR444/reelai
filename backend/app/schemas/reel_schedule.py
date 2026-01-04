"""Reel Schedule Pydantic schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class ScheduleStatus(str, Enum):
    GENERATED = "generated"
    SCHEDULED = "scheduled"
    READY_FOR_UPLOAD = "ready_for_upload"
    UPLOADED = "uploaded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReelScheduleCreate(BaseModel):
    reel_id: int
    instagram_account_id: int
    scheduled_at: Optional[datetime] = None


class ReelScheduleUpdate(BaseModel):
    status: ScheduleStatus
    error_message: Optional[str] = None


class MarkAsUploadedRequest(BaseModel):
    pass


class ReelScheduleResponse(BaseModel):
    id: int
    reel_id: int
    instagram_account_id: int
    user_id: int
    status: ScheduleStatus
    scheduled_at: Optional[datetime]
    uploaded_at: Optional[datetime]
    failed_at: Optional[datetime]
    error_message: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReelScheduleListResponse(BaseModel):
    schedules: list[ReelScheduleResponse]
    total: int
