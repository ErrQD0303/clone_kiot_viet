"""Define the Response Models for Shared Kernel."""

from pydantic import BaseModel

from shared_kernel.infra.fastapi.exception import DEFAULT_PASSWORD_STRENGTH_ERROR_MESSAGE


class PasswordStrengthResponseError(BaseModel):
    """Response model for password strength validation errors."""
    detail: str = DEFAULT_PASSWORD_STRENGTH_ERROR_MESSAGE