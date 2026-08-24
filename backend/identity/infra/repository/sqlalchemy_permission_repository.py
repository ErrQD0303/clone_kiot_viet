"""Define concrete implementation of the PermissionRepository using SQLAlchemy."""
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from identity.domain.repository.permission_repository import PermissionRepository
from identity.domain.entity.permission import Permission
from shared_kernel.domain.entity.permission_code import PermissionCode


class SQLAlchemyPermissionRepository:
    """Concrete implementation of the PermissionRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codes(self, codes: list[PermissionCode]) -> list[Permission]:
        """Get permissions by their unique codes."""
        if not codes:
            return []
        
        result: Result = await self.session.execute(
            select(Permission).where(Permission.code.in_(codes))
        )
        return list(result.scalars().all())

    async def get_by_code(self, code: PermissionCode) -> Permission | None:
        """Get a permission by its unique code."""
        result: Result = await self.session.execute(
            select(Permission).where(Permission.code == code)
        )
        return result.scalar_one_or_none()

    def create(self, permission: Permission) -> None:
        """Add a new permission to the current transaction."""
        self.session.add(permission)

def get_permission_repository(session: AsyncSession) -> PermissionRepository:
    """Dependency injection for SQLAlchemyPermissionRepository."""
    return SQLAlchemyPermissionRepository(session)
