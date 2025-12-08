"""Facebook and Instagram OAuth service"""

import httpx
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlencode, parse_qs
from typing import Dict, Optional, Tuple
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class FacebookOAuthService:
    """Handle Facebook OAuth flow and token management"""
    
    # Facebook API endpoints
    FB_AUTHORIZE_URL = "https://www.facebook.com/v18.0/dialog/oauth"
    FB_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    FB_GRAPH_URL = "https://graph.facebook.com/v18.0"
    
    def __init__(self):
        self.app_id = settings.FACEBOOK_APP_ID
        self.app_secret = settings.FACEBOOK_APP_SECRET
        self.redirect_uri = settings.FACEBOOK_REDIRECT_URI
        
    def generate_login_url(self) -> Tuple[str, str]:
        """Generate Facebook login URL with state parameter"""
        state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "scope": "instagram_basic,instagram_manage_messages,pages_show_list,pages_manage_metadata",
            "state": state,
            "response_type": "code",
            "auth_type": "rerequest",
        }
        
        login_url = f"{self.FB_AUTHORIZE_URL}?{urlencode(params)}"
        logger.info(f"Generated Facebook login URL for state: {state}")
        
        return login_url, state
    
    async def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for short-lived access token"""
        try:
            params = {
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "redirect_uri": self.redirect_uri,
                "code": code,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.FB_TOKEN_URL, params=params)
                response.raise_for_status()
                data = response.json()
            
            logger.info(f"Successfully exchanged code for short-lived token")
            return {
                "success": True,
                "short_lived_token": data.get("access_token"),
                "expires_in": data.get("expires_in", 3600),
                "token_type": data.get("token_type", "Bearer"),
            }
        except Exception as e:
            logger.error(f"Failed to exchange code: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }
    
    async def get_long_lived_token(self, short_lived_token: str) -> Dict:
        """Convert short-lived token to long-lived token (60 days validity)"""
        try:
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "fb_exchange_token": short_lived_token,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.FB_GRAPH_URL}/oauth/access_token", params=params)
                response.raise_for_status()
                data = response.json()
            
            expires_in = data.get("expires_in", 5184000)  # 60 days default
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            logger.info(f"Successfully converted to long-lived token, expires in {expires_in}s")
            return {
                "success": True,
                "long_lived_token": data.get("access_token"),
                "expires_in": expires_in,
                "expires_at": expires_at,
                "token_type": data.get("token_type", "Bearer"),
            }
        except Exception as e:
            logger.error(f"Failed to get long-lived token: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }
    
    async def get_facebook_page_id(self, access_token: str) -> Dict:
        """Fetch Facebook page ID and details from user's pages"""
        try:
            params = {
                "access_token": access_token,
                "fields": "id,name,access_token",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.FB_GRAPH_URL}/me/accounts", params=params)
                response.raise_for_status()
                data = response.json()
            
            pages = data.get("data", [])
            if not pages:
                return {"success": False, "error": "No Facebook pages found"}
            
            # Use first page (can be extended to select specific page)
            page = pages[0]
            logger.info(f"Fetched Facebook page: {page.get('name')} (ID: {page.get('id')})")
            
            return {
                "success": True,
                "fb_page_id": page.get("id"),
                "fb_page_name": page.get("name"),
                "page_access_token": page.get("access_token"),
            }
        except Exception as e:
            logger.error(f"Failed to fetch Facebook page: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_instagram_business_account(self, fb_page_id: str, access_token: str) -> Dict:
        """Fetch Instagram Business Account linked to Facebook Page"""
        try:
            params = {
                "access_token": access_token,
                "fields": "instagram_business_account",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.FB_GRAPH_URL}/{fb_page_id}", params=params)
                response.raise_for_status()
                data = response.json()
            
            ig_account_id = data.get("instagram_business_account", {}).get("id")
            if not ig_account_id:
                return {"success": False, "error": "No Instagram business account found"}
            
            # Get Instagram account details
            ig_details = await self.get_instagram_account_details(ig_account_id, access_token)
            
            if ig_details["success"]:
                logger.info(f"Fetched Instagram account: {ig_details.get('username')} (ID: {ig_account_id})")
                return {
                    "success": True,
                    "ig_user_id": ig_account_id,
                    "instagram_username": ig_details.get("username"),
                    "ig_profile_picture": ig_details.get("profile_picture_url"),
                }
            
            return ig_details
        except Exception as e:
            logger.error(f"Failed to fetch Instagram business account: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_instagram_account_details(self, ig_user_id: str, access_token: str) -> Dict:
        """Get Instagram account details"""
        try:
            params = {
                "access_token": access_token,
                "fields": "id,username,name,biography,website,profile_picture_url,followers_count",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.FB_GRAPH_URL}/{ig_user_id}", params=params)
                response.raise_for_status()
                data = response.json()
            
            return {
                "success": True,
                "ig_user_id": data.get("id"),
                "username": data.get("username"),
                "name": data.get("name"),
                "biography": data.get("biography"),
                "website": data.get("website"),
                "profile_picture_url": data.get("profile_picture_url"),
                "followers_count": data.get("followers_count"),
            }
        except Exception as e:
            logger.error(f"Failed to fetch Instagram account details: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def refresh_long_lived_token(self, current_token: str) -> Dict:
        """Refresh long-lived token (gets new 60 days validity)"""
        try:
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "fb_exchange_token": current_token,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.FB_GRAPH_URL}/oauth/access_token", params=params)
                response.raise_for_status()
                data = response.json()
            
            expires_in = data.get("expires_in", 5184000)  # 60 days
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            logger.info(f"Successfully refreshed long-lived token, new expiry: {expires_at}")
            return {
                "success": True,
                "new_token": data.get("access_token"),
                "expires_in": expires_in,
                "expires_at": expires_at,
            }
        except Exception as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def validate_token(self, access_token: str) -> Dict:
        """Validate if access token is still valid"""
        try:
            params = {
                "access_token": access_token,
                "fields": "id,app_id,application,data_access_expires_at,expires_at",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.FB_GRAPH_URL}/debug_token", params=params)
                response.raise_for_status()
                data = response.json().get("data", {})
            
            is_valid = data.get("is_valid", False)
            expires_at = data.get("expires_at")
            
            return {
                "success": True,
                "is_valid": is_valid,
                "expires_at": expires_at,
                "app_id": data.get("app_id"),
            }
        except Exception as e:
            logger.error(f"Failed to validate token: {str(e)}")
            return {"success": False, "error": str(e), "is_valid": False}
