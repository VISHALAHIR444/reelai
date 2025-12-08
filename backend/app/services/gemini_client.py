import logging
from typing import Dict, List
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini AI for metadata generation"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        self.api_key = api_key
        self.model = model
        
        if api_key:
            genai.configure(api_key=api_key)
        else:
            logger.warning("Gemini API key not configured")
    
    def generate_reel_metadata(self, 
                              transcript: str,
                              video_title: str = "",
                              video_description: str = "") -> Dict:
        """
        Generate title, caption, hashtags, and topics for a reel
        """
        try:
            if not self.api_key:
                logger.warning("Gemini not configured - returning defaults")
                return self._get_default_metadata()
            
            prompt = f"""Analyze this video content and generate Instagram Reel metadata.

Video Title: {video_title}
Video Description: {video_description}

Transcript/Content:
{transcript[:2000]}  # Limit to 2000 chars

Generate a JSON response with:
- title: catchy reel title (max 100 chars)
- caption: engaging caption (max 300 chars)
- hashtags: 10-15 relevant hashtags (as string, space-separated)
- topics: 3-5 topic labels (as comma-separated string)
- quality_score: content quality 0-100

Return ONLY valid JSON, no markdown."""
            
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            
            # Parse response
            import json
            try:
                result = json.loads(response.text)
                return {
                    "title": result.get("title", "Check this out!"),
                    "caption": result.get("caption", "Amazing content"),
                    "hashtags": result.get("hashtags", "#viral #content #shorts"),
                    "topics": result.get("topics", "Entertainment,Creative,Trending"),
                    "quality_score": float(result.get("quality_score", 75))
                }
            except json.JSONDecodeError:
                logger.warning("Failed to parse Gemini response")
                return self._get_default_metadata()
        
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            return self._get_default_metadata()
    
    def _get_default_metadata(self) -> Dict:
        """Return default metadata when Gemini is not available"""
        return {
            "title": "Check this out!",
            "caption": "Amazing content you'll love! 🔥",
            "hashtags": "#viral #content #shorts #trending",
            "topics": "Entertainment,Creative,Trending",
            "quality_score": 75.0
        }
