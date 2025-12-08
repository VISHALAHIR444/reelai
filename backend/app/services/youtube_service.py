"""YouTube video download and processing service"""

import asyncio
import os
import subprocess
import json
from typing import Optional, Dict, Any, Tuple
from pathlib import Path
import logging
from datetime import datetime
import yt_dlp
from google.cloud import speech_v1
from app.core.config import get_settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)
settings = get_settings()


class YouTubeService:
    """Service for downloading and processing YouTube videos"""
    
    def __init__(self):
        self.storage_base = settings.storage_base_path
        self.temp_path = settings.temp_path
        self.ffmpeg_path = settings.ffmpeg_path
        self.ffprobe_path = settings.ffprobe_path
        
        # Create directories if they don't exist
        Path(self.storage_base).mkdir(parents=True, exist_ok=True)
        Path(self.temp_path).mkdir(parents=True, exist_ok=True)
    
    def extract_youtube_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        try:
            if "youtu.be/" in url:
                return url.split("youtu.be/")[-1].split("?")[0]
            elif "youtube.com" in url:
                if "v=" in url:
                    return url.split("v=")[1].split("&")[0]
            return None
        except Exception as e:
            logger.error(f"Error extracting YouTube ID: {str(e)}")
            return None
    
    async def download_video(self, youtube_url: str, video_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Download YouTube video in highest quality MP4
        
        Returns: (success, result_dict)
        result_dict: {"video_path": str, "audio_path": str, "metadata": {...}}
        """
        try:
            video_dir = Path(self.storage_base) / video_id
            video_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Starting YouTube download: {youtube_url}")
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': str(video_dir / '%(id)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': 30,
            }
            
            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
            
            video_path = video_dir / f"{video_id}.mp4"
            
            if not video_path.exists():
                logger.error(f"Video file not found after download: {video_path}")
                return False, None
            
            logger.info(f"Video downloaded successfully: {video_path}")
            
            # Extract audio
            audio_path = await self._extract_audio(str(video_path), video_id)
            
            # Get transcript
            transcript = await self._get_transcript(youtube_url, video_id)
            
            # Get metadata
            duration = info.get('duration')
            title = info.get('title')
            description = info.get('description', '')
            thumbnail_url = info.get('thumbnail')
            
            result = {
                'video_path': str(video_path),
                'audio_path': audio_path,
                'transcript': transcript,
                'duration': duration,
                'title': title,
                'description': description,
                'thumbnail_url': thumbnail_url,
                'youtube_video_id': video_id,
                'file_size': os.path.getsize(video_path),
            }
            
            logger.info(f"YouTube download complete. Duration: {duration}s, Size: {result['file_size']} bytes")
            return True, result
        
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {str(e)}", exc_info=True)
            return False, None
    
    async def _extract_audio(self, video_path: str, video_id: str) -> Optional[str]:
        """Extract audio from video using FFmpeg"""
        try:
            audio_path = Path(self.storage_base) / video_id / f"{video_id}_audio.m4a"
            
            cmd = [
                self.ffmpeg_path,
                '-i', video_path,
                '-q:a', '0',  # highest quality audio
                '-map', 'a',
                '-c:a', 'aac',
                str(audio_path),
                '-y'  # overwrite
            ]
            
            logger.info(f"Extracting audio from video: {video_path}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0 and audio_path.exists():
                logger.info(f"Audio extracted: {audio_path}")
                return str(audio_path)
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            return None
    
    async def _get_transcript(self, youtube_url: str, video_id: str) -> Tuple[Optional[str], str]:
        """
        Get transcript from YouTube or generate using Google Speech-to-Text
        
        Returns: (transcript_text, source)
        """
        try:
            # Try to get transcript from YouTube directly (if available)
            transcript = await self._get_youtube_transcript(youtube_url)
            if transcript:
                logger.info(f"Got transcript from YouTube")
                return transcript, "youtube"
            
            logger.info(f"YouTube transcript not available, generating using Speech-to-Text")
            # Generate transcript from audio
            audio_path = Path(self.storage_base) / video_id / f"{video_id}_audio.m4a"
            if audio_path.exists():
                transcript = await self._speech_to_text(str(audio_path))
                if transcript:
                    return transcript, "google_speech"
            
            return None, None
        
        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            return None, None
    
    async def _get_youtube_transcript(self, youtube_url: str) -> Optional[str]:
        """Attempt to get transcript from YouTube API"""
        try:
            # This is a simplified version - in production, use youtube-transcript-api
            # For now, return None to trigger Speech-to-Text fallback
            logger.info("YouTube transcript extraction not configured")
            return None
        except Exception as e:
            logger.warning(f"Could not get YouTube transcript: {str(e)}")
            return None
    
    async def _speech_to_text(self, audio_path: str) -> Optional[str]:
        """Convert audio to text using Google Speech-to-Text"""
        try:
            if not settings.google_application_credentials:
                logger.warning("Google Cloud credentials not configured")
                return None
            
            client = speech_v1.SpeechClient()
            
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Read audio file
            with open(audio_path, 'rb') as audio_file:
                content = audio_file.read()
            
            # Create audio object
            audio = speech_v1.RecognitionAudio(content=content)
            
            # Configure recognition
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
                enable_automatic_punctuation=True,
            )
            
            # Perform transcription
            response = client.recognize(config=config, audio=audio)
            
            # Extract transcript
            transcript = ""
            for result in response.results:
                for alternative in result.alternatives:
                    transcript += alternative.transcript + " "
            
            logger.info(f"Transcription complete: {len(transcript)} characters")
            return transcript.strip() if transcript else None
        
        except Exception as e:
            logger.error(f"Error in speech-to-text: {str(e)}")
            return None
    
    def get_video_duration(self, video_path: str) -> Optional[float]:
        """Get video duration using ffprobe"""
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1:noesc=1',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                logger.error(f"ffprobe error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error getting video duration: {str(e)}")
            return None
    
    def validate_youtube_url(self, url: str) -> bool:
        """Validate if URL is a valid YouTube URL"""
        try:
            valid_hosts = ["youtube.com", "youtu.be", "www.youtube.com"]
            return any(host in url for host in valid_hosts)
        except:
            return False
