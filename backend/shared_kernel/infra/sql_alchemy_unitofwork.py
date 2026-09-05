"""Define SQLAlchemyUnitOfWork for managing database transactions using SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession
class SQLAlchemyUnitOfWork:
    """SQLAlchemyUnitOfWork for managing database transactions using SQLAlchemy."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        if self.session.in_transaction():
            raise RuntimeError(
                "Cannot enter Unit of Work: "
                "a transaction has already started."
            )

        await self.session.begin()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        if exc_type is not None:
            await self.rollback()
            return False

        try:
            await self.commit()
        except BaseException:
            await self.rollback()
            raise

        return False # Indicate that exceptions should not be suppressed

    async def commit(self) -> None:
        if not self.session.in_transaction():
            raise RuntimeError(
                "Cannot commit: no active transaction."
            )

        if not self.session.is_active:
            raise RuntimeError(
                "Cannot commit: transaction requires rollback."
            )

        await self.session.commit()

    async def rollback(self) -> None:
        if self.session.in_transaction():
            await self.session.rollback()

    async def flush(self) -> None:
        if not self.session.in_transaction():
            raise RuntimeError(
                "Cannot flush: no active transaction."
            )

        await self.session.flush()