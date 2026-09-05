"""Define the UserRepository interface for user-related operations."""
from typing import Protocol
from uuid import UUID

from identity.domain.entity.user import User

class UserRepository(Protocol):
    """UserRepository interface for user-related operations."""
    async def get_all_users(self, with_roles: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_credential: bool = False) -> list[User]:
        """Get all users in the repository."""

    async def get_user_by_username(self, username: str, with_roles: bool = False, with_permissions: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_credential: bool = False) -> User | None:
        """Get a user by their username."""

    async def get_by_id(self, user_id: UUID, with_roles: bool = False, with_permissions: bool = False, with_sessions: bool = False, with_refresh_tokens: bool = False, with_password_credential: bool = False) -> User | None:
        """Get a user by their unique identifier."""

    def create_user(self, user: User):
        """Create a new user in the repository."""

    async def update_user_by_id(self, user: User):
        """Update an existing user in the repository."""

    async def delete_user_by_id(self, user_id: UUID):
        """Delete a user from the repository."""
