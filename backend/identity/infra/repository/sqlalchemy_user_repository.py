"""Define concrete implementation of the UserRepository using SQLAlchemy."""
from sqlalchemy.orm import Session

from identity.domain.repository.user_repository import UserRepository
from identity.domain.entity.user import User


class SQLAlchemyUserRepository:
    """Concrete implementation of the UserRepository using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def get_user_by_username(self, username: str):
        """Get a user by their username."""
        return self.session.query(User).filter_by(username=username).first()

    def get_by_id(self, user_id: str):
        """Get a user by their unique identifier."""
        return self.session.query(User).filter_by(id=user_id).first()

    def create_user(self, user):
        """Create a new user in the repository."""
        self.session.add(user)

    def update_user_by_id(self, user: User):
        """Update an existing user in the repository."""
        existing_user = self.get_by_id(user.id)
        if existing_user:
            existing_user.display_name = user.display_name
            existing_user.username = user.username
            existing_user.password = user.password

    def delete_user_by_id(self, user):
        """Delete a user from the repository."""
        existing_user = self.get_by_id(user.id)
        if existing_user:
            self.session.delete(existing_user)
            # Commit later in the unit of work to allow for transaction management

def get_user_repository(session: Session) -> UserRepository:
    """Dependency injection for SQLAlchemyUserRepository."""
    return SQLAlchemyUserRepository(session)
