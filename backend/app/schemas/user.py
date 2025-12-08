"""Pydantic schemas for users"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    instagram_connected: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserDetail(UserResponse):
    """Detailed user schema"""
    instagram_user_id: Optional[str] = None
    is_superuser: bool
