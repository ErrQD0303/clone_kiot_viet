"""Define the RefreshTokenRepository interface for managing token-related operations."""
from typing import Protocol

class RefreshTokenRepository(Protocol):
    """RefreshTokenRepository interface for managing token-related operations."""

    async def save_token(self, user_id: str, token: str) -> None:
        """Save a token for a given user ID."""

    async def get_token(self, user_id: str) -> str:
        """Retrieve a token for a given user ID."""

    async def delete_token(self, user_id: str) -> None:
        """Delete a token for a given user ID."""