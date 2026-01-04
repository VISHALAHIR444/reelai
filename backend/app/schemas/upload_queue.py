"""Upload Queue Schemas"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UploadQueueCreate(BaseModel):
    """Schema for adding reel to upload queue"""
    reel_id: str = Field(..., description="Reel ID")
    instagram_account_id: int = Field(..., description="Instagram account ID")


class UploadQueueUpdate(BaseModel):
    """Schema for updating upload status"""
    upload_status: str = Field(..., pattern="^(pending|uploaded|failed)$")
    upload_error: Optional[str] = None
    instagram_post_id: Optional[str] = None
    instagram_url: Optional[str] = None


class UploadQueueResponse(BaseModel):
    """Schema for upload queue response"""
    id: int
    reel_id: str
    instagram_account_id: int
    upload_status: str
    upload_error: Optional[str]
    uploaded_at: Optional[datetime]
    instagram_post_id: Optional[str]
    instagram_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Nested data
    instagram_account: dict
    reel: dict
    
    class Config:
        from_attributes = True
