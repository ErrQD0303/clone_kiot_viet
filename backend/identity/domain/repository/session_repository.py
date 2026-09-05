"""Define the SessionRepository interface for managing session-related operations."""
from typing import Protocol
from uuid import UUID

from identity.domain.entity.session import Session
from identity.domain.entity.user import User

class SessionRepository(Protocol):
    """SessionRepository interface for managing session-related operations."""

    async def save(self, session: Session) -> None:
        """Create a session for a given user ID."""

    async def get_session(self, session_id: str, with_user: bool = False, with_refresh_tokens: bool = False, include_expired: bool = False) -> Session | None:
        """Retrieve a session, excluding expired sessions unless requested."""

    async def get_current_valid_sessions(self, user_id: UUID) -> list[Session] | None:
        """Retrieve the current active session for a given user."""

    async def delete_session(self, session: Session) -> None:
        """Delete a session for a given user ID."""