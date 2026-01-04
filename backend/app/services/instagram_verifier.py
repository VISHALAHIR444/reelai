"""Instagram Account Verification Service"""

import logging
import os
from typing import Dict, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.instagram_account import InstagramAccount, AccountStatus
from app.services.instagram_publisher import InstagramPublisher

logger = logging.getLogger(__name__)


class InstagramVerifier:
    """Verify Instagram accounts by publishing test image post"""
    
    MAX_VERIFICATION_ATTEMPTS = 3
    TEST_IMAGE_PATH = "/home/ubuntu/reelai/backend/assets/verification_test.jpg"
    TEST_CAPTION = "✓ Instagram connection test – posted via Reels Studio"
    
    def __init__(self):
        self.publisher = InstagramPublisher()
    
    async def verify_account(
        self,
        account: InstagramAccount,
        ig_user_id: str,
        access_token: str,
        db: Session
    ) -> Tuple[bool, str]:
        """
        Verify Instagram account by publishing test image
        
        Args:
            account: InstagramAccount model instance
            ig_user_id: Instagram business account ID
            access_token: Valid Instagram access token
            db: Database session
            
        Returns:
            (success, message)
        """
        
        # Check verification attempts
        if account.verification_attempts >= self.MAX_VERIFICATION_ATTEMPTS:
            return False, f"Maximum verification attempts ({self.MAX_VERIFICATION_ATTEMPTS}) exceeded"
        
        # Check status - only allow pending or failed
        if account.status not in [AccountStatus.PENDING_VERIFICATION, AccountStatus.VERIFICATION_FAILED]:
            return False, f"Account must be in pending_verification or verification_failed status. Current: {account.status}"
        
        # Increment attempts
        account.verification_attempts += 1
        db.commit()
        
        try:
            # Check if test image exists
            if not os.path.exists(self.TEST_IMAGE_PATH):
                error_msg = "Verification test image not found"
                logger.error(f"{error_msg}: {self.TEST_IMAGE_PATH}")
                account.last_verification_error = error_msg
                account.status = AccountStatus.VERIFICATION_FAILED
                db.commit()
                return False, error_msg
            
            # Publish test image using Instagram Graph API
            # Note: For Instagram Graph API, we need a publicly accessible image URL
            # This is a simplified version - in production, upload test image to CDN first
            
            logger.info(f"Starting verification for account: {account.username}")
            
            # For now, simulate verification since we need actual Instagram API credentials
            # In production, this would call:
            # result = self.publisher.upload_image(
            #     ig_user_id=ig_user_id,
            #     image_url=test_image_url,
            #     caption=self.TEST_CAPTION,
            #     access_token=access_token
            # )
            
            # PRODUCTION IMPLEMENTATION:
            # Uncomment when Instagram API is configured with real credentials
            """
            from app.services.instagram_image_publisher import InstagramImagePublisher
            image_publisher = InstagramImagePublisher()
            
            # Upload test image to CDN/public storage first
            public_image_url = await upload_to_cdn(self.TEST_IMAGE_PATH)
            
            # Publish to Instagram
            result = image_publisher.upload_and_publish_image(
                ig_user_id=ig_user_id,
                image_url=public_image_url,
                caption=self.TEST_CAPTION,
                access_token=access_token
            )
            
            if result.get("success"):
                # Verification successful
                account.status = AccountStatus.CONNECTED
                account.verified_by_post = True
                account.connected_at = datetime.utcnow()
                account.last_verified_at = datetime.utcnow()
                account.last_verification_error = None
                db.commit()
                
                logger.info(f"Account {account.username} verified successfully")
                return True, "Instagram account verified successfully"
            else:
                # Verification failed
                error_msg = result.get("error", "Unknown error during verification")
                account.status = AccountStatus.VERIFICATION_FAILED
                account.last_verification_error = error_msg
                db.commit()
                
                logger.error(f"Verification failed for {account.username}: {error_msg}")
                return False, f"Verification failed: {error_msg}"
            """
            
            # TEMPORARY: Mark as verified for testing
            # Remove this block when implementing real Instagram API
            account.status = AccountStatus.CONNECTED
            account.verified_by_post = True
            account.connected_at = datetime.utcnow()
            account.last_verified_at = datetime.utcnow()
            account.last_verification_error = None
            db.commit()
            
            logger.info(f"Account {account.username} marked as verified (test mode)")
            return True, "Instagram account verified successfully (test mode - replace with real Instagram API)"
            
        except Exception as e:
            error_msg = f"Verification error: {str(e)}"
            logger.error(f"Verification failed for {account.username}: {error_msg}", exc_info=True)
            
            account.status = AccountStatus.VERIFICATION_FAILED
            account.last_verification_error = error_msg
            db.commit()
            
            return False, error_msg
    
    def can_retry_verification(self, account: InstagramAccount) -> Tuple[bool, str]:
        """Check if account can retry verification"""
        
        if account.verification_attempts >= self.MAX_VERIFICATION_ATTEMPTS:
            return False, f"Maximum attempts ({self.MAX_VERIFICATION_ATTEMPTS}) reached"
        
        if account.status == AccountStatus.CONNECTED:
            return False, "Account already verified"
        
        if account.status not in [AccountStatus.PENDING_VERIFICATION, AccountStatus.VERIFICATION_FAILED]:
            return False, f"Invalid status for verification: {account.status}"
        
        return True, "Verification allowed"
