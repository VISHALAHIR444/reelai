"""Instagram Account Management Model"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.db.base import Base, IDMixin, TimestampMixin


class AccountStatus(str, Enum):
    """Instagram account status"""
    PENDING_VERIFICATION = "pending_verification"
    CONNECTED = "connected"
    VERIFICATION_FAILED = "verification_failed"
    INACTIVE = "inactive"


class InstagramAccount(IDMixin, TimestampMixin, Base):
    """Instagram account for scheduling and uploading"""
    
    __tablename__ = "instagram_accounts"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    label = Column(String(255), nullable=True)
    status = Column(SQLEnum(AccountStatus), default=AccountStatus.PENDING_VERIFICATION, nullable=False, index=True)
    
    # Verification tracking
    verified_by_post = Column(Boolean, default=False, nullable=False)
    verification_attempts = Column(Integer, default=0, nullable=False)
    last_verification_error = Column(String(1000), nullable=True)
    
    # Timestamps
    connected_at = Column(DateTime(timezone=True), nullable=True)
    last_verified_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Future automation flags (placeholders)
    automation_enabled = Column(Boolean, default=False, nullable=False)
    device_bound = Column(Boolean, default=False, nullable=False)
    
    # Future metadata (placeholders)
    session_id = Column(String(500), nullable=True)
    device_id = Column(String(500), nullable=True)
    automation_meta = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="instagram_accounts")
    schedules = relationship("ReelSchedule", back_populates="instagram_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<InstagramAccount(id={self.id}, username={self.username}, status={self.status})>"
