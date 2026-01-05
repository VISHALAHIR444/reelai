"""Instagram Image Publisher - Graph API Implementation"""

import requests
import logging
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class InstagramImagePublisher:
    """
    Publish images to Instagram using Graph API.
    
    This service handles the two-step process required by Instagram Graph API:
    1. Create a media container with the image
    2. Publish the container
    
    Documentation: https://developers.facebook.com/docs/instagram-api/reference/ig-user/media
    """
    
    GRAPH_API_VERSION = "v19.0"
    GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ReelsStudio/1.0'
        })
    
    def upload_and_publish_image(
        self,
        ig_user_id: str,
        image_url: str,
        caption: str,
        access_token: str,
        location_id: Optional[str] = None
    ) -> Dict:
        """
        Upload and publish an image to Instagram.
        
        Args:
            ig_user_id: Instagram Business Account ID
            image_url: Publicly accessible URL of the image
            caption: Image caption (max 2200 characters)
            access_token: Valid Instagram access token
            location_id: Optional Instagram location ID
            
        Returns:
            Dict with 'success' boolean and 'data' or 'error'
        """
        
        try:
            # Step 1: Create media container
            container_id = self._create_media_container(
                ig_user_id=ig_user_id,
                image_url=image_url,
                caption=caption,
                access_token=access_token,
                location_id=location_id
            )
            
            if not container_id:
                return {
                    "success": False,
                    "error": "Failed to create media container"
                }
            
            logger.info(f"Media container created: {container_id}")
            
            # Step 2: Publish the container
            media_id = self._publish_media_container(
                ig_user_id=ig_user_id,
                creation_id=container_id,
                access_token=access_token
            )
            
            if not media_id:
                return {
                    "success": False,
                    "error": "Failed to publish media container"
                }
            
            logger.info(f"Image published successfully: {media_id}")
            
            return {
                "success": True,
                "data": {
                    "container_id": container_id,
                    "media_id": media_id,
                    "ig_user_id": ig_user_id
                }
            }
            
        except Exception as e:
            logger.error(f"Error publishing image: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_media_container(
        self,
        ig_user_id: str,
        image_url: str,
        caption: str,
        access_token: str,
        location_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Create an Instagram media container.
        
        Returns:
            Container ID if successful, None otherwise
        """
        
        url = f"{self.GRAPH_API_BASE_URL}/{ig_user_id}/media"
        
        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token
        }
        
        if location_id:
            payload["location_id"] = location_id
        
        try:
            response = self.session.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            container_id = data.get("id")
            
            if not container_id:
                logger.error(f"No container ID in response: {data}")
                return None
            
            return container_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create media container: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
    
    def _publish_media_container(
        self,
        ig_user_id: str,
        creation_id: str,
        access_token: str
    ) -> Optional[str]:
        """
        Publish an Instagram media container.
        
        Returns:
            Media ID if successful, None otherwise
        """
        
        url = f"{self.GRAPH_API_BASE_URL}/{ig_user_id}/media_publish"
        
        payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }
        
        try:
            response = self.session.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            media_id = data.get("id")
            
            if not media_id:
                logger.error(f"No media ID in response: {data}")
                return None
            
            return media_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to publish media container: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            return None
    
    def check_container_status(
        self,
        container_id: str,
        access_token: str
    ) -> Dict:
        """
        Check the status of a media container.
        
        Useful for debugging and monitoring container processing.
        
        Returns:
            Dict with container status information
        """
        
        url = f"{self.GRAPH_API_BASE_URL}/{container_id}"
        
        params = {
            "fields": "id,status,status_code",
            "access_token": access_token
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check container status: {str(e)}")
            return {"error": str(e)}
