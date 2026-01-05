"""Reels routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Reel, Video
from app.schemas import ReelResponse

router = APIRouter(prefix="/api/reels", tags=["reels"])


@router.get("/", response_model=list[ReelResponse])
async def list_all_reels(
    db: Session = Depends(get_db),
    skip: int = Query(0),
    limit: int = Query(50),
    status: str = Query(None)
):
    """List all reels with optional status filter"""
    query = db.query(Reel)
    
    if status:
        query = query.filter_by(publish_status=status)
    
    reels = query.offset(skip).limit(limit).all()
    
    return reels


@router.get("/pending-publish/count")
async def get_pending_publish_count(db: Session = Depends(get_db)):
    """Get count of reels pending publish"""
    count = db.query(Reel).filter_by(publish_status="pending").count()
    
    return {
        "pending_count": count
    }


@router.get("/video/{video_id}", response_model=list[ReelResponse])
async def get_video_reels(
    video_id: str,
    db: Session = Depends(get_db),
    skip: int = Query(0),
    limit: int = Query(50)
):
    """Get all reels for a video"""
    video = db.query(Video).filter_by(id=video_id).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    reels = db.query(Reel).filter_by(video_id=video_id).offset(skip).limit(limit).all()
    
    return reels


@router.get("/{reel_id}/details", response_model=ReelResponse)
async def get_reel_details(
    reel_id: str,
    db: Session = Depends(get_db)
):
    """Get individual reel details"""
    reel = db.query(Reel).filter_by(id=reel_id).first()
    
    if not reel:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    return reel


@router.post("/{reel_id}/publish")
async def publish_reel(
    reel_id: str,
    db: Session = Depends(get_db)
):
    """Trigger reel publishing to Instagram"""
    reel = db.query(Reel).filter_by(id=reel_id).first()
    
    if not reel:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    if reel.publish_status == "published":
        raise HTTPException(status_code=400, detail="Reel already published")
    
    return {
        "reel_id": reel_id,
        "status": "publishing",
        "message": "Reel publish job queued"
    }


@router.post("/job/{job_id}/upload-all-instagram")
async def upload_all_reels_to_instagram(job_id: int, db: Session = Depends(get_db)):
    """Upload all reels from a job to Instagram - placeholder"""
    # TODO: Trigger bulk Instagram upload task
    return {"message": "Upload all reels to Instagram endpoint - backend implementation pending"}
