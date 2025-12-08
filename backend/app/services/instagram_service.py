"""Instagram upload and integration service"""

import logging
import httpx
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from app.core.config import get_settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)
settings = get_settings()


class InstagramService:
    """Service for Instagram Graph API integration"""
    
    def __init__(self):
        self.api_version = settings.instagram_graph_api_version
        self.api_url = settings.instagram_api_url
        self.timeout = 30
    
    async def get_oauth_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate OAuth authorization URL
        
        User will be redirected to Instagram to authorize the app
        """
        oauth_url = (
            f"https://api.instagram.com/oauth/authorize?"
            f"client_id={settings.instagram_business_account_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope=instagram_business_basic,instagram_business_content_publish&"
            f"response_type=code&"
            f"state={state}"
        )
        
        logger.info(f"Generated OAuth URL for Instagram")
        return oauth_url
    
    async def handle_oauth_callback(self, code: str, redirect_uri: str) -> Tuple[bool, Optional[Dict]]:
        """
        Handle OAuth callback and exchange code for access token
        
        Returns: (success, token_data)
        token_data: {"access_token": "...", "user_id": "...", "username": "..."}
        """
        try:
            # Exchange code for short-lived token
            token_url = f"{self.api_url}/oauth/access_token"
            
            params = {
                'client_id': settings.instagram_business_account_id,
                'client_secret': settings.instagram_business_account_id,  # In production, use separate secret
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
                'code': code,
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(token_url, data=params)
                response.raise_for_status()
                token_data = response.json()
            
            if 'access_token' not in token_data:
                logger.error(f"No access token in response: {token_data}")
                return False, None
            
            short_lived_token = token_data['access_token']
            
            # Exchange for long-lived token (valid for 60 days)
            long_token_data = await self._exchange_for_long_lived_token(short_lived_token)
            
            if not long_token_data:
                logger.warning("Could not get long-lived token, using short-lived")
                long_token_data = {
                    'access_token': short_lived_token,
                    'expires_in': 3600,
                }
            
            # Get user info
            user_info = await self._get_user_info(long_token_data['access_token'])
            
            if not user_info:
                logger.error("Could not get user info")
                return False, None
            
            result = {
                'access_token': long_token_data['access_token'],
                'user_id': user_info.get('id'),
                'username': user_info.get('username'),
                'expires_in': long_token_data.get('expires_in'),
            }
            
            logger.info(f"Instagram OAuth successful. User: {user_info.get('username')}")
            return True, result
        
        except Exception as e:
            logger.error(f"Error in OAuth callback: {str(e)}", exc_info=True)
            return False, None
    
    async def _exchange_for_long_lived_token(self, short_lived_token: str) -> Optional[Dict]:
        """Exchange short-lived token for long-lived token"""
        try:
            url = f"{self.api_url}/access_token"
            
            params = {
                'grant_type': 'ig_refresh_token',
                'access_token': short_lived_token,
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            logger.warning(f"Could not exchange for long-lived token: {str(e)}")
            return None
    
    async def _get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get authenticated user info"""
        try:
            url = f"{self.api_url}/me"
            
            params = {
                'fields': 'id,username,name',
                'access_token': access_token,
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            return None
    
    async def upload_reel(self, 
                         reel_file_path: str,
                         caption: str,
                         access_token: str,
                         thumbnail_path: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Upload reel to Instagram
        
        Returns: (success, post_id, post_url)
        """
        try:
            logger.info(f"Uploading reel to Instagram: {reel_file_path}")
            
            # Get user's business account ID
            user_info = await self._get_user_info(access_token)
            if not user_info:
                logger.error("Could not get user info for upload")
                return False, None, None
            
            user_id = user_info['id']
            
            # Create media container
            media_id = await self._create_media_container(
                user_id, 
                reel_file_path, 
                caption, 
                access_token
            )
            
            if not media_id:
                logger.error("Failed to create media container")
                return False, None, None
            
            # Publish media
            post_id, post_url = await self._publish_media(media_id, access_token)
            
            if post_id:
                logger.info(f"Reel uploaded successfully. Post ID: {post_id}")
                return True, post_id, post_url
            else:
                logger.error("Failed to publish media")
                return False, None, None
        
        except Exception as e:
            logger.error(f"Error uploading reel: {str(e)}", exc_info=True)
            return False, None, None
    
    async def _create_media_container(self,
                                     user_id: str,
                                     video_path: str,
                                     caption: str,
                                     access_token: str) -> Optional[str]:
        """Create media container for video upload"""
        try:
            url = f"{self.api_url}/{user_id}/media"
            
            # Upload video file
            with open(video_path, 'rb') as f:
                files = {'video': f}
                
                data = {
                    'media_type': 'REELS',
                    'caption': caption,
                    'access_token': access_token,
                }
                
                async with httpx.AsyncClient(timeout=300) as client:
                    response = await client.post(url, data=data, files=files)
                    response.raise_for_status()
                    result = response.json()
            
            media_id = result.get('id')
            if media_id:
                logger.info(f"Media container created: {media_id}")
                return media_id
            else:
                logger.error(f"No media ID in response: {result}")
                return None
        
        except Exception as e:
            logger.error(f"Error creating media container: {str(e)}")
            return None
    
    async def _publish_media(self, media_id: str, access_token: str) -> Tuple[Optional[str], Optional[str]]:
        """Publish media to Instagram"""
        try:
            url = f"{self.api_url}/{media_id}/publish"
            
            data = {
                'access_token': access_token,
            }
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, data=data)
                response.raise_for_status()
                result = response.json()
            
            post_id = result.get('id')
            post_url = f"https://instagram.com/p/{post_id}" if post_id else None
            
            if post_id:
                logger.info(f"Media published. Post ID: {post_id}")
                return post_id, post_url
            else:
                logger.error(f"No post ID in response: {result}")
                return None, None
        
        except Exception as e:
            logger.error(f"Error publishing media: {str(e)}")
            return None, None
    
    async def disconnect_account(self, access_token: str) -> bool:
        """Revoke Instagram access"""
        try:
            url = f"{self.api_url}/me/permissions"
            
            data = {
                'access_token': access_token,
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(url, data=data)
                response.raise_for_status()
            
            logger.info("Instagram account disconnected")
            return True
        
        except Exception as e:
            logger.error(f"Error disconnecting Instagram: {str(e)}")
            return False

        """Disconnect Instagram account - placeholder"""
        # TODO: Remove stored access token
        pass
