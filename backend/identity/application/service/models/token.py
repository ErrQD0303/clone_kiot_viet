"""Define the token models for jwt token management."""

from pydantic import BaseModel
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Token(BaseModel):
    """Define the token model for jwt token management."""
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None # Expiration time in seconds for the access token
    refresh_expires_in: int | None = None # Expiration time in seconds for the refresh token

@dataclass(frozen=True, slots=True)
class TokenData(BaseModel):
    """Define the token data model for jwt token management."""
    user_id: str
    username: str
    email: str
    status: str
    display_name: str | None = None
    roles: list[str] = []

@dataclass(frozen=True, slots=True)
class TokenPayload(BaseModel):
    """Define the token payload model for jwt token management."""
    sub: str # user_id
    username: str # username
    email: str # email
    account_status: str | None = None # account_status
    display_name: str | None = None # display_name
    roles: list[str] = [] # roles

@dataclass(frozen=True, slots=True)
class CreatedRefreshToken(BaseModel):
    """Define the created refresh token model for jwt token management."""
    refresh_token: str
    expires_at: int # Expiration time in seconds for the refresh token
    