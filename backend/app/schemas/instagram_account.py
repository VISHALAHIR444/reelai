"""Instagram Account Pydantic schemas"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class AccountStatus(str, Enum):
    PENDING_VERIFICATION = "pending_verification"
    CONNECTED = "connected"
    VERIFICATION_FAILED = "verification_failed"
    INACTIVE = "inactive"


class InstagramAccountCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=255)
    label: Optional[str] = Field(None, max_length=255)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        v = v.strip().lower()
        if not v.replace('_', '').replace('.', '').isalnum():
            raise ValueError('Invalid Instagram username format')
        return v


class InstagramAccountUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=255)


class InstagramAccountStatusUpdate(BaseModel):
    status: AccountStatus


class InstagramAccountResponse(BaseModel):
    id: int
    user_id: int
    username: str
    label: Optional[str]
    status: AccountStatus
    verified_by_post: bool
    verification_attempts: int
    last_verification_error: Optional[str]
    connected_at: Optional[datetime]
    last_verified_at: Optional[datetime]
    last_used_at: Optional[datetime]
    automation_enabled: bool
    device_bound: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InstagramAccountListResponse(BaseModel):
    accounts: list[InstagramAccountResponse]
    total: int
