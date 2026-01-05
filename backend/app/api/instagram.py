"""Instagram Account Management API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List
from app.db.database import get_db
from app.models.instagram_account import InstagramAccount, AccountStatus
from app.models.reel_schedule import ReelSchedule, ScheduleStatus
from app.schemas.instagram_account import (
    InstagramAccountCreate,
    InstagramAccountUpdate,
    InstagramAccountStatusUpdate,
    InstagramAccountResponse,
    InstagramAccountListResponse,
)
from app.services.instagram_verifier import InstagramVerifier

router = APIRouter(prefix="/instagram/accounts", tags=["Instagram Accounts"])


@router.post("", response_model=InstagramAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_instagram_account(
    account_data: InstagramAccountCreate,
    db: Session = Depends(get_db),
):
    """Create new Instagram account"""
    
    # Check duplicate username
    existing = db.query(InstagramAccount).filter(
        InstagramAccount.username == account_data.username
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Instagram account '{account_data.username}' already exists"
        )
    
    # TODO: Get user_id from auth - hardcoded for now
    user_id = 1
    
    account = InstagramAccount(
        user_id=user_id,
        username=account_data.username,
        label=account_data.label,
        status=AccountStatus.PENDING_VERIFICATION,
        verification_attempts=0,
        verified_by_post=False,
    )
    
    db.add(account)
    db.commit()
    db.refresh(account)
    
    return account


@router.post("/{account_id}/verify", response_model=InstagramAccountResponse)
async def verify_instagram_account(
    account_id: int,
    ig_user_id: str,  # Instagram business account ID
    access_token: str,  # Valid Instagram access token
    db: Session = Depends(get_db),
):
    """
    Verify Instagram account by publishing test image post.
    
    This endpoint:
    1. Publishes a test image post to Instagram
    2. If successful, marks account as CONNECTED
    3. If failed, marks as VERIFICATION_FAILED with error details
    
    Required params:
    - ig_user_id: Instagram business account ID
    - access_token: Valid Instagram Graph API access token
    """
    
    # Get account
    account = db.query(InstagramAccount).filter(
        InstagramAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account {account_id} not found"
        )
    
    # Initialize verifier
    verifier = InstagramVerifier()
    
    # Check if verification is allowed
    can_verify, message = verifier.can_retry_verification(account)
    if not can_verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Perform verification
    success, result_message = await verifier.verify_account(
        account=account,
        ig_user_id=ig_user_id,
        access_token=access_token,
        db=db
    )
    
    # Refresh to get updated data
    db.refresh(account)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result_message
        )
    
    return account


@router.get("", response_model=InstagramAccountListResponse)
async def get_instagram_accounts(
    status_filter: AccountStatus = None,
    db: Session = Depends(get_db),
):
    """Get all Instagram accounts"""
    
    # TODO: Filter by user_id from auth
    query = db.query(InstagramAccount)
    
    if status_filter:
        query = query.filter(InstagramAccount.status == status_filter)
    
    accounts = query.order_by(InstagramAccount.created_at.desc()).all()
    
    return InstagramAccountListResponse(
        accounts=accounts,
        total=len(accounts)
    )


@router.get("/{account_id}", response_model=InstagramAccountResponse)
async def get_instagram_account(
    account_id: int,
    db: Session = Depends(get_db),
):
    """Get single Instagram account"""
    
    account = db.query(InstagramAccount).filter(
        InstagramAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account {account_id} not found"
        )
    
    return account


@router.put("/{account_id}", response_model=InstagramAccountResponse)
async def update_instagram_account(
    account_id: int,
    account_data: InstagramAccountUpdate,
    db: Session = Depends(get_db),
):
    """Update Instagram account"""
    
    account = db.query(InstagramAccount).filter(
        InstagramAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account {account_id} not found"
        )
    
    if account_data.label is not None:
        account.label = account_data.label
    
    db.commit()
    db.refresh(account)
    
    return account


@router.patch("/{account_id}/status", response_model=InstagramAccountResponse)
async def update_account_status(
    account_id: int,
    status_data: InstagramAccountStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update account status"""
    
    account = db.query(InstagramAccount).filter(
        InstagramAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account {account_id} not found"
        )
    
    account.status = status_data.status
    db.commit()
    db.refresh(account)
    
    return account


@router.delete("/{account_id}", status_code=status.HTTP_200_OK)
async def delete_instagram_account(
    account_id: int,
    db: Session = Depends(get_db),
):
    """Soft delete Instagram account"""
    
    account = db.query(InstagramAccount).filter(
        InstagramAccount.id == account_id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account {account_id} not found"
        )
    
    # Check for active schedules
    active_schedules = db.query(ReelSchedule).filter(
        and_(
            ReelSchedule.instagram_account_id == account_id,
            ReelSchedule.status.in_([
                ScheduleStatus.SCHEDULED,
                ScheduleStatus.READY_FOR_UPLOAD
            ])
        )
    ).count()
    
    if active_schedules > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete account with {active_schedules} active schedules. Cancel or complete them first."
        )
    
    # Soft delete
    account.status = AccountStatus.INACTIVE
    db.commit()
    
    return {
        "message": f"Instagram account '{account.username}' deleted successfully",
        "account_id": account_id
    }
