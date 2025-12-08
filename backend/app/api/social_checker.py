"""Instagram Connect Checker endpoint"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.instagram_checker import InstagramChecker, GraphAPIError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/social", tags=["social-checker"])
checker = InstagramChecker()


@router.get("/check")
async def check_social_connection(db: Session = Depends(get_db)):
    """Return real-time status of Facebook + Instagram connection."""
    try:
        result = checker.check_connection(db)
        return result
    except GraphAPIError as exc:
        logger.error(f"Graph API error: {exc.message}")
        raise HTTPException(status_code=400, detail=exc.message)
    except Exception as exc:
        logger.error(f"Social check failed: {exc}")
        raise HTTPException(status_code=500, detail="social_check_failed")
