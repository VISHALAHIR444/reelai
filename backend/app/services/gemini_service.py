"""Gemini AI service for generating reel metadata"""

import json
import logging
from typing import Dict, Optional
import google.generativeai as genai
from app.core.config import get_settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)
settings = get_settings()


class GeminiAIService:
    """Service for generating AI metadata using Google Gemini API"""
    
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("Gemini API key not configured")
    
    async def generate_reel_metadata(self, 
                                    transcript: Optional[str],
                                    duration: float,
                                    title: Optional[str] = None) -> Dict:
        """
        Generate reel metadata using Gemini API
        
        Returns dict with:
        - title: Short engaging title
        - caption: Instagram caption
        - hashtags: List of hashtags
        - topics: List of topics
        - quality_score: 0.0-1.0
        """
        try:
            if not self.api_key:
                logger.warning("Gemini API key not configured, returning default metadata")
                return self._get_default_metadata()
            
            # Prepare prompt
            prompt = self._build_prompt(transcript, duration, title)
            
            logger.info(f"Generating AI metadata for reel (duration: {duration}s)")
            
            # Call Gemini API
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if not response.text:
                logger.warning("Empty response from Gemini API")
                return self._get_default_metadata()
            
            # Parse response
            metadata = self._parse_gemini_response(response.text)
            
            logger.info(f"Generated metadata: {json.dumps(metadata, indent=2)}")
            return metadata
        
        except Exception as e:
            logger.error(f"Error generating AI metadata: {str(e)}", exc_info=True)
            return self._get_default_metadata()
    
    def _build_prompt(self, transcript: Optional[str], duration: float, title: Optional[str] = None) -> str:
        """Build prompt for Gemini API"""
        context = ""
        
        if title:
            context += f"Video Title: {title}\n"
        
        if transcript:
            # Truncate if too long
            transcript_preview = transcript[:1000] if len(transcript) > 1000 else transcript
            context += f"Transcript: {transcript_preview}\n"
        
        context += f"Duration: {duration}s (Instagram Reel)"
        
        prompt = f"""You are an Instagram content expert. Analyze the following video reel and generate metadata:

{context}

Generate the following in JSON format:
{{
    "title": "A short, engaging title (max 50 chars)",
    "caption": "An engaging Instagram caption with call-to-action (max 150 chars)",
    "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
    "topics": ["topic1", "topic2", "topic3"],
    "quality_score": 0.85
}}

Important:
- Title should be catchy and engaging
- Caption should encourage engagement (likes, comments, shares)
- Hashtags should be relevant and trending
- Topics should describe the main content
- Quality score: 0.0-1.0, where 1.0 is perfect viral potential
- Return ONLY valid JSON, no extra text"""
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse JSON response from Gemini"""
        try:
            # Extract JSON from response
            json_str = response_text.strip()
            
            # If wrapped in markdown code blocks, extract
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            
            json_str = json_str.strip()
            
            metadata = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['title', 'caption', 'hashtags', 'topics', 'quality_score']
            for field in required_fields:
                if field not in metadata:
                    logger.warning(f"Missing field in Gemini response: {field}")
                    return self._get_default_metadata()
            
            # Ensure quality_score is between 0 and 1
            metadata['quality_score'] = max(0.0, min(1.0, float(metadata['quality_score'])))
            
            return metadata
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Response text: {response_text}")
            return self._get_default_metadata()
        
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            return self._get_default_metadata()
    
    def _get_default_metadata(self) -> Dict:
        """Return default metadata when AI generation fails"""
        return {
            'title': 'Check this out!',
            'caption': 'Amazing content! Check it out! 🚀',
            'hashtags': ['#reels', '#viral', '#content', '#awesome', '#explore'],
            'topics': ['entertainment', 'trending'],
            'quality_score': 0.5
        }
    
    def calculate_quality_grade(self, quality_score: float) -> str:
        """Convert quality score to grade"""
        if quality_score >= 0.85:
            return "EXCELLENT"
        elif quality_score >= 0.70:
            return "GOOD"
        elif quality_score >= 0.50:
            return "FAIR"
        else:
            return "POOR"
