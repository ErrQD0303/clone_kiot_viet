"""Define concrete implementation of the UserRepository using SQLAlchemy."""
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload

from identity.domain.entity.session import Session
from identity.domain.repository.user_repository import UserRepository
from identity.domain.entity.user import User


class SQLAlchemyUserRepository:
    """Concrete implementation of the UserRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _build_user_query(statement: Any, with_roles: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_credential: bool = False):
        """Build a SQLAlchemy query for retrieving users with optional related data."""
        if not with_roles:
            statement = statement.options(raiseload(User._role_links))
        if not with_sessions:
            statement = statement.options(raiseload(User._session_links))
        else:
            if not with_refresh_tokens:
                statement = statement.options(raiseload(User._session_links).raiseload(Session._refresh_token_links))
        if not with_password_credential:
            statement = statement.options(raiseload(User._password_credential))
        return statement

    async def get_all_users(self, with_roles: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_credential: bool = False) -> list[User]:
            """Get all users in the repository."""
            statement = self._build_user_query(statement=select(User),with_roles=with_roles, with_sessions=with_sessions, with_refresh_tokens=with_refresh_tokens, with_password_credential=with_password_credential)
            result: Result = await self.session.execute(statement)
            return list(result.scalars().all())

    async def get_user_by_username(self, username: str, with_roles: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_credential: bool = False) -> User | None:
        """Get a user by their username."""
        statement = self._build_user_query(statement=select(User).where(User.username==username), with_roles=with_roles, with_sessions=with_sessions, with_refresh_tokens=with_refresh_tokens,with_password_credential=with_password_credential)        
        result: Result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID, with_roles: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_crerdential: bool = False) -> User | None:
        """Get a user by their unique identifier."""
        statement = self._build_user_query(statement=select(User).where(User.id==user_id),with_roles=with_roles, with_sessions=with_sessions, with_refresh_tokens=with_refresh_tokens, with_password_credential=with_password_crerdential)
        result: Result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    def create_user(self, user: User) -> None:
        """Create a new user in the repository."""
        self.session.add(user)

    async def update_user_by_id(self, user: User):
        """Update an existing user in the repository."""
        existing_user = await self.get_by_id(user.id)
        if existing_user:
            existing_user.display_name = user.display_name
            existing_user.username = user.username
            existing_user.password = user.password
            existing_user.is_active = user.is_active
            existing_user.updated_at = user.updated_at
            existing_user._role_links = user._role_links
            existing_user._session_links = user._session_links

    async def delete_user_by_id(self, user_id: UUID):
        """Delete a user from the repository."""
        existing_user = await self.get_by_id(user_id)
        if existing_user:
            self.session.delete(existing_user)
            # Commit later in the unit of work to allow for transaction management

def get_user_repository(session: AsyncSession) -> UserRepository:
    """Dependency injection for SQLAlchemyUserRepository."""
    return SQLAlchemyUserRepository(session)
