"""Background job worker using RQ"""

import logging
from rq import Queue
from redis import Redis
from datetime import datetime
from app.core.config import get_settings
from app.utils.helpers import get_logger
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.reel import Job, JobStatus

logger = get_logger(__name__)
settings = get_settings()

# Connect to Redis
redis_conn = Redis.from_url(settings.rq_redis_url)
job_queue = Queue(connection=redis_conn)


def enqueue_job(job_type: str, user_id: int, video_id: int = None, **kwargs) -> str:
    """Enqueue a background job"""
    try:
        # Create job record in database
        db = SessionLocal()
        job = Job(
            user_id=user_id,
            video_id=video_id,
            job_type=job_type,
            status=JobStatus.PENDING,
        )
        db.add(job)
        db.commit()
        job_id_db = job.id
        db.close()
        
        logger.info(f"Enqueued job: {job_type} (db_id={job_id_db})")
        return str(job_id_db)
    
    except Exception as e:
        logger.error(f"Error enqueuing job: {str(e)}")
        return None


def update_job_status(job_id: int, status: JobStatus, progress: float = None, result: dict = None, error: str = None):
    """Update job status in database"""
    try:
        db = SessionLocal()
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if job:
            job.status = status
            if progress is not None:
                job.progress = progress
            if result:
                job.result = result
            if error:
                job.error_message = error
            job.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"Updated job {job_id} status: {status}")
        
        db.close()
    
    except Exception as e:
        logger.error(f"Error updating job status: {str(e)}")


# Background job functions

async def process_youtube_download_job(job_id: int, youtube_url: str, video_id: str):
    """Background job: Download YouTube video"""
    try:
        update_job_status(job_id, JobStatus.PROCESSING, 0)
        
        from app.services.youtube_service import YouTubeService
        yt_service = YouTubeService()
        
        success, result = await yt_service.download_video(youtube_url, video_id)
        
        if success:
            update_job_status(job_id, JobStatus.COMPLETED, 100, result)
        else:
            update_job_status(job_id, JobStatus.FAILED, 0, error="Download failed")
    
    except Exception as e:
        logger.error(f"Job {job_id} error: {str(e)}")
        update_job_status(job_id, JobStatus.FAILED, 0, error=str(e))


async def process_video_cutting_job(job_id: int, video_path: str, video_id: str, duration: float):
    """Background job: Cut video into chunks"""
    try:
        update_job_status(job_id, JobStatus.PROCESSING, 10)
        
        from app.services.video_service import VideoProcessingService
        video_service = VideoProcessingService()
        
        success, chunks = await video_service.cut_into_sequential_chunks(video_path, video_id, duration)
        
        if success:
            update_job_status(job_id, JobStatus.COMPLETED, 100, {'chunks': chunks})
        else:
            update_job_status(job_id, JobStatus.FAILED, 0, error="Cutting failed")
    
    except Exception as e:
        logger.error(f"Job {job_id} error: {str(e)}")
        update_job_status(job_id, JobStatus.FAILED, 0, error=str(e))


async def process_vertical_conversion_job(job_id: int, chunks: list, video_id: str):
    """Background job: Convert chunks to vertical reels"""
    try:
        update_job_status(job_id, JobStatus.PROCESSING, 20)
        
        from app.services.video_service import VideoProcessingService
        video_service = VideoProcessingService()
        
        success, reels = await video_service.convert_to_vertical_reels(chunks, video_id)
        
        if success:
            update_job_status(job_id, JobStatus.COMPLETED, 100, {'reels': reels})
        else:
            update_job_status(job_id, JobStatus.FAILED, 0, error="Vertical conversion failed")
    
    except Exception as e:
        logger.error(f"Job {job_id} error: {str(e)}")
        update_job_status(job_id, JobStatus.FAILED, 0, error=str(e))


async def process_ai_generation_job(job_id: int, reels: list, transcript: str = None):
    """Background job: Generate AI metadata for reels"""
    try:
        update_job_status(job_id, JobStatus.PROCESSING, 30)
        
        from app.services.gemini_service import GeminiAIService
        ai_service = GeminiAIService()
        
        reels_with_ai = []
        total = len(reels)
        
        for i, reel in enumerate(reels):
            metadata = await ai_service.generate_reel_metadata(
                transcript=transcript,
                duration=reel.get('duration'),
            )
            
            reel['metadata'] = metadata
            reels_with_ai.append(reel)
            
            progress = 30 + int((i + 1) / total * 50)  # 30-80%
            update_job_status(job_id, JobStatus.PROCESSING, progress)
        
        update_job_status(job_id, JobStatus.COMPLETED, 100, {'reels': reels_with_ai})
    
    except Exception as e:
        logger.error(f"Job {job_id} error: {str(e)}")
        update_job_status(job_id, JobStatus.FAILED, 0, error=str(e))


async def process_token_refresh_job(job_id: int, instagram_token_id: int):
    """Background job: Refresh Instagram long-lived access token"""
    try:
        update_job_status(job_id, JobStatus.PROCESSING, 20)
        
        from app.services.facebook_oauth_service import FacebookOAuthService
        from app.models.reel import InstagramToken
        
        facebook_service = FacebookOAuthService()
        db = SessionLocal()
        
        # Get the Instagram token
        token_record = db.query(InstagramToken).filter(
            InstagramToken.id == instagram_token_id
        ).first()
        
        if not token_record:
            logger.error(f"Instagram token {instagram_token_id} not found")
            update_job_status(job_id, JobStatus.FAILED, 0, error="Instagram token not found")
            return
        
        update_job_status(job_id, JobStatus.PROCESSING, 50)
        
        # Refresh the token
        refresh_response = await facebook_service.refresh_long_lived_token(
            token_record.long_lived_token
        )
        
        if not refresh_response["success"]:
            error_msg = f"Token refresh failed: {refresh_response.get('error')}"
            logger.error(error_msg)
            update_job_status(job_id, JobStatus.FAILED, 0, error=error_msg)
            db.close()
            return
        
        # Update the token
        new_token = refresh_response["new_token"]
        expires_at = refresh_response.get("expires_at")
        expires_in = refresh_response.get("expires_in")
        
        token_record.access_token = new_token
        token_record.long_lived_token = new_token
        token_record.expires_at = expires_at
        token_record.token_expires_in = expires_in
        token_record.last_refreshed_at = datetime.utcnow()
        token_record.refresh_count += 1
        token_record.is_valid = True
        
        db.commit()
        db.close()
        
        logger.info(f"Successfully refreshed token for user {token_record.user_id}, expires at {expires_at}")
        update_job_status(
            job_id,
            JobStatus.COMPLETED,
            100,
            {
                "success": True,
                "new_expires_at": expires_at,
                "instagram_user_id": token_record.ig_user_id,
                "username": token_record.instagram_username,
            }
        )
    
    except Exception as e:
        logger.error(f"Job {job_id} error during token refresh: {str(e)}")
        update_job_status(job_id, JobStatus.FAILED, 0, error=str(e))

