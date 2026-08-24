"""Define the BaseResponse class for API responses."""

from typing import Any
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response class for API responses."""
    detail: str = Field(...)
    result: Any