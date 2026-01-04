import logging
from datetime import datetime
from typing import Dict, List, Optional

import requests
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import InstagramToken

logger = logging.getLogger(__name__)
settings = get_settings()


class InstagramChecker:
    """Validates Facebook + Instagram connection status via Graph API v19."""

    REQUIRED_PERMISSIONS = [
        "instagram_basic",
        "instagram_content_publish",
        "pages_show_list",
        "pages_read_engagement",
        "business_management",
    ]

    def __init__(self, api_version: str = "v19.0"):
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def _graph_get(self, path: str, token: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        query = {"access_token": token}
        if params:
            query.update(params)

        response = requests.get(url, params=query, timeout=15)
        data = response.json()

        if response.status_code != 200 or "error" in data:
            error_info = data.get("error", {}) if isinstance(data, dict) else {}
            message = error_info.get("message", "Graph API error")
            code = error_info.get("code")
            raise GraphAPIError(message=message, code=code, details=error_info)

        return data

    def _check_permissions(self, token: str) -> List[str]:
        try:
            data = self._graph_get("/me/permissions", token)
            granted = {item.get("permission"): item.get("status") for item in data.get("data", [])}
            missing = [perm for perm in self.REQUIRED_PERMISSIONS if granted.get(perm) != "granted"]
            return missing
        except GraphAPIError as exc:
            logger.warning(f"Permission check failed: {exc.message}")
            raise

    def check_connection(self, db: Session) -> Dict:
        record: Optional[InstagramToken] = db.query(InstagramToken).filter_by(is_active=True).first()

        if not record:
            return {
                "fb_page_connected": False,
                "fb_page_id": None,
                "fb_page_name": None,
                "ig_connected": False,
                "ig_user_id": None,
                "long_lived_token_valid": False,
                "token_expiry_date": None,
                "required_permissions_missing": self.REQUIRED_PERMISSIONS,
                "message": "fb_page_missing",
            }

        token = record.long_lived_access_token
        expiry = record.token_expires_at
        now = datetime.utcnow()
        long_lived_token_valid = True
        message = "ok"

        if not token:
            return {
                "fb_page_connected": False,
                "fb_page_id": record.fb_page_id,
                "fb_page_name": record.fb_page_name,
                "ig_connected": False,
                "ig_user_id": record.ig_user_id,
                "long_lived_token_valid": False,
                "token_expiry_date": expiry.isoformat() if expiry else None,
                "required_permissions_missing": self.REQUIRED_PERMISSIONS,
                "message": "token_expired",
            }

        if expiry and expiry < now:
            long_lived_token_valid = False
            message = "token_expired"

        fb_page_connected = False
        fb_page_id = record.fb_page_id
        fb_page_name = record.fb_page_name
        ig_connected = False
        ig_user_id = record.ig_user_id
        required_permissions_missing: List[str] = []

        try:
            # Validate token
            me_data = self._graph_get("/me", token)
            if not me_data.get("id"):
                long_lived_token_valid = False
                message = "token_expired"
                return self._build_response(
                    fb_page_connected=False,
                    fb_page_id=fb_page_id,
                    fb_page_name=fb_page_name,
                    ig_connected=False,
                    ig_user_id=ig_user_id,
                    long_lived_token_valid=long_lived_token_valid,
                    expiry=expiry,
                    required_permissions_missing=self.REQUIRED_PERMISSIONS,
                    message=message,
                )

            # Validate Facebook pages
            pages_data = self._graph_get("/me/accounts", token)
            pages = pages_data.get("data", [])
            target_page = None
            for page in pages:
                if fb_page_id and page.get("id") == fb_page_id:
                    target_page = page
                    break
            if not target_page and pages:
                target_page = pages[0]
                fb_page_id = target_page.get("id")
                fb_page_name = target_page.get("name")

            if not target_page:
                message = "fb_page_missing"
                return self._build_response(
                    fb_page_connected=False,
                    fb_page_id=fb_page_id,
                    fb_page_name=fb_page_name,
                    ig_connected=False,
                    ig_user_id=ig_user_id,
                    long_lived_token_valid=long_lived_token_valid,
                    expiry=expiry,
                    required_permissions_missing=self.REQUIRED_PERMISSIONS,
                    message=message,
                )

            fb_page_connected = True

            page_access_token = target_page.get("access_token", token)

            # Validate Instagram Business account
            ig_data = self._graph_get(f"/{fb_page_id}", page_access_token, params={"fields": "instagram_business_account"})
            ig_account = ig_data.get("instagram_business_account") or {}
            ig_user_id = ig_account.get("id")
            if ig_user_id:
                ig_connected = True
            else:
                message = "ig_not_linked"

            # Permissions check
            required_permissions_missing = self._check_permissions(token)
            if required_permissions_missing and message == "ok":
                message = "permissions_missing"

        except GraphAPIError as exc:
            logger.error(f"Graph API error during check: {exc.message}")
            code = exc.code or 0
            if code == 190:
                long_lived_token_valid = False
                message = "token_expired"
            else:
                message = "graph_error"
            return self._build_response(
                fb_page_connected=fb_page_connected,
                fb_page_id=fb_page_id,
                fb_page_name=fb_page_name,
                ig_connected=ig_connected,
                ig_user_id=ig_user_id,
                long_lived_token_valid=long_lived_token_valid,
                expiry=expiry,
                required_permissions_missing=self.REQUIRED_PERMISSIONS if message == "token_expired" else required_permissions_missing,
                message=message,
            )
        except requests.RequestException as exc:
            logger.error(f"Network error during Instagram check: {exc}")
            message = "network_error"
            long_lived_token_valid = False
        except Exception as exc:
            logger.error(f"Unexpected error during Instagram check: {exc}")
            message = "unexpected_error"
            long_lived_token_valid = False

        return self._build_response(
            fb_page_connected=fb_page_connected,
            fb_page_id=fb_page_id,
            fb_page_name=fb_page_name,
            ig_connected=ig_connected,
            ig_user_id=ig_user_id,
            long_lived_token_valid=long_lived_token_valid,
            expiry=expiry,
            required_permissions_missing=required_permissions_missing,
            message=message,
        )

    @staticmethod
    def _build_response(
        *,
        fb_page_connected: bool,
        fb_page_id: Optional[str],
        fb_page_name: Optional[str],
        ig_connected: bool,
        ig_user_id: Optional[str],
        long_lived_token_valid: bool,
        expiry: Optional[datetime],
        required_permissions_missing: List[str],
        message: str,
    ) -> Dict:
        return {
            "fb_page_connected": fb_page_connected,
            "fb_page_id": fb_page_id,
            "fb_page_name": fb_page_name,
            "ig_connected": ig_connected,
            "ig_user_id": ig_user_id,
            "long_lived_token_valid": long_lived_token_valid,
            "token_expiry_date": expiry.isoformat() if expiry else None,
            "required_permissions_missing": required_permissions_missing,
            "message": message,
        }


class GraphAPIError(Exception):
    def __init__(self, message: str, code: Optional[int] = None, details: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

