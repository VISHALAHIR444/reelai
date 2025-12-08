"""Common schemas"""

from pydantic import BaseModel
from typing import Generic, TypeVar, Any, Optional


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper"""
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None
