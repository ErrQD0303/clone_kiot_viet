"""Defines the application container for dependency injection."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from identity.application.service.sync_rbac_service import SyncRbacService
from identity.domain.repository import user_repository
from identity.infra.repository.sqlalchemy_permission_repository import SQLAlchemyPermissionRepository
from identity.infra.repository.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from identity.infra.repository.sqlalchemy_user_repository import SQLAlchemyUserRepository
from shared_kernel.infra.database.connection import async_session_factory
from shared_kernel.infra.database.orm import init_orm_mappers
from shared_kernel.infra.sql_alchemy_unitofwork import SQLAlchemyUnitOfWork
from identity.presentation.rest.registration import identity_fastapi_module
from shared_kernel.infra.fastapi.registration import FastAPIModule, install_fastapi_modules


@asynccontextmanager
async def create_command_session(
    session_factory: sessionmaker,
) -> AsyncIterator[AsyncSession]:
    """Open one session for the lifetime of a CLI command."""
    async with session_factory() as session:
        yield session

class AppContainer(containers.DeclarativeContainer):  # pylint: disable=c-extension-no-member
    """Application container class for dependency injection."""
    wiring_config = containers.WiringConfiguration(  # pylint: disable=c-extension-no-member
        modules=[
            "identity.presentation.rest.api",
        ],
        warn_unresolved=True, # Warn if dependencies cannot be resolved
    )

    session_factory = providers.Object(async_session_factory)

    sync_rbac_session = providers.Resource(
        create_command_session,
        session_factory=session_factory,
    )

    permission_repository = providers.Factory(
        SQLAlchemyPermissionRepository,
        session=sync_rbac_session,
    )

    role_repository = providers.Factory(
        SQLAlchemyRoleRepository,
        session=sync_rbac_session,
    )

    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session=sync_rbac_session,
    )

    unit_of_work = providers.Factory(
        SQLAlchemyUnitOfWork,
        session=sync_rbac_session,
    )

    sync_rbac_service = providers.Factory(
        SyncRbacService,
        permission_repository=permission_repository,
        role_repository=role_repository,
        unit_of_work=unit_of_work,
    )

    fastapi_modules = providers.List(
        providers.Object(identity_fastapi_module),
        # Add another modules below here
    )

    install_fastapi = providers.Callable(
        install_fastapi_modules,
        modules=fastapi_modules ,
    )

def create_application_container() -> AppContainer:
    """Create and return an instance of the application container."""
    init_orm_mappers()
    return AppContainer()

