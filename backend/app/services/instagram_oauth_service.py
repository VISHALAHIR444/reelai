import logging
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FacebookOAuthService:
    """Facebook OAuth v19.0 for Instagram connection"""
    
    def __init__(self, app_id: str, app_secret: str, redirect_uri: str, api_version: str = "v19.0"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
        self.api_version = api_version
        self.graph_url = f"https://graph.{api_version}"
    
    def get_oauth_url(self, state: str = "") -> str:
        """Generate Facebook OAuth authorization URL"""
        scopes = [
            "pages_show_list",
            "pages_read_engagement",
            "instagram_basic",
            "instagram_content_publish"
        ]
        
        url = (
            f"https://www.facebook.com/{self.api_version}/dialog/oauth?"
            f"client_id={self.app_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={','.join(scopes)}"
            f"&state={state}"
        )
        return url
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for short-lived token"""
        try:
            url = f"https://graph.facebook.com/{self.api_version}/oauth/access_token"
            
            params = {
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "redirect_uri": self.redirect_uri,
                "code": code
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"OAuth error: {data['error']['message']}")
            
            return {
                "short_lived_token": data.get("access_token"),
                "user_id": data.get("user_id"),
                "token_type": data.get("token_type")
            }
        
        except Exception as e:
            logger.error(f"Token exchange error: {str(e)}")
            raise
    
    def get_long_lived_token(self, short_lived_token: str) -> Dict:
        """Convert short-lived token to long-lived token (valid 60 days)"""
        try:
            url = f"https://graph.facebook.com/{self.api_version}/oauth/access_token"
            
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "fb_exchange_token": short_lived_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"Token conversion error: {data['error']['message']}")
            
            expires_in = data.get("expires_in", 5184000)  # 60 days in seconds
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            return {
                "long_lived_token": data.get("access_token"),
                "expires_in": expires_in,
                "expires_at": expires_at
            }
        
        except Exception as e:
            logger.error(f"Long-lived token error: {str(e)}")
            raise
    
    def get_facebook_pages(self, access_token: str) -> list:
        """Get list of Facebook pages for user"""
        try:
            url = f"https://graph.facebook.com/{self.api_version}/me/accounts"
            
            params = {"access_token": access_token}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"Error fetching pages: {data['error']['message']}")
            
            pages = []
            for page in data.get("data", []):
                pages.append({
                    "page_id": page.get("id"),
                    "page_name": page.get("name"),
                    "page_access_token": page.get("access_token")
                })
            
            return pages
        
        except Exception as e:
            logger.error(f"Facebook pages error: {str(e)}")
            raise
    
    def get_instagram_account(self, page_id: str, page_access_token: str) -> Dict:
        """Get Instagram Business Account from Facebook Page"""
        try:
            url = f"https://graph.facebook.com/{self.api_version}/{page_id}"
            
            params = {
                "fields": "instagram_business_account",
                "access_token": page_access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"Error fetching Instagram account: {data['error']['message']}")
            
            ig_account = data.get("instagram_business_account", {})
            
            return {
                "ig_user_id": ig_account.get("id"),
                "ig_username": ig_account.get("username", "")
            }
        
        except Exception as e:
            logger.error(f"Instagram account error: {str(e)}")
            raise
    
    def refresh_long_lived_token(self, current_token: str) -> Dict:
        """Refresh long-lived token to extend expiration"""
        try:
            url = f"https://graph.facebook.com/{self.api_version}/oauth/access_token"
            
            params = {
                "grant_type": "fb_exchange_token",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "fb_exchange_token": current_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"Token refresh error: {data['error']['message']}")
            
            expires_in = data.get("expires_in", 5184000)
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            
            return {
                "long_lived_token": data.get("access_token"),
                "expires_in": expires_in,
                "expires_at": expires_at
            }
        
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            raise
