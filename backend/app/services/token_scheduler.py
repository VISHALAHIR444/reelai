"""Scheduled token refresh tasks"""

import asyncio
import logging
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.reel import InstagramToken, Job, JobStatus
from app.services.facebook_oauth_service import FacebookOAuthService
from app.workers.rq_worker import enqueue_job

logger = logging.getLogger(__name__)


async def schedule_token_refresh():
    """
    Check all tokens and schedule refresh for those expiring soon.
    This should be run every day or can be triggered manually.
    """
    try:
        db = SessionLocal()
        
        # Find tokens expiring within 10 days
        threshold = datetime.utcnow() + timedelta(days=10)
        tokens_to_refresh = db.query(InstagramToken).filter(
            InstagramToken.expires_at <= threshold,
            InstagramToken.is_connected == True,
        ).all()
        
        logger.info(f"Found {len(tokens_to_refresh)} tokens to refresh")
        
        facebook_service = FacebookOAuthService()
        
        for token in tokens_to_refresh:
            try:
                # Check if token is still valid
                validation = await facebook_service.validate_token(token.access_token)
                
                if not validation.get("success"):
                    logger.warning(f"Token validation failed for user {token.user_id}")
                    continue
                
                if not validation.get("is_valid"):
                    logger.warning(f"Token is invalid for user {token.user_id}")
                    token.is_valid = False
                    db.commit()
                    continue
                
                # Schedule refresh job
                job_id = enqueue_job(
                    job_type="token_refresh",
                    user_id=token.user_id,
                )
                
                if job_id:
                    logger.info(f"Scheduled token refresh job for user {token.user_id}")
                else:
                    logger.error(f"Failed to schedule token refresh for user {token.user_id}")
            
            except Exception as e:
                logger.error(f"Error processing token for user {token.user_id}: {str(e)}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Error in schedule_token_refresh: {str(e)}")


async def auto_refresh_expiring_tokens():
    """
    Automatically refresh tokens that are expiring soon.
    Run this as a background task.
    """
    try:
        db = SessionLocal()
        
        # Find tokens expiring within 3 days
        threshold = datetime.utcnow() + timedelta(days=3)
        tokens_expiring = db.query(InstagramToken).filter(
            InstagramToken.expires_at <= threshold,
            InstagramToken.expires_at > datetime.utcnow(),
            InstagramToken.is_connected == True,
        ).all()
        
        logger.info(f"Auto-refreshing {len(tokens_expiring)} tokens")
        
        facebook_service = FacebookOAuthService()
        
        for token in tokens_expiring:
            try:
                refresh_response = await facebook_service.refresh_long_lived_token(
                    token.long_lived_token
                )
                
                if not refresh_response["success"]:
                    logger.error(f"Failed to auto-refresh token for user {token.user_id}")
                    continue
                
                # Update token
                new_token = refresh_response["new_token"]
                expires_at = refresh_response.get("expires_at")
                expires_in = refresh_response.get("expires_in")
                
                token.access_token = new_token
                token.long_lived_token = new_token
                token.expires_at = expires_at
                token.token_expires_in = expires_in
                token.last_refreshed_at = datetime.utcnow()
                token.refresh_count += 1
                token.is_valid = True
                
                db.commit()
                logger.info(f"Auto-refreshed token for user {token.user_id}, new expiry: {expires_at}")
                
            except Exception as e:
                logger.error(f"Error auto-refreshing token for user {token.user_id}: {str(e)}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Error in auto_refresh_expiring_tokens: {str(e)}")


async def cleanup_invalid_tokens():
    """
    Cleanup and invalidate tokens that have expired.
    """
    try:
        db = SessionLocal()
        
        # Find expired tokens
        expired_tokens = db.query(InstagramToken).filter(
            InstagramToken.expires_at <= datetime.utcnow()
        ).all()
        
        logger.info(f"Found {len(expired_tokens)} expired tokens")
        
        for token in expired_tokens:
            token.is_valid = False
            token.is_connected = False
            db.commit()
            logger.info(f"Marked token as invalid for user {token.user_id}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Error in cleanup_invalid_tokens: {str(e)}")


if __name__ == "__main__":
    # Test the scheduler
    import asyncio
    asyncio.run(schedule_token_refresh())
