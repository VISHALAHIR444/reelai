import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.models import Base
from app.core.config import get_settings

settings = get_settings()

# Database URL
if "sqlite" in settings.database_url:
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.debug
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
