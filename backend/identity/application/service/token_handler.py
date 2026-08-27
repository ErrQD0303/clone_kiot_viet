"""Define the Token Handler interface for generating and validating JWT tokens."""
from typing import Protocol

from identity.application.service.models.token import TokenData

class TokenHandler(Protocol):
    """Token Handler interface for generating and validating JWT tokens."""
    def generate_access_token(self, data: TokenData) -> str:
        """Generate an access token for a given user ID."""
        ...

    def generate_refresh_token(self) -> str:
        """Generate a refresh token."""
        ...

    def validate_access_token(self, token: str) -> bool:
        """Validate an access token."""
        ...

    def validate_refresh_token(self, token: str) -> bool:
        """Validate a refresh token."""
        ...
