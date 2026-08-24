"""Define the UserRepository interface for user-related operations."""
from typing import Protocol

from identity.domain.entity.user import User

class UserRepository(Protocol):
    """UserRepository interface for user-related operations."""
    async def get_all_users(self, include_roles: bool = False) -> list[User]:
        """Get all users in the repository."""

    async def get_user_by_username(self, username: str, include_roles: bool = False) -> User | None:
        """Get a user by their username."""

    async def get_by_id(self, user_id: str, include_roles: bool = False) -> User | None:
        """Get a user by their unique identifier."""

    def create_user(self, user):
        """Create a new user in the repository."""

    async def update_user_by_id(self, user):
        """Update an existing user in the repository."""

    async def delete_user_by_id(self, user):
        """Delete a user from the repository."""
