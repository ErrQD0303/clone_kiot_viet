"""Define concrete implementation of the RoleRepository using SQLAlchemy."""
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from identity.domain.repository.role_repository import RoleRepository
from identity.domain.entity.role import Role
class SQLAlchemyRoleRepository:
    """Concrete implementation of the RoleRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_names(self, names: set[str]) -> list[Role]:
        if not names:
            return []

        result: Result = await self.session.execute(
            select(Role).where(Role.name.in_(names))
        )
        db_result = list(result.scalars().unique().all())
        return db_result

    async def get_by_codes(
        self,
        codes: list[str],
    ) -> list[Role]:
        if not codes:
            return []

        result: Result = await self.session.execute(select(Role).where(Role.code.in_(codes)))

        return list(result.scalars().unique().all())

    async def get_by_code(
        self,
        code: str,
    ) -> Role | None:
        result: Result = await self.session.execute(select(Role).where(Role.code == code))

        return result.scalar_one_or_none()

    def create(
        self,
        role: Role,
    ) -> None:
        self.session.add(role)

def get_role_repository(session: AsyncSession) -> RoleRepository:
    """Dependency injection for SQLAlchemyUserRepository."""
    return SQLAlchemyRoleRepository(session)
