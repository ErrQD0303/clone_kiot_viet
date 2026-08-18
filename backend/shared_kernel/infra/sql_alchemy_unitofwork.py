"""Define SQLAlchemyUnitOfWork for managing database transactions using SQLAlchemy."""
from fastapi import Depends
from sqlalchemy.orm import Session

from shared_kernel.domain.unit_of_work import UnitOfWork
from clone_kiot_viet.backend.shared_kernel.infra.database.connection import get_db_session

class SQLAlchemyUnitOfWork:
    """Unit of Work pattern implementation for managing database transactions using SQLAlchemy."""

    def __init__(self, session):
        self.session = session

    def commit(self):
        """Commit the current transaction."""
        self.session.commit()

    def rollback(self):
        """Rollback the current transaction."""
        self.session.rollback()

def get_uow(session: Session = Depends(get_db_session)) -> UnitOfWork:
    """Dependency injection for SQLAlchemyUnitOfWork."""
    return SQLAlchemyUnitOfWork(session)