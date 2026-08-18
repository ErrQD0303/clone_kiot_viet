"""Define the UserRepository interface for user-related operations."""
from typing import Protocol

class UserRepository(Protocol):
    """UserRepository interface for user-related operations."""

    def get_user_by_username(self, username: str):
        """Get a user by their username."""

    def get_by_id(self, user_id: str):
        """Get a user by their unique identifier."""

    def create_user(self, user):
        """Create a new user in the repository."""

    def update_user_by_id(self, user):
        """Update an existing user in the repository."""

    def delete_user_by_id(self, user):
        """Delete a user from the repository."""
