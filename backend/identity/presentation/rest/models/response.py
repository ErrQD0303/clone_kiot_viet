"""Define the Reponse Models for identity management."""

from pydantic import BaseModel

from identity.application.service.models.logout_model import LogoutModel
from identity.application.service.models.token import Token
from shared_kernel.presentation.base_response import BaseResponse

class UserSchema(BaseModel):
    """Schema for user-related data."""
    user_id: str
    username: str
    display_name: str
    email: str
    roles: list[str]


class UserResponse(BaseResponse):
    """Response model for user-related API responses."""
    result: UserSchema

class UsersResponse(BaseResponse):
    """Response model for multiple users."""
    result: list[UserSchema]

class TokenResponse(BaseResponse):
    """Response model for token-related API responses."""
    result: Token

class LogoutResponse(BaseResponse):
    """Response model for logout API responses."""
    result: LogoutModel