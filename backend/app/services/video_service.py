"""Video cutting and vertical reel conversion service"""

import subprocess
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from app.core.config import get_settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)
settings = get_settings()


class VideoProcessingService:
    """Service for cutting videos into chunks and converting to vertical format"""
    
    def __init__(self):
        self.storage_base = settings.storage_base_path
        self.ffmpeg_path = settings.ffmpeg_path
        self.ffprobe_path = settings.ffprobe_path
        self.chunk_duration = settings.chunk_duration  # 35 seconds
        self.reel_width = settings.reel_width  # 1080
        self.reel_height = settings.reel_height  # 1920
    
    async def cut_into_sequential_chunks(self, video_path: str, video_id: str, total_duration: float) -> Tuple[bool, List[Dict]]:
        """
        Cut video into 35-second sequential chunks
        
        Example: 0-35s, 35-70s, 70-105s
        
        Returns: (success, chunks_list)
        chunks_list: [{"chunk_number": 1, "start": 0, "end": 35, "file_path": "..."},  ...]
        """
        try:
            chunks_dir = Path(self.storage_base) / video_id / "chunks"
            chunks_dir.mkdir(parents=True, exist_ok=True)
            
            chunks_list = []
            chunk_number = 1
            current_time = 0
            
            logger.info(f"Starting video cutting. Total duration: {total_duration}s, Chunk size: {self.chunk_duration}s")
            
            while current_time < total_duration:
                start_time = current_time
                end_time = min(current_time + self.chunk_duration, total_duration)
                duration = end_time - start_time
                
                chunk_path = chunks_dir / f"chunk_{chunk_number:03d}.mp4"
                
                logger.info(f"Cutting chunk {chunk_number}: {start_time}s - {end_time}s")
                
                # Cut video using FFmpeg
                success = await self._cut_video(video_path, str(chunk_path), start_time, duration)
                
                if success:
                    file_size = os.path.getsize(chunk_path)
                    chunks_list.append({
                        'chunk_number': chunk_number,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': duration,
                        'file_path': str(chunk_path),
                        'file_size': file_size,
                    })
                    logger.info(f"Chunk {chunk_number} created: {duration}s, {file_size} bytes")
                else:
                    logger.error(f"Failed to cut chunk {chunk_number}")
                    return False, []
                
                current_time = end_time
                chunk_number += 1
            
            logger.info(f"Video cutting complete. Created {len(chunks_list)} chunks")
            return True, chunks_list
        
        except Exception as e:
            logger.error(f"Error cutting video into chunks: {str(e)}", exc_info=True)
            return False, []
    
    async def _cut_video(self, input_path: str, output_path: str, start_time: float, duration: float) -> bool:
        """Cut video segment using FFmpeg"""
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:v', 'libx264',  # Video codec
                '-c:a', 'aac',      # Audio codec
                '-q:v', '6',        # Quality (1-51, lower is better)
                '-preset', 'fast',  # Speed (ultrafast, fast, medium, slow)
                str(output_path),
                '-y'  # Overwrite output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"FFmpeg cut error: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error in _cut_video: {str(e)}")
            return False
    
    async def convert_to_vertical_reels(self, chunks_list: List[Dict], video_id: str) -> Tuple[bool, List[Dict]]:
        """
        Convert chunks to vertical format (1080x1920)
        
        Creates canvas with black bars on top/bottom to center original video
        
        Returns: (success, reels_list)
        reels_list: [{"reel_number": 1, "file_path": "...", ...}, ...]
        """
        try:
            reels_dir = Path(self.storage_base) / video_id / "reels"
            reels_dir.mkdir(parents=True, exist_ok=True)
            
            reels_list = []
            
            logger.info(f"Starting vertical reel conversion for {len(chunks_list)} chunks")
            
            for chunk in chunks_list:
                chunk_number = chunk['chunk_number']
                chunk_path = chunk['file_path']
                reel_number = chunk_number
                reel_path = reels_dir / f"reel_{reel_number:03d}.mp4"
                
                logger.info(f"Converting chunk {chunk_number} to vertical reel {reel_number}")
                
                # Convert to vertical format
                success = await self._convert_to_vertical(chunk_path, str(reel_path))
                
                if success:
                    file_size = os.path.getsize(reel_path)
                    reels_list.append({
                        'reel_number': reel_number,
                        'chunk_number': chunk_number,
                        'file_path': str(reel_path),
                        'file_size': file_size,
                        'duration': chunk['duration'],
                        'width': self.reel_width,
                        'height': self.reel_height,
                    })
                    logger.info(f"Reel {reel_number} created: {file_size} bytes")
                else:
                    logger.error(f"Failed to convert chunk {chunk_number} to vertical reel")
                    return False, []
            
            logger.info(f"Vertical reel conversion complete. Created {len(reels_list)} reels")
            return True, reels_list
        
        except Exception as e:
            logger.error(f"Error converting to vertical reels: {str(e)}", exc_info=True)
            return False, []
    
    async def _convert_to_vertical(self, input_path: str, output_path: str) -> bool:
        """
        Convert video to 1080x1920 vertical format
        
        Strategy:
        1. Get input video dimensions
        2. Scale to fit within 1080 width while maintaining aspect ratio
        3. Create 1080x1920 canvas with black bars
        4. Overlay scaled video centered
        """
        try:
            # Get input video dimensions
            dimensions = await self._get_video_dimensions(input_path)
            if not dimensions:
                logger.error(f"Could not get video dimensions: {input_path}")
                return False
            
            width, height = dimensions
            logger.info(f"Input video dimensions: {width}x{height}")
            
            # Calculate scaling to fit 1080x1920
            # If video is wider, scale to 1080 width
            if width / height > self.reel_width / self.reel_height:
                # Video is too wide, scale by width
                scale_width = self.reel_width
                scale_height = int(self.reel_width * height / width)
            else:
                # Video is too tall, scale by height
                scale_height = self.reel_height
                scale_width = int(self.reel_height * width / height)
            
            logger.info(f"Scaling to: {scale_width}x{scale_height}")
            
            # FFmpeg filter to scale and add black bars
            # Create canvas, scale input, and overlay centered
            filter_complex = (
                f"scale={scale_width}:{scale_height},"
                f"pad={self.reel_width}:{self.reel_height}:"
                f"(ow-iw)/2:(oh-ih)/2:black"
            )
            
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-vf', filter_complex,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-q:v', '6',
                '-preset', 'fast',
                str(output_path),
                '-y'
            ]
            
            logger.info(f"FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"Vertical reel created: {output_path}")
                return True
            else:
                logger.error(f"FFmpeg vertical conversion error: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error in _convert_to_vertical: {str(e)}")
            return False
    
    async def _get_video_dimensions(self, video_path: str) -> Optional[Tuple[int, int]]:
        """Get video dimensions (width, height) using ffprobe"""
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                width, height = map(int, result.stdout.strip().split(','))
                return (width, height)
            else:
                logger.error(f"ffprobe error: {result.stderr}")
                return None
        
        except Exception as e:
            logger.error(f"Error getting video dimensions: {str(e)}")
            return None
