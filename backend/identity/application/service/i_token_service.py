"""Define the Token Service interface for generating and validating JWT tokens."""

from typing import Protocol


class ITokenService(Protocol):
    """Token Service"""
    def generate_access_token(self, user_id: str) -> str:
        """Generate an access token for a given user ID."""
        ...

    def generate_refresh_token(self, user_id: str) -> str:
        """Generate a refresh token for a given user ID."""
        ...

    def validate_access_token(self, token: str) -> bool:
        """Validate an access token."""
        ...

    def validate_refresh_token(self, token: str) -> bool:
        """Validate a refresh token."""
        ...
