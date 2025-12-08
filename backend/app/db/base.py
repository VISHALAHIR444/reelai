"""Base model for all SQLAlchemy models"""

from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql import func

# Create declarative base for models
Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models"""
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IDMixin:
    """Mixin to add id column to models"""
    
    id = Column(Integer, primary_key=True, index=True)
