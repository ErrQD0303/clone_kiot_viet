"""Define the SessionRepository interface for managing session-related operations."""
from typing import Protocol

from identity.domain.entity.session import Session
from identity.domain.entity.user import User

class SessionRepository(Protocol):
    """SessionRepository interface for managing session-related operations."""

    async def save_session(self, session: Session) -> None:
        """Create a session for a given user ID."""

    async def get_session(self, user_id: str, with_user: bool = False, with_refresh_tokens: bool = False) -> Session | None:
        """Retrieve a session for a given user ID."""

    async def delete_session(self, session: Session) -> None:
        """Delete a session for a given user ID."""