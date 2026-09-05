"""Define the Token Handler interface for generating and validating JWT tokens."""
from typing import Protocol

from identity.application.service.models.token import CreatedAccessToken, CreatedRefreshToken, TokenData

class TokenHandler(Protocol):
    """Token Handler interface for generating and validating JWT tokens."""
    def generate_access_token(self, data: TokenData, issuer: str, audience: str, expired_in_minute: int | None = None) -> CreatedAccessToken:
        """Generate an access token for a given user ID."""
        ...

    def generate_refresh_token(self, expired_in_minute: int | None = None) -> CreatedRefreshToken:
        """Generate a refresh token."""
        ...

    def validate_access_token(self, token: str, valid_issuer: str, valid_audience: str) -> tuple[bool, TokenData | None]:
        """Validate an access token."""
        ...

    def validate_refresh_token(self, token: str) -> bool:
        """Validate a refresh token."""
        ...
