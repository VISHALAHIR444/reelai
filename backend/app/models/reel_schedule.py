"""Reel Scheduling and Upload Queue Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.db.base import Base, IDMixin, TimestampMixin


class ScheduleStatus(str, Enum):
    """Reel schedule/upload status"""
    GENERATED = "generated"
    SCHEDULED = "scheduled"
    READY_FOR_UPLOAD = "ready_for_upload"
    UPLOADED = "uploaded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReelSchedule(IDMixin, TimestampMixin, Base):
    """Manual upload queue and scheduling"""
    
    __tablename__ = "reel_schedules"
    
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False, index=True)
    instagram_account_id = Column(Integer, ForeignKey("instagram_accounts.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    status = Column(SQLEnum(ScheduleStatus), default=ScheduleStatus.GENERATED, nullable=False, index=True)
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    uploaded_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    
    # Relationships
    reel = relationship("Reel", backref="schedules")
    instagram_account = relationship("InstagramAccount", back_populates="schedules")
    user = relationship("User", backref="reel_schedules")
    
    def __repr__(self):
        return f"<ReelSchedule(id={self.id}, reel_id={self.reel_id}, status={self.status})>"
