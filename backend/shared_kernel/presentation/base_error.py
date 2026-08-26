"""Define the BaseResponseError class for API error responses."""

from typing import Any

from pydantic import BaseModel


class BaseResponseError(BaseModel):
    """Base response error class for API error responses."""
    detail: str
    error: Any = None
