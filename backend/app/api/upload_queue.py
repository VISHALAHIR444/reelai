"""Upload Queue API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.models import UploadQueue, InstagramAccount, Reel
from app.schemas.upload_queue import (
    UploadQueueCreate,
    UploadQueueUpdate,
    UploadQueueResponse
)

router = APIRouter(prefix="/upload-queue", tags=["Upload Queue"])


@router.post("", response_model=UploadQueueResponse, status_code=status.HTTP_201_CREATED)
def add_to_upload_queue(
    queue_data: UploadQueueCreate,
    db: Session = Depends(get_db)
):
    """Add reel to upload queue with selected Instagram account"""
    
    # Validate Instagram account exists and is active
    account = db.query(InstagramAccount).filter(
        and_(
            InstagramAccount.id == queue_data.instagram_account_id,
            InstagramAccount.is_deleted == False
        )
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    if account.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot schedule reels to inactive Instagram account"
        )
    
    # Validate reel exists
    reel = db.query(Reel).filter(Reel.id == queue_data.reel_id).first()
    if not reel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reel not found"
        )
    
    # Check if already in queue
    existing = db.query(UploadQueue).filter(
        and_(
            UploadQueue.reel_id == queue_data.reel_id,
            UploadQueue.instagram_account_id == queue_data.instagram_account_id
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reel already in upload queue for this account"
        )
    
    # Add to queue
    queue_item = UploadQueue(
        reel_id=queue_data.reel_id,
        instagram_account_id=queue_data.instagram_account_id,
        upload_status="pending"
    )
    
    db.add(queue_item)
    db.commit()
    db.refresh(queue_item)
    
    # Prepare response with nested data
    response = {
        **queue_item.__dict__,
        "instagram_account": {
            "id": account.id,
            "username": account.username,
            "label": account.label
        },
        "reel": {
            "id": reel.id,
            "title": reel.title,
            "duration": reel.duration,
            "file_path": reel.file_path
        }
    }
    
    return response


@router.get("", response_model=List[UploadQueueResponse])
def list_upload_queue(
    status_filter: str = None,
    instagram_account_id: int = None,
    db: Session = Depends(get_db)
):
    """List upload queue"""
    
    query = db.query(UploadQueue)
    
    if status_filter in ["pending", "uploaded", "failed"]:
        query = query.filter(UploadQueue.upload_status == status_filter)
    
    if instagram_account_id:
        query = query.filter(UploadQueue.instagram_account_id == instagram_account_id)
    
    queue_items = query.order_by(UploadQueue.created_at.desc()).all()
    
    # Prepare responses with nested data
    responses = []
    for item in queue_items:
        account = db.query(InstagramAccount).filter(InstagramAccount.id == item.instagram_account_id).first()
        reel = db.query(Reel).filter(Reel.id == item.reel_id).first()
        
        responses.append({
            **item.__dict__,
            "instagram_account": {
                "id": account.id if account else None,
                "username": account.username if account else None,
                "label": account.label if account else None
            },
            "reel": {
                "id": reel.id if reel else None,
                "title": reel.title if reel else None,
                "duration": reel.duration if reel else None,
                "file_path": reel.file_path if reel else None
            }
        })
    
    return responses


@router.put("/{queue_id}", response_model=UploadQueueResponse)
def update_upload_status(
    queue_id: int,
    status_data: UploadQueueUpdate,
    db: Session = Depends(get_db)
):
    """Update upload status (manually mark as uploaded/failed)"""
    
    queue_item = db.query(UploadQueue).filter(UploadQueue.id == queue_id).first()
    
    if not queue_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue item not found"
        )
    
    # Update status
    queue_item.upload_status = status_data.upload_status
    
    if status_data.upload_error:
        queue_item.upload_error = status_data.upload_error
    
    if status_data.instagram_post_id:
        queue_item.instagram_post_id = status_data.instagram_post_id
    
    if status_data.instagram_url:
        queue_item.instagram_url = status_data.instagram_url
    
    if status_data.upload_status == "uploaded":
        queue_item.uploaded_at = datetime.utcnow()
        
        # Update last_used_at for Instagram account
        account = db.query(InstagramAccount).filter(
            InstagramAccount.id == queue_item.instagram_account_id
        ).first()
        if account:
            account.last_used_at = datetime.utcnow()
    
    queue_item.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(queue_item)
    
    # Prepare response
    account = db.query(InstagramAccount).filter(InstagramAccount.id == queue_item.instagram_account_id).first()
    reel = db.query(Reel).filter(Reel.id == queue_item.reel_id).first()
    
    response = {
        **queue_item.__dict__,
        "instagram_account": {
            "id": account.id if account else None,
            "username": account.username if account else None,
            "label": account.label if account else None
        },
        "reel": {
            "id": reel.id if reel else None,
            "title": reel.title if reel else None,
            "duration": reel.duration if reel else None,
            "file_path": reel.file_path if reel else None
        }
    }
    
    return response


@router.delete("/{queue_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_queue(
    queue_id: int,
    db: Session = Depends(get_db)
):
    """Remove item from upload queue"""
    
    queue_item = db.query(UploadQueue).filter(UploadQueue.id == queue_id).first()
    
    if not queue_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue item not found"
        )
    
    db.delete(queue_item)
    db.commit()
    
    return None
