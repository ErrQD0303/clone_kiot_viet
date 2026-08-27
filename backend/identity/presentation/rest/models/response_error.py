"""Define the Response Error Models for identity management."""

from shared_kernel.presentation.base_error import BaseResponseError


class UserNotFoundError(Exception):
    """Raise this exception when a user is not exists in the repository."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found."
        super().__init__(self.message)

    def __init__(self, username: str):
        self.username = username
        self.message = f"User with username {username} not found."
        super().__init__(self.message)

class UserResponseError(BaseResponseError):
    """Response model for user-related API errors."""
