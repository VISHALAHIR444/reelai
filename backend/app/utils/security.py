"""Security utilities for authentication and encryption"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.database import get_db
from app.models.user import User
from app.utils.helpers import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    try:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    try:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    except Exception as e:
        logger.error(f"Error creating refresh token: {str(e)}")
        raise


def verify_token(token: str) -> Optional[Dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    
    except JWTError as e:
        logger.warning(f"JWT verification failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return None


async def get_current_user(
    credentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id = int(payload.get("sub"))
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )
        
        return user
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
