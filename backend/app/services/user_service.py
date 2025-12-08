"""User service with complete CRUD and authentication"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password
from app.utils.helpers import get_logger

logger = get_logger(__name__)


class UserService:
    """Service for user-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            hashed_password = hash_password(user_data.password)
            
            user = User(
                email=user_data.email,
                username=user_data.username,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=False,
                instagram_connected=False,
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User created: {user.email}")
            return user
        
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            self.db.rollback()
            raise
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        try:
            user = self.get_user_by_email(email)
            if not user:
                logger.warning(f"Authentication failed: user not found - {email}")
                return None
            
            if not verify_password(password, user.hashed_password):
                logger.warning(f"Authentication failed: incorrect password - {email}")
                return None
            
            logger.info(f"User authenticated: {email}")
            return user
        
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return None
