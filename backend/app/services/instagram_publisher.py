import logging
import requests
from typing import Dict, Optional
import time

logger = logging.getLogger(__name__)


class InstagramPublisher:
    """Publish reels to Instagram using Graph API v19"""
    
    def __init__(self, api_version: str = "v19.0"):
        self.api_version = api_version
        self.graph_url = f"https://graph.instagram.com/{api_version}"
    
    def upload_reel(self,
                    ig_user_id: str,
                    video_url: str,
                    caption: str,
                    access_token: str) -> Dict:
        """
        Upload reel video to Instagram (create media object)
        
        Returns: {media_id, status}
        """
        try:
            url = f"{self.graph_url}/{ig_user_id}/media"
            
            payload = {
                "media_type": "VIDEO",
                "video_url": video_url,
                "caption": caption,
                "access_token": access_token
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                error_msg = data["error"].get("message", "Unknown error")
                raise Exception(f"Upload error: {error_msg}")
            
            media_id = data.get("id")
            logger.info(f"Reel uploaded: {media_id}")
            
            return {
                "media_id": media_id,
                "status": "uploaded",
                "success": True
            }
        
        except Exception as e:
            logger.error(f"Reel upload error: {str(e)}")
            return {
                "media_id": None,
                "status": "failed",
                "success": False,
                "error": str(e)
            }
    
    def publish_reel(self,
                     ig_user_id: str,
                     media_id: str,
                     access_token: str) -> Dict:
        """
        Publish uploaded media to Instagram feed
        
        Returns: {reel_id, status}
        """
        try:
            url = f"{self.graph_url}/{ig_user_id}/media_publish"
            
            payload = {
                "creation_id": media_id,
                "access_token": access_token
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                error_msg = data["error"].get("message", "Unknown error")
                raise Exception(f"Publish error: {error_msg}")
            
            reel_id = data.get("id")
            logger.info(f"Reel published: {reel_id}")
            
            return {
                "reel_id": reel_id,
                "status": "published",
                "success": True
            }
        
        except Exception as e:
            logger.error(f"Reel publish error: {str(e)}")
            return {
                "reel_id": None,
                "status": "failed",
                "success": False,
                "error": str(e)
            }
    
    def upload_and_publish(self,
                          ig_user_id: str,
                          video_url: str,
                          caption: str,
                          access_token: str) -> Dict:
        """
        Complete flow: upload -> wait -> publish
        """
        try:
            # Step 1: Upload
            upload_result = self.upload_reel(ig_user_id, video_url, caption, access_token)
            
            if not upload_result.get("success"):
                return upload_result
            
            media_id = upload_result["media_id"]
            
            # Step 2: Wait for processing (usually instant, but sometimes takes a moment)
            time.sleep(2)
            
            # Step 3: Publish
            publish_result = self.publish_reel(ig_user_id, media_id, access_token)
            
            if publish_result.get("success"):
                return {
                    "reel_id": publish_result["reel_id"],
                    "media_id": media_id,
                    "status": "published",
                    "success": True
                }
            else:
                return {
                    "media_id": media_id,
                    "status": "upload_only",
                    "success": False,
                    "error": "Publishing failed, but media was uploaded"
                }
        
        except Exception as e:
            logger.error(f"Upload and publish error: {str(e)}")
            return {
                "status": "failed",
                "success": False,
                "error": str(e)
            }
    
    def get_media_info(self,
                       media_id: str,
                       access_token: str) -> Dict:
        """Get media information"""
        try:
            url = f"{self.graph_url}/{media_id}"
            
            params = {
                "fields": "id,media_type,media_product_type,status",
                "access_token": access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"Error fetching media: {data['error'].get('message')}")
            
            return {
                "media_id": data.get("id"),
                "media_type": data.get("media_type"),
                "status": data.get("status"),
                "product_type": data.get("media_product_type")
            }
        
        except Exception as e:
            logger.error(f"Media info error: {str(e)}")
            return {"error": str(e)}
