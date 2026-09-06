"""Defines the application container for dependency injection."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from pwdlib import PasswordHash

from identity.application.service.admin_init_service import AdminInitService
from identity.application.service.application_authentication_service import ApplicationAuthenticationService
from identity.application.service.sync_rbac_service import SyncRbacService
from identity.application.service.token_service import get_token_service
from identity.domain.repository import user_repository
from identity.infra.repository.sqlalchemy_permission_repository import SQLAlchemyPermissionRepository
from identity.infra.repository.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from identity.infra.repository.sqlalchemy_session_repository import SQLAlchemySessionRepository
from identity.infra.repository.sqlalchemy_refreshtoken_repository import SQLAlchemyRefreshTokenRepository
from identity.infra.repository.sqlalchemy_user_repository import SQLAlchemyUserRepository
from identity.infra.token.pyjwt_token_handler import PyJWTTokenHandler, get_token_handler
from identity.infra.token.database_token_service import DatabaseTokenService
from shared_kernel.infra.database.connection import async_session_factory
from shared_kernel.infra.database.orm import init_orm_mappers
from shared_kernel.infra.sql_alchemy_unitofwork import SQLAlchemyUnitOfWork
from identity.presentation.rest.registration import identity_fastapi_module
from shared_kernel.infra.fastapi.registration_utility import install_fastapi_modules
from shared_kernel.infra.fastapi.config import settings
from shared_kernel.infra.fastapi.registration import shared_kernel_fastapi_module
from identity.application.service.i_password_hasher import IPasswordHasher
from identity.application.service.password_hasher import PasswordHasher


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
            "shared_kernel.presentation.security",
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
        providers.Object(shared_kernel_fastapi_module),
    )

    install_fastapi = providers.Callable(
        install_fastapi_modules,
        modules=fastapi_modules ,
    )

    token_handler = providers.Singleton(
        get_token_handler,
        secret_key=settings.SECRET_KEY,  # Replace with your actual secret key
        algorithm=settings.ALGORITHM,  # Replace with your actual algorithm
        access_token_expiration_minute=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # Replace
        refresh_token_expiration_minute=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES),  # Replace
        token_type=settings.TOKEN_TYPE,  # Replace with your actual token type
    )

    refresh_token_repository = providers.Factory(
        SQLAlchemyRefreshTokenRepository,
        session=sync_rbac_session,
        user_repository=user_repository,
        settings=settings,
    )

    session_repository = providers.Factory(
        SQLAlchemySessionRepository,
        session=sync_rbac_session,
        user_repository=user_repository,
    )

    token_service = providers.Factory(
        get_token_service,
        implementation=DatabaseTokenService,
        token_handler=token_handler,
        refresh_token_repository=refresh_token_repository,
        session_repository=session_repository,
        unit_of_work=unit_of_work,
        issuer=settings.ISSUER,
        audience=settings.AUDIENCE,
    )

    password_hasher = providers.Singleton(
        PasswordHasher,
        password_hash=PasswordHash.recommended()
    )

    authentication_service = providers.Factory(
        ApplicationAuthenticationService,
        session_repository=session_repository,
        token_service=token_service,
        user_repository=user_repository,
        unit_of_work=unit_of_work,
        password_hasher=password_hasher,
        setting=settings,
    )

    admin_init_service = providers.Factory(
        AdminInitService,
        permission_repository=permission_repository,
        role_repository=role_repository,
        user_repository=user_repository,
        unit_of_work=unit_of_work,
        password_hasher=password_hasher,
        setting=settings,
    )


def create_application_container() -> AppContainer:
    """Create and return an instance of the application container."""
    init_orm_mappers()
    return AppContainer()

