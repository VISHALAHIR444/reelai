"""Instagram integration routes placeholder"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/instagram", tags=["Instagram"])


@router.get("/auth-url")
async def get_instagram_auth_url():
    """Get Instagram OAuth URL - placeholder"""
    # TODO: Generate OAuth URL
    return {"message": "Get Instagram auth URL endpoint - backend implementation pending"}


@router.post("/callback")
async def instagram_callback(code: str, db: Session = Depends(get_db)):
    """Instagram OAuth callback - placeholder"""
    # TODO: Exchange code for token
    # TODO: Store token in database
    return {"message": "Instagram callback endpoint - backend implementation pending"}


@router.get("/disconnect")
async def disconnect_instagram(db: Session = Depends(get_db)):
    """Disconnect Instagram account - placeholder"""
    # TODO: Remove Instagram token from database
    return {"message": "Disconnect Instagram endpoint - backend implementation pending"}
