"""Social account connection endpoints - GRAVIXAI"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import InstagramSettings
from app.services.instagram_oauth_service import FacebookOAuthService
from app.core.config import get_settings
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api/social", tags=["social"])

oauth_service = FacebookOAuthService(
    app_id=settings.facebook_app_id,
    app_secret=settings.facebook_app_secret,
    redirect_uri=settings.facebook_redirect_uri
)


@router.get("/connect")
async def get_connect_url():
    """Get Facebook OAuth authorization URL"""
    state = str(uuid.uuid4())
    url = oauth_service.get_oauth_url(state=state)
    
    return {
        "authorization_url": url,
        "state": state
    }


@router.get("/facebook/callback")
async def facebook_callback(
    code: str = Query(...),
    db: Session = Depends(get_db)
):
    """Facebook OAuth callback endpoint"""
    try:
        # Step 1: Exchange code for short-lived token
        token_result = oauth_service.exchange_code_for_token(code)
        short_token = token_result.get("short_lived_token")
        user_id = token_result.get("user_id")
        
        if not short_token:
            logger.error("Failed to get short-lived token")
            return RedirectResponse(
                url="http://localhost:3000/settings/social-accounts?error=InvalidToken",
                status_code=302
            )
        
        # Step 2: Get long-lived token
        long_token_result = oauth_service.get_long_lived_token(short_token)
        long_token = long_token_result.get("long_lived_token")
        expires_at = long_token_result.get("expires_at")
        
        if not long_token:
            logger.error("Failed to get long-lived token")
            return RedirectResponse(
                url="http://localhost:3000/settings/social-accounts?error=TokenConversionFailed",
                status_code=302
            )
        
        # Step 3: Get Facebook pages
        pages = oauth_service.get_facebook_pages(long_token)
        
        if not pages:
            logger.error("No Facebook pages found")
            return RedirectResponse(
                url="http://localhost:3000/settings/social-accounts?error=NoPageFound",
                status_code=302
            )
        
        # Use first page
        page = pages[0]
        page_id = page.get("page_id")
        page_token = page.get("page_access_token", long_token)
        page_name = page.get("page_name", "Unknown")
        
        # Step 4: Get Instagram Business Account
        ig_result = oauth_service.get_instagram_account(page_id, page_token)
        ig_user_id = ig_result.get("ig_user_id")
        
        if not ig_user_id:
            logger.error("Instagram Business Account not found")
            return RedirectResponse(
                url="http://localhost:3000/settings/social-accounts?error=NoInstagramAccount",
                status_code=302
            )
        
        # Step 5: Save to database
        existing = db.query(InstagramSettings).filter_by(ig_user_id=ig_user_id).first()
        
        if existing:
            existing.long_lived_access_token = long_token
            existing.token_expires_at = expires_at
            existing.is_active = True
            existing.updated_at = datetime.utcnow()
            db.commit()
        else:
            instagram_settings = InstagramSettings(
                fb_page_id=page_id,
                fb_page_name=page_name,
                fb_user_id=user_id or "",
                ig_user_id=ig_user_id,
                long_lived_access_token=long_token,
                token_expires_at=expires_at,
                is_active=True
            )
            db.add(instagram_settings)
            db.commit()
        
        logger.info(f"✓ Instagram account connected: {ig_user_id}")
        
        # Redirect to success page
        return RedirectResponse(
            url=f"http://localhost:3000/settings/social-accounts?success=true&ig_id={ig_user_id}",
            status_code=302
        )
    
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        return RedirectResponse(
            url=f"http://localhost:3000/settings/social-accounts?error=CallbackError",
            status_code=302
        )


@router.get("/status")
async def get_social_status(db: Session = Depends(get_db)):
    """Get current Instagram connection status"""
    try:
        settings_record = db.query(InstagramSettings).filter_by(is_active=True).first()
        
        if not settings_record:
            return {
                "connected": False,
                "message": "No Instagram account connected"
            }
        
        is_token_valid = True
        if settings_record.token_expires_at and settings_record.token_expires_at < datetime.utcnow():
            is_token_valid = False
        
        return {
            "connected": True,
            "ig_user_id": settings_record.ig_user_id,
            "fb_page_name": settings_record.fb_page_name,
            "fb_page_id": settings_record.fb_page_id,
            "token_expires_at": settings_record.token_expires_at,
            "is_token_valid": is_token_valid
        }
    except Exception as e:
        logger.error(f"Failed to get social status: {str(e)}")
        return {
            "connected": False,
            "error": str(e)
        }


@router.post("/refresh-token")
async def refresh_token(db: Session = Depends(get_db)):
    """Refresh Instagram access token"""
    try:
        settings_record = db.query(InstagramSettings).filter_by(is_active=True).first()
        
        if not settings_record:
            raise HTTPException(status_code=404, detail="No Instagram account connected")
        
        refresh_result = oauth_service.refresh_long_lived_token(
            settings_record.long_lived_access_token
        )
        
        settings_record.long_lived_access_token = refresh_result.get("long_lived_token")
        settings_record.token_expires_at = refresh_result.get("expires_at")
        settings_record.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"✓ Token refreshed for {settings_record.ig_user_id}")
        
        return {
            "success": True,
            "message": "Token refreshed",
            "expires_at": refresh_result.get("expires_at")
        }
    
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/disconnect")
async def disconnect_instagram(db: Session = Depends(get_db)):
    """Disconnect Instagram account"""
    try:
        settings_record = db.query(InstagramSettings).filter_by(is_active=True).first()
        
        if not settings_record:
            raise HTTPException(status_code=404, detail="No Instagram account connected")
        
        ig_id = settings_record.ig_user_id
        settings_record.is_active = False
        settings_record.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"✓ Instagram account disconnected: {ig_id}")
        
        return {
            "success": True,
            "message": f"Instagram account {ig_id} disconnected"
        }
    
    except Exception as e:
        logger.error(f"Disconnect error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
