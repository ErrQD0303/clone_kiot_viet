"""Repository adapters for relational persistence using SQLAlchemy."""

from typing import Protocol


class UnitOfWork(Protocol):
    """Unit of Work pattern implementation for managing database transactions."""

    async def commit(self):
        """Commit the current transaction."""

    async def rollback(self):
        """Rollback the current transaction."""

    async def flush(self):
        """Flush the current transaction."""
