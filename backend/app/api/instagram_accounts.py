"""Instagram Account Management API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.models.instagram_account import InstagramAccount
from app.schemas.instagram_account import (
    InstagramAccountCreate,
    InstagramAccountUpdate,
    InstagramAccountResponse,
    InstagramAccountListResponse
)

router = APIRouter(prefix="/instagram/accounts", tags=["Instagram Accounts"])


@router.post("", response_model=InstagramAccountResponse, status_code=status.HTTP_201_CREATED)
def create_instagram_account(
    account_data: InstagramAccountCreate,
    db: Session = Depends(get_db)
):
    """Add new Instagram account"""
    
    # Check if username already exists
    existing = db.query(InstagramAccount).filter(
        and_(
            InstagramAccount.username == account_data.username,
            InstagramAccount.is_deleted == False
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Instagram account with username '{account_data.username}' already exists"
        )
    
    # Create new account
    account = InstagramAccount(
        username=account_data.username,
        label=account_data.label,
        status=account_data.status,
        automation_enabled=False
    )
    
    db.add(account)
    db.commit()
    db.refresh(account)
    
    return account


@router.get("", response_model=InstagramAccountListResponse)
def list_instagram_accounts(
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """List all Instagram accounts"""
    
    query = db.query(InstagramAccount).filter(InstagramAccount.is_deleted == False)
    
    if status_filter in ["active", "inactive"]:
        query = query.filter(InstagramAccount.status == status_filter)
    
    accounts = query.order_by(InstagramAccount.created_at.desc()).all()
    
    total = len(accounts)
    active_count = sum(1 for a in accounts if a.status == "active")
    inactive_count = sum(1 for a in accounts if a.status == "inactive")
    
    return {
        "accounts": accounts,
        "total": total,
        "active_count": active_count,
        "inactive_count": inactive_count
    }


@router.get("/{account_id}", response_model=InstagramAccountResponse)
def get_instagram_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """Get Instagram account details"""
    
    account = db.query(InstagramAccount).filter(
        and_(
            InstagramAccount.id == account_id,
            InstagramAccount.is_deleted == False
        )
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account with id {account_id} not found"
        )
    
    return account


@router.put("/{account_id}", response_model=InstagramAccountResponse)
def update_instagram_account(
    account_id: int,
    account_data: InstagramAccountUpdate,
    db: Session = Depends(get_db)
):
    """Update Instagram account"""
    
    account = db.query(InstagramAccount).filter(
        and_(
            InstagramAccount.id == account_id,
            InstagramAccount.is_deleted == False
        )
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account with id {account_id} not found"
        )
    
    # Update fields
    if account_data.label is not None:
        account.label = account_data.label
    if account_data.status is not None:
        account.status = account_data.status
    if account_data.automation_enabled is not None:
        account.automation_enabled = account_data.automation_enabled
    
    account.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(account)
    
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instagram_account(
    account_id: int,
    hard_delete: bool = False,
    db: Session = Depends(get_db)
):
    """Delete Instagram account (soft delete by default)"""
    
    account = db.query(InstagramAccount).filter(
        and_(
            InstagramAccount.id == account_id,
            InstagramAccount.is_deleted == False
        )
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instagram account with id {account_id} not found"
        )
    
    if hard_delete:
        # Hard delete - remove from database
        db.delete(account)
    else:
        # Soft delete - mark as deleted
        account.is_deleted = True
        account.deleted_at = datetime.utcnow()
        account.status = "inactive"
    
    db.commit()
    
    return None
