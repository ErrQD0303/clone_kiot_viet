"""Define the Logout Model for user logout and session management."""

from pydantic import BaseModel

class Revoked_Tokens(BaseModel):
    """Define the revoked tokens model for user logout and session management."""
    access_token: bool
    refresh_token: bool


class LogoutModel(BaseModel):
    """Logout Model for user logout and session management."""

    revoked_tokens: Revoked_Tokens