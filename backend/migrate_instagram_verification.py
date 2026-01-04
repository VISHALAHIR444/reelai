"""Database migration: Add Instagram verification fields

Run this migration using Python:
    python migrate_instagram_verification.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.database import engine

def migrate():
    """Add verification columns to instagram_accounts table"""
    
    with engine.connect() as conn:
        print("Starting migration: Add Instagram verification fields...")
        
        try:
            # Add verified_by_post column
            conn.execute(text(
                "ALTER TABLE instagram_accounts ADD COLUMN verified_by_post BOOLEAN DEFAULT 0 NOT NULL"
            ))
            print("✓ Added verified_by_post column")
        except Exception as e:
            print(f"  verified_by_post already exists or error: {e}")
        
        try:
            # Add verification_attempts column
            conn.execute(text(
                "ALTER TABLE instagram_accounts ADD COLUMN verification_attempts INTEGER DEFAULT 0 NOT NULL"
            ))
            print("✓ Added verification_attempts column")
        except Exception as e:
            print(f"  verification_attempts already exists or error: {e}")
        
        try:
            # Add last_verification_error column
            conn.execute(text(
                "ALTER TABLE instagram_accounts ADD COLUMN last_verification_error TEXT"
            ))
            print("✓ Added last_verification_error column")
        except Exception as e:
            print(f"  last_verification_error already exists or error: {e}")
        
        try:
            # Add last_verified_at column
            conn.execute(text(
                "ALTER TABLE instagram_accounts ADD COLUMN last_verified_at TIMESTAMP"
            ))
            print("✓ Added last_verified_at column")
        except Exception as e:
            print(f"  last_verified_at already exists or error: {e}")
        
        try:
            # Make connected_at nullable (it's now set only after verification)
            # SQLite doesn't support modifying columns, so this is handled in model
            print("✓ connected_at is now nullable (handled in model)")
        except Exception as e:
            print(f"  connected_at modification: {e}")
        
        try:
            # Update existing records to pending_verification status
            result = conn.execute(text(
                "UPDATE instagram_accounts SET status = 'pending_verification' WHERE status = 'active'"
            ))
            print(f"✓ Updated {result.rowcount} existing accounts to pending_verification status")
        except Exception as e:
            print(f"  Status update: {e}")
        
        conn.commit()
        print("\nMigration completed successfully!")
        print("\nNext steps:")
        print("1. Restart backend server")
        print("2. Test verification endpoint: POST /instagram/accounts/{id}/verify")
        print("3. Replace placeholder test image with real 1080x1080 image")

if __name__ == "__main__":
    migrate()
