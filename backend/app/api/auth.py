"""Authentication API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.services.user_service import UserService
from app.utils.security import create_access_token, create_refresh_token
from app.core.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        user_service = UserService(db)
        
        # Check if user exists
        existing = user_service.get_user_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = user_service.create_user(user_data)
        return user
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user and get JWT tokens"""
    try:
        user_service = UserService(db)
        
        # Authenticate user
        user = user_service.authenticate_user(credentials.email, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(days=settings.refresh_token_expire_days)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        from app.utils.security import verify_token
        
        payload = verify_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = int(payload.get("sub"))
        
        # Generate new access token
        access_token = create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
