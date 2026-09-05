"""Define concrete implementation of the SessionRepository using SQLAlchemy."""
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload, joinedload

from identity.domain.entity.refresh_token import RefreshToken
from identity.domain.entity.session import Session
from identity.domain.entity.user import User
from identity.domain.repository.refreshtoken_repository import RefreshTokenRepository
from identity.domain.repository.session_repository import SessionRepository
from identity.domain.repository.user_repository import UserRepository
class SQLAlchemySessionRepository:
    """Concrete implementation of the SessionRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession, user_repository: UserRepository):
        self.session = session
        self._user_repository = user_repository

    async def save(self, session: Session) -> None:
        """Save a session for a given user ID."""
        existing_session = await self.get_session(session.id)
        if existing_session:
            # Update existing session
            existing_session.last_seen_at = datetime.now(tz=UTC)
            existing_session.updated_at = datetime.now(tz=UTC)
            existing_session.revoked_at = session.revoked_at
            existing_session.revoke_reason = session.revoke_reason
            existing_session.ip_address = session.ip_address
            existing_session.user_agent = session.user_agent
            existing_session.expires_at = session.expires_at
            existing_session.user_id = session.user_id
            return

        self.session.add(session)
    
    async def get_session(self, session_id: str, with_user: bool = False, with_refresh_tokens: bool = False, include_expired: bool = False) -> Session | None:
        """Retrieve a session for a given user ID."""
        statement = select(Session).where(Session.id == session_id and (Session.revoked_at.is_(None) if not include_expired else True) and (Session.expires_at > datetime.now(tz=UTC) if not include_expired else True))
        if not with_user:
            statement = statement.options(raiseload(Session._user))
        if not with_refresh_tokens:
            statement = statement.options(raiseload(Session._refresh_token_links))

        result: Result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_current_valid_sessions(self, user_id: UUID) -> list[Session] | None:
            """Retrieve the current active session for a given user."""
            statement = select(Session).where(Session.user_id == user_id, Session.revoked_at.is_(None), Session.expires_at > datetime.now(tz=UTC)).order_by(Session.last_seen_at.desc())
            result: Result = await self.session.execute(statement)
            return result.scalars().all()

    async def delete_session(self, session: Session) -> None:
        """Delete a session for a given user ID."""
        self.session.delete(session)

    
def get_session_repository(session: AsyncSession) -> SessionRepository:
    """Dependency injection for SQLAlchemyUserRepository."""
    return SQLAlchemySessionRepository(session)
