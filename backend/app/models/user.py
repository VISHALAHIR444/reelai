"""User model for database"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base, IDMixin, TimestampMixin


class User(IDMixin, TimestampMixin, Base):
    """User model"""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Instagram integration
    instagram_connected = Column(Boolean, default=False, nullable=False)
    instagram_user_id = Column(String(255), nullable=True, unique=True)
    
    # Relationships
    videos = relationship("Video", back_populates="user", cascade="all, delete-orphan")
    instagram_token = relationship("InstagramToken", back_populates="user", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="user", cascade="all, delete-orphan")
    instagram_accounts = relationship("InstagramAccount", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
