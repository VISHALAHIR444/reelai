"""Social account connection schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FacebookLoginRequest(BaseModel):
    """Request to generate Facebook login URL"""
    pass


class FacebookLoginResponse(BaseModel):
    """Facebook login URL response"""
    login_url: str = Field(..., description="Facebook OAuth login URL")
    state: str = Field(..., description="State parameter for security")


class FacebookCallbackRequest(BaseModel):
    """Facebook OAuth callback request"""
    code: str = Field(..., description="Authorization code from Facebook")
    state: str = Field(..., description="State parameter for verification")


class TokenExchangeResponse(BaseModel):
    """Token exchange response"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None


class InstagramAccountInfo(BaseModel):
    """Instagram account information"""
    ig_user_id: str
    instagram_username: str
    ig_profile_picture: Optional[str] = None


class FacebookPageInfo(BaseModel):
    """Facebook page information"""
    fb_page_id: str
    fb_page_name: str
    fb_user_id: Optional[str] = None


class SocialAccountStatus(BaseModel):
    """Social account connection status"""
    is_connected: bool
    connection_type: str = "instagram"  # instagram, facebook
    instagram_username: Optional[str] = None
    instagram_user_id: Optional[str] = None
    facebook_page_name: Optional[str] = None
    facebook_page_id: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    is_token_valid: bool
    last_refreshed_at: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    """Request to refresh access token"""
    pass


class RefreshTokenResponse(BaseModel):
    """Token refresh response"""
    success: bool
    message: str
    new_expires_at: Optional[datetime] = None
    token_refreshed: bool


class DisconnectAccountRequest(BaseModel):
    """Request to disconnect social account"""
    pass


class DisconnectAccountResponse(BaseModel):
    """Account disconnection response"""
    success: bool
    message: str
    disconnected: bool


class FacebookConnectResponse(BaseModel):
    """Full Facebook connection response"""
    success: bool
    message: str
    instagram_account: Optional[InstagramAccountInfo] = None
    facebook_page: Optional[FacebookPageInfo] = None
    token_expires_at: Optional[datetime] = None
    permissions: Optional[List[str]] = None


class SocialAccountError(BaseModel):
    """Social account error response"""
    error: bool
    error_code: str
    error_message: str
    details: Optional[dict] = None
