"""Define SQLAlchemyUnitOfWork for managing database transactions using SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession

from shared_kernel.domain.unit_of_work import UnitOfWork

class SQLAlchemyUnitOfWork:
    """Unit of Work pattern implementation for managing database transactions using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        """Commit the current transaction."""
        if not self.session.is_active:
            raise RuntimeError("Cannot commit: No active transaction.")
        await self.session.commit()

    async def rollback(self):
        """Rollback the current transaction."""
        await self.session.rollback()

    async def start(self):
        """Start a new transaction."""
        if self.session.in_transaction():
            raise RuntimeError("Cannot start a new transaction: Session is already active.")
        await self.session.begin()

    async def flush(self):
        """Flush the current transaction."""
        if not self.session.in_transaction():
            raise RuntimeError("Cannot flush: No active transaction.")
        await self.session.flush()

def get_uow(session: AsyncSession) -> UnitOfWork:
    """Dependency injection for SQLAlchemyUnitOfWork."""
    return SQLAlchemyUnitOfWork(session)
