"""Upload Queue Model"""

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base, IDMixin, TimestampMixin


class UploadQueue(Base, IDMixin, TimestampMixin):
    """Manual upload queue for reels"""
    __tablename__ = "upload_queue"
    
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False, index=True)
    instagram_account_id = Column(Integer, ForeignKey("instagram_accounts.id"), nullable=False, index=True)
    
    # Upload status
    upload_status = Column(String(20), default="pending", nullable=False, index=True)  # pending, uploaded, failed
    upload_error = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)
    
    # Upload metadata
    instagram_post_id = Column(String(100), nullable=True)
    instagram_url = Column(String(500), nullable=True)
    
    # Relationships
    reel = relationship("Reel")
    instagram_account = relationship("InstagramAccount", back_populates="upload_queue")
    
    def __repr__(self):
        return f"<UploadQueue(id={self.id}, reel_id={self.reel_id}, status={self.upload_status})>"
