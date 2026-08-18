"""Repository adapters for relational persistence using SQLAlchemy."""

from typing import Protocol


class UnitOfWork(Protocol):
    """Unit of Work pattern implementation for managing database transactions."""

    def commit(self):
        """Commit the current transaction."""

    def rollback(self):
        """Rollback the current transaction."""
