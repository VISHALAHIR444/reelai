"""CDN Upload Service - Make local files publicly accessible"""

import logging
import os
import shutil
from typing import Optional
from pathlib import Path
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CDNUploadService:
    """
    Handle uploading files to CDN or public storage.
    
    For Instagram Graph API, images must be publicly accessible via HTTPS URL.
    
    Supported methods:
    1. Local static server (development)
    2. AWS S3 (production)
    3. Cloudflare R2 (production alternative)
    4. Custom CDN (configurable)
    """
    
    def __init__(self):
        self.public_dir = Path("/home/ubuntu/reelai/backend/public")
        self.public_dir.mkdir(exist_ok=True)
        
        # Configure based on environment
        self.cdn_enabled = getattr(settings, 'cdn_enabled', False)
        self.cdn_type = getattr(settings, 'cdn_type', 'local')  # 'local', 's3', 'r2', 'custom'
        self.base_url = getattr(settings, 'public_base_url', 'http://localhost:8000/public')
    
    async def upload_file_to_public(
        self,
        local_file_path: str,
        destination_filename: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload a local file to public storage and return the public URL.
        
        Args:
            local_file_path: Path to local file
            destination_filename: Optional custom filename (uses original if None)
            
        Returns:
            Public HTTPS URL if successful, None otherwise
        """
        
        if not os.path.exists(local_file_path):
            logger.error(f"File not found: {local_file_path}")
            return None
        
        try:
            # Determine destination filename
            if not destination_filename:
                destination_filename = Path(local_file_path).name
            
            if self.cdn_type == 'local':
                return await self._upload_to_local(local_file_path, destination_filename)
            
            elif self.cdn_type == 's3':
                return await self._upload_to_s3(local_file_path, destination_filename)
            
            elif self.cdn_type == 'r2':
                return await self._upload_to_r2(local_file_path, destination_filename)
            
            elif self.cdn_type == 'custom':
                return await self._upload_to_custom_cdn(local_file_path, destination_filename)
            
            else:
                logger.error(f"Unknown CDN type: {self.cdn_type}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to upload file to CDN: {str(e)}", exc_info=True)
            return None
    
    async def _upload_to_local(self, source_path: str, filename: str) -> str:
        """
        Copy file to local public directory.
        
        For development only - requires web server to serve /public directory.
        """
        
        destination = self.public_dir / filename
        
        # Copy file
        shutil.copy2(source_path, destination)
        
        logger.info(f"File copied to public directory: {filename}")
        
        # Return public URL
        return f"{self.base_url}/{filename}"
    
    async def _upload_to_s3(self, source_path: str, filename: str) -> Optional[str]:
        """
        Upload file to AWS S3.
        
        Requires:
        - boto3 library
        - AWS credentials configured
        - S3 bucket with public read access
        """
        
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            s3_bucket = getattr(settings, 's3_bucket_name', None)
            s3_region = getattr(settings, 's3_region', 'us-east-1')
            
            if not s3_bucket:
                logger.error("S3 bucket name not configured")
                return None
            
            s3_client = boto3.client('s3', region_name=s3_region)
            
            # Upload file
            s3_client.upload_file(
                source_path,
                s3_bucket,
                filename,
                ExtraArgs={'ContentType': self._get_content_type(filename)}
            )
            
            # Generate public URL
            public_url = f"https://{s3_bucket}.s3.{s3_region}.amazonaws.com/{filename}"
            
            logger.info(f"File uploaded to S3: {public_url}")
            return public_url
            
        except ImportError:
            logger.error("boto3 not installed. Install with: pip install boto3")
            return None
        except ClientError as e:
            logger.error(f"S3 upload failed: {str(e)}")
            return None
    
    async def _upload_to_r2(self, source_path: str, filename: str) -> Optional[str]:
        """
        Upload file to Cloudflare R2.
        
        R2 is S3-compatible, so we use boto3 with custom endpoint.
        """
        
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            r2_bucket = getattr(settings, 'r2_bucket_name', None)
            r2_account_id = getattr(settings, 'r2_account_id', None)
            r2_access_key = getattr(settings, 'r2_access_key', None)
            r2_secret_key = getattr(settings, 'r2_secret_key', None)
            
            if not all([r2_bucket, r2_account_id, r2_access_key, r2_secret_key]):
                logger.error("R2 credentials not fully configured")
                return None
            
            # Configure R2 endpoint
            endpoint_url = f"https://{r2_account_id}.r2.cloudflarestorage.com"
            
            s3_client = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=r2_access_key,
                aws_secret_access_key=r2_secret_key
            )
            
            # Upload file
            s3_client.upload_file(
                source_path,
                r2_bucket,
                filename,
                ExtraArgs={'ContentType': self._get_content_type(filename)}
            )
            
            # Generate public URL (requires custom domain configured in R2)
            r2_public_domain = getattr(settings, 'r2_public_domain', None)
            if r2_public_domain:
                public_url = f"https://{r2_public_domain}/{filename}"
            else:
                public_url = f"{endpoint_url}/{r2_bucket}/{filename}"
            
            logger.info(f"File uploaded to R2: {public_url}")
            return public_url
            
        except ImportError:
            logger.error("boto3 not installed. Install with: pip install boto3")
            return None
        except ClientError as e:
            logger.error(f"R2 upload failed: {str(e)}")
            return None
    
    async def _upload_to_custom_cdn(self, source_path: str, filename: str) -> Optional[str]:
        """
        Upload to custom CDN provider.
        
        Override this method to integrate with your CDN of choice.
        """
        
        logger.warning("Custom CDN upload not implemented - falling back to local")
        return await self._upload_to_local(source_path, filename)
    
    def _get_content_type(self, filename: str) -> str:
        """Get MIME type for file"""
        
        import mimetypes
        content_type, _ = mimetypes.guess_type(filename)
        return content_type or 'application/octet-stream'
