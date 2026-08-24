"""Define concrete implementation of the UserRepository using SQLAlchemy."""
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload

from identity.domain.repository.user_repository import UserRepository
from identity.domain.entity.user import User


class SQLAlchemyUserRepository:
    """Concrete implementation of the UserRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self, include_roles: bool = False) -> list[User]:
            """Get all users in the repository."""
            statement = select(User)
            if not include_roles:
                statement = statement.options(raiseload(User._role_links))
            result: Result = await self.session.execute(statement)
            return list(result.scalars().all())

    async def get_user_by_username(self, username: str, include_roles: bool = False) -> User | None:
        """Get a user by their username."""
        statement = select(User).where(User.username == username)
        if not include_roles:
            statement = statement.options(raiseload(User._role_links))
        result: Result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: str, include_roles: bool = False) -> User | None:
        """Get a user by their unique identifier."""
        statement = select(User).where(User.id == user_id)
        if not include_roles:
            statement = statement.options(raiseload(User._role_links))
        result: Result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    def create_user(self, user):
        """Create a new user in the repository."""
        self.session.add(user)

    async def update_user_by_id(self, user: User):
        """Update an existing user in the repository."""
        existing_user = await self.get_by_id(user.id)
        if existing_user:
            existing_user.display_name = user.display_name
            existing_user.username = user.username
            existing_user.password = user.password

    async def delete_user_by_id(self, user):
        """Delete a user from the repository."""
        existing_user = await self.get_by_id(user.id)
        if existing_user:
            self.session.delete(existing_user)
            # Commit later in the unit of work to allow for transaction management

def get_user_repository(session: AsyncSession) -> UserRepository:
    """Dependency injection for SQLAlchemyUserRepository."""
    return SQLAlchemyUserRepository(session)
