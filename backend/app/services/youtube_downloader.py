import os
import subprocess
import json
import logging
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class YouTubeDownloader:
    """Download videos from YouTube with transcripts"""
    
    def __init__(self, yt_dlp_path: str = "yt-dlp", videos_dir: str = "./videos"):
        self.yt_dlp_path = yt_dlp_path
        self.videos_dir = videos_dir
        os.makedirs(videos_dir, exist_ok=True)
    
    def extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return ""
    
    def download_video(self, url: str) -> Tuple[str, Dict]:
        """Download video and metadata"""
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL: {url}")
        
        video_dir = os.path.join(self.videos_dir, video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        try:
            # Download video with metadata
            cmd = [
                self.yt_dlp_path,
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "-o", os.path.join(video_dir, "video.mp4"),
                "--write-info-json",
                "--write-auto-sub",
                "--sub-lang", "en",
                "--skip-download" if os.path.exists(os.path.join(video_dir, "video.mp4")) else "",
                url
            ]
            cmd = [c for c in cmd if c]  # Remove empty strings
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                logger.error(f"yt-dlp error: {result.stderr}")
                raise Exception(f"Download failed: {result.stderr}")
            
            # Read metadata
            info_file = os.path.join(video_dir, "video.info.json")
            metadata = {}
            if os.path.exists(info_file):
                with open(info_file, 'r') as f:
                    metadata = json.load(f)
            
            video_path = os.path.join(video_dir, "video.mp4")
            
            return video_path, {
                "title": metadata.get("title", ""),
                "description": metadata.get("description", ""),
                "thumbnail_url": metadata.get("thumbnail", ""),
                "duration": metadata.get("duration", 0),
                "video_id": video_id,
                "video_dir": video_dir
            }
        
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            raise
    
    def download_audio(self, url: str, video_dir: str) -> str:
        """Download audio for speech-to-text"""
        try:
            audio_path = os.path.join(video_dir, "audio.m4a")
            
            cmd = [
                self.yt_dlp_path,
                "-f", "bestaudio[ext=m4a]/bestaudio",
                "-o", audio_path,
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                raise Exception(f"Audio download failed: {result.stderr}")
            
            return audio_path
        
        except Exception as e:
            logger.error(f"Audio download error: {str(e)}")
            raise


class TranscriptExtractor:
    """Extract transcripts from videos"""
    
    def __init__(self, videos_dir: str = "./videos"):
        self.videos_dir = videos_dir
    
    def get_auto_transcript(self, video_dir: str) -> str:
        """Get auto-generated transcript from yt-dlp"""
        try:
            # Look for .vtt subtitle file
            vtt_files = []
            for root, dirs, files in os.walk(video_dir):
                for f in files:
                    if f.endswith('.vtt'):
                        vtt_files.append(os.path.join(root, f))
            
            if vtt_files:
                transcript = self._parse_vtt(vtt_files[0])
                if transcript.strip():
                    return transcript
            
            return ""
        
        except Exception as e:
            logger.error(f"Transcript extraction error: {str(e)}")
            return ""
    
    def _parse_vtt(self, vtt_file: str) -> str:
        """Parse WebVTT subtitle file"""
        try:
            with open(vtt_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            transcript = []
            for line in lines:
                line = line.strip()
                # Skip VTT header, timing lines, and empty lines
                if line and not line.startswith("WEBVTT") and "-->" not in line:
                    transcript.append(line)
            
            return " ".join(transcript)
        
        except Exception as e:
            logger.error(f"VTT parsing error: {str(e)}")
            return ""
    
    def get_stt_fallback(self, audio_path: str) -> str:
        """Use Google Speech-to-Text as fallback (not implemented - returns placeholder)"""
        # This would require Google Cloud credentials
        # For now, return empty to indicate fallback not available
        logger.warning("STT fallback not configured - returning empty transcript")
        return ""
