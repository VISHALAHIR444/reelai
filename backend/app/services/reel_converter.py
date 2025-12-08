import os
import subprocess
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class ReelConverter:
    """Convert video chunks to vertical Instagram Reels (1080x1920)"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg", reel_width: int = 1080, reel_height: int = 1920):
        self.ffmpeg_path = ffmpeg_path
        self.reel_width = reel_width
        self.reel_height = reel_height
    
    def convert_to_vertical(self, chunk_path: str, output_path: str) -> Tuple[str, int]:
        """
        Convert chunk to 1080x1920 with black borders (letterbox format)
        Input: 16:9 video chunk
        Output: 1080x1920 with centered content and black top/bottom borders
        
        Returns: (output_path, duration_seconds)
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Calculate padding for 16:9 content in 1080x1920
            # Original aspect: 16:9 = 1.777...
            # Target aspect: 1080:1920 = 0.5625 (9:16 portrait)
            
            # Fit 16:9 inside 1080x1920:
            # Option 1: Width 1080, height = 1080 * 9/16 = 607.5
            # This leaves black bars on top/bottom
            
            video_height = int(1080 * 9 / 16)
            pad_height = (1920 - video_height) // 2
            
            # FFmpeg filter to scale and pad
            # scale=1080:-1: Scale to 1080 width, auto height maintaining aspect
            # pad=1080:1920:(ow-iw)/2:(oh-ih)/2: Pad to 1080x1920, center content
            
            filter_complex = f"scale={self.reel_width}:-1,pad={self.reel_width}:{self.reel_height}:(ow-iw)/2:(oh-ih)/2:color=black"
            
            cmd = [
                self.ffmpeg_path,
                "-i", chunk_path,
                "-vf", filter_complex,
                "-c:v", "libx264",  # H.264 codec
                "-preset", "medium",  # medium speed/quality trade-off
                "-crf", "23",  # Quality (0-51, lower is better, 23 is default)
                "-c:a", "aac",  # Audio codec
                "-b:a", "128k",  # Audio bitrate
                "-y",  # Overwrite output
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                logger.error(f"Conversion error: {result.stderr}")
                raise Exception(f"Failed to convert to vertical: {result.stderr}")
            
            # Get duration of output
            duration = self._get_duration(output_path)
            
            logger.info(f"Converted chunk to reel: {output_path} ({duration}s)")
            return output_path, int(duration)
        
        except Exception as e:
            logger.error(f"Reel conversion error: {str(e)}")
            raise
    
    def _get_duration(self, video_path: str) -> float:
        """Get video duration in seconds"""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return float(result.stdout.strip())
            return 0.0
        
        except:
            return 0.0
