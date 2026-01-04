from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Video, Reel
from app.schemas import VideoCreate, VideoResponse, VideoDetailResponse, SocialStatusResponse
from app.services.youtube_downloader import YouTubeDownloader
from app.core.config import get_settings
import uuid
from datetime import datetime

settings = get_settings()
router = APIRouter(prefix="/api/video", tags=["video"])


@router.post("/youtube", response_model=VideoResponse)
async def upload_youtube_video(
    request: VideoCreate,
    db: Session = Depends(get_db)
):
    """Upload YouTube video for processing"""
    try:
        # Validate URL
        downloader = YouTubeDownloader(
            yt_dlp_path=settings.yt_dlp_path,
            videos_dir=settings.videos_dir
        )
        
        video_id = downloader.extract_video_id(request.youtube_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Check if already exists
        existing = db.query(Video).filter_by(youtube_video_id=video_id).first()
        if existing:
            return existing
        
        # Create video record
        video = Video(
            id=str(uuid.uuid4()),
            youtube_url=request.youtube_url,
            youtube_video_id=video_id,
            title="Processing...",
            status="pending",
            created_at=datetime.utcnow()
        )
        
        db.add(video)
        db.commit()
        db.refresh(video)
        
        return video
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}", response_model=VideoDetailResponse)
async def get_video(
    video_id: str,
    db: Session = Depends(get_db)
):
    """Get video details with chunks and reels"""
    video = db.query(Video).filter_by(id=video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video


@router.get("/", response_model=list[VideoResponse])
async def list_videos(
    db: Session = Depends(get_db),
    skip: int = Query(0),
    limit: int = Query(20)
):
    """List all videos"""
    videos = db.query(Video).offset(skip).limit(limit).all()
    return videos


@router.post("/{video_id}/process")
async def process_video(
    video_id: str,
    db: Session = Depends(get_db)
):
    """Trigger video processing pipeline"""
    video = db.query(Video).filter_by(id=video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Update status to processing
    video.status = "processing"
    db.commit()
    
    # Start background processing
    import threading
    import subprocess
    import json
    from app.core.database import SessionLocal
    
    def process_in_background(vid_id: str, url: str):
        db_local = SessionLocal()
        try:
            video_local = db_local.query(Video).filter_by(id=vid_id).first()
            if not video_local:
                return
            
            # Fetch metadata using yt-dlp
            result = subprocess.run(
                ["yt-dlp", "--dump-json", url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                video_local.title = metadata.get("title", "Unknown")
                video_local.description = metadata.get("description", "")[:500] if metadata.get("description") else None
                video_local.duration = int(metadata.get("duration", 0)) if metadata.get("duration") else None
                video_local.thumbnail_url = metadata.get("thumbnail")
                video_local.status = "completed"
            else:
                video_local.status = "failed"
                video_local.error_message = "Failed to fetch video metadata"
            
            db_local.commit()
        except Exception as e:
            if video_local:
                video_local.status = "failed"
                video_local.error_message = str(e)
                db_local.commit()
        finally:
            db_local.close()
    
    thread = threading.Thread(target=process_in_background, args=(video_id, video.youtube_url))
    thread.start()
    
    return {
        "video_id": video_id,
        "status": "processing",
        "message": "Video processing started"
    }


@router.get("/{video_id}/status")
async def get_video_status(
    video_id: str,
    db: Session = Depends(get_db)
):
    """Get video processing status"""
    video = db.query(Video).filter_by(id=video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    reels_count = db.query(Reel).filter_by(video_id=video_id).count()
    
    return {
        "video_id": video_id,
        "status": video.status,
        "title": video.title,
        "duration": video.duration,
        "reels_created": reels_count,
        "created_at": video.created_at,
        "updated_at": video.updated_at
    }
