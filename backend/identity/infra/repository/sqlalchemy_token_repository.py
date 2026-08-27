"""Define concrete implementation of the RefreshTokenRepository using SQLAlchemy."""
from datetime import datetime
from uuid import UUID

from requests import delete
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload

from identity.domain.entity.refresh_token import RefreshToken
from identity.domain.entity.session import Session
from identity.domain.entity.user import User
from identity.domain.entity.role import Role
from identity.domain.repository.token_repository import TokenRepository
from identity.domain.repository.user_repository import UserRepository
from shared_kernel.infra.fastapi.config import Setting

class SQLAlchemyRefreshTokenRepository:
    """Concrete implementation of the RefreshTokenRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession, user_repository: UserRepository, settings: Setting):
        self.session = session
        self._user_repository = user_repository
        self._settings = settings

    def save_token(self, session: Session, refresh_token: str, parent_token: RefreshToken, expires_time: datetime) -> None:
        """Save a token for a given user ID."""
        # Implementation for saving the token in the database
        if session is None:
            raise ValueError("Session cannot be None")
        if refresh_token is None:
            raise ValueError("Token cannot be None")
        if expires_time is None:
            raise ValueError("Expires time cannot be None")

        session.refresh_token = refresh_token
        session.parent_token = parent_token
        session.expires_time = expires_time
        self.session.add(session)

    def _build_token_query(self, statement: any, with_session: bool = False, with_users: bool = False):
        """Build a SQLAlchemy query for retrieving tokens with optional related data."""
        if not with_session:
            statement = statement.options(raiseload(RefreshToken._session_links))
        else:
            if not with_users:
                statement = statement.options(raiseload(RefreshToken._session_links).raiseload(Session._user_links))
        return statement

    def update_token(self, token: RefreshToken) -> None:
        """Update a token for a given refresh token."""
        if not token:
            raise ValueError("Token cannot be None")

        existing_token = self.session.get(RefreshToken, token.id)
        if existing_token:
            existing_token.token = token.token
            existing_token.expires_time = token.expires_time
            existing_token.revoked = token.revoked
            existing_token.parent_token_id = token.parent_token_id
            existing_token.updated_at = token.updated_at
            existing_token._session_links = token._session_links

    def get_token(self, refresh_token_id: UUID, with_session: bool = False, with_user: bool = False) -> RefreshToken | None:
        """Retrieve a refresh token with a specific refresh token id."""
        if not refresh_token_id:
            raise ValueError("Refresh token ID cannot be None")

        statement = self._build_token_query(statement=select(RefreshToken).where(RefreshToken.id == refresh_token_id), with_session=with_session, with_users=with_user)
        result: Result = self.session.execute(statement)
        return result.scalar_one_or_none()

    def delete_token(self, token: RefreshToken) -> None:
        """Delete a token for a given user ID."""
        self.session.delete(token)


def get_refresh_token_repository(session: AsyncSession) -> TokenRepository:
    """Dependency injection for SQLAlchemyUserRepository."""
    return SQLAlchemyRefreshTokenRepository(session)
