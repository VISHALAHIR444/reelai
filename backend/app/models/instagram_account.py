"""Instagram Account Management Model"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base, IDMixin, TimestampMixin


class InstagramAccount(Base, IDMixin, TimestampMixin):
    """Instagram account registry for manual upload queue"""
    __tablename__ = "instagram_accounts"
    
    username = Column(String(100), unique=True, nullable=False, index=True)
    label = Column(String(200), nullable=False)
    status = Column(String(20), default="active", nullable=False, index=True)  # active, inactive
    
    # Future automation fields
    automation_enabled = Column(Boolean, default=False)
    last_used_at = Column(DateTime, nullable=True)
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    upload_queue = relationship("UploadQueue", back_populates="instagram_account")
    
    def __repr__(self):
        return f"<InstagramAccount(id={self.id}, username={self.username}, label={self.label}, status={self.status})>"
