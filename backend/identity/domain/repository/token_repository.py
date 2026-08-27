"""Define the TokenRepository interface for managing session-related operations."""
from datetime import datetime
from typing import Protocol
from uuid import UUID

from identity.domain.entity.refresh_token import RefreshToken
from identity.domain.entity.session import Session
from identity.domain.entity.user import User

class TokenRepository(Protocol):
    """TokenRepository interface for managing token-related operations."""

    def save_token(self, session: Session, refresh_token: str, parent_token: RefreshToken, expires_time: datetime) -> None:
        """Save a token for a given session."""

    def update_token(self, token: RefreshToken) -> None:
        """Update a token for a given refresh token."""

    def get_token(self, refresh_token_id: UUID, with_session: bool = False, with_user: bool = False) -> RefreshToken | None:
        """Retrieve a refresh token with a specific refresh token id."""

    def delete_token(self, token: RefreshToken) -> None:
        """Delete a token for a given user ID."""