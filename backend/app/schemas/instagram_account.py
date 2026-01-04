"""Instagram Account Schemas"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re


class InstagramAccountCreate(BaseModel):
    """Schema for creating Instagram account"""
    username: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=200)
    status: str = Field(default="active", pattern="^(active|inactive)$")
    
    @validator('username')
    def validate_username(cls, v):
        if not v:
            raise ValueError('Username cannot be empty')
        # Instagram username validation: alphanumeric, dots, underscores
        if not re.match(r'^[a-zA-Z0-9._]+$', v):
            raise ValueError('Invalid Instagram username format')
        if len(v) > 30:
            raise ValueError('Username too long (max 30 characters)')
        return v.lower().strip()
    
    @validator('label')
    def validate_label(cls, v):
        if not v.strip():
            raise ValueError('Label cannot be empty')
        return v.strip()


class InstagramAccountUpdate(BaseModel):
    """Schema for updating Instagram account"""
    label: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[str] = Field(None, pattern="^(active|inactive)$")
    automation_enabled: Optional[bool] = None
    
    @validator('label')
    def validate_label(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Label cannot be empty')
        return v.strip() if v else v


class InstagramAccountResponse(BaseModel):
    """Schema for Instagram account response"""
    id: int
    username: str
    label: str
    status: str
    automation_enabled: bool
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InstagramAccountListResponse(BaseModel):
    """Schema for list of Instagram accounts"""
    accounts: list[InstagramAccountResponse]
    total: int
    active_count: int
    inactive_count: int
