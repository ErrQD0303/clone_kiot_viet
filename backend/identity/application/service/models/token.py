"""Define the token models for jwt token management."""

from pydantic import BaseModel

class Token(BaseModel):
    """Define the token model for jwt token management."""
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None # Expiration time in seconds for the access token
    scope: str | None = None # Scope of the access token, if applicables

class TokenData(BaseModel):
    """Define the token data model for jwt token management."""
    user_id: str
    username: str
    email: str
    status: str
    display_name: str | None = None
    roles: list[str] = []
    permissions: list[str] = []
    session_id: str | None = None

class AccessTokenPayload(BaseModel):
    """Define the token payload model for jwt token management."""
    sub: str # user_id
    username: str # username
    email: str # email
    account_status: str | None = None # account_status
    display_name: str | None = None # display_name
    roles: list[str] = [] # roles
    permissions: list[str] = [] # permissions
    iss: str | None = None # issuer
    aud: str | None = None # audience
    iat: int | None = None # issued at
    exp: int | None = None # expiration time
    sid: str | None = None # session id, used for session management

class CreatedRefreshToken(BaseModel):
    """Define the created refresh token model for jwt token management."""
    refresh_token: str
    expires_at: int # Expiration time in seconds for the refresh token

class CreatedAccessToken(BaseModel):
    """Define the created access token model for jwt token management."""
    access_token: str
    expires_at: int # Expiration time in seconds for the access token
    token_type: str = "Bearer" # Token type, default is "Bearer"