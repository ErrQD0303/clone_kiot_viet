"""Define the API endpoints for identity management."""
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID
from starlette import status

from dependency_injector.wiring import inject, Provide, Closing
from fastapi import APIRouter, Depends, Form, Query, Request

from identity.application.exceptions import AccountNotActiveError, InvalidAccessTokenError, InvalidCredentialError, UserNotFoundError
from identity.application.service.application_authentication_service import ApplicationAuthenticationService
from identity.application.service.i_authentication_service import IAuthenticationService
from identity.application.service.models.logout_model import LogoutModel, Revoked_Tokens
from identity.application.service.models.token import CreatedRefreshToken, Token
from identity.application.service.token_handler import TokenHandler
from identity.application.service.token_service import TokenService
from identity.domain.entity.session import Session
from identity.domain.repository.refreshtoken_repository import RefreshTokenRepository
from identity.domain.repository.user_repository import UserRepository
from identity.infra.repository.sqlalchemy_session_repository import SQLAlchemySessionRepository
from identity.presentation.rest.models.request import LoginFormRequest
from identity.presentation.rest.models.response import TokenResponse, UserResponse, UserSchema, UsersResponse, LogoutResponse
from identity.presentation.rest.models.response_error import UserResponseError
from shared_kernel.domain.unit_of_work import UnitOfWork
from shared_kernel.infra.database.schema import Schema
from logging import INFO, getLogger
from shared_kernel.infra.fastapi.config import Setting, settings
from shared_kernel.infra.fastapi.helper import as_form
from shared_kernel.presentation.dependencies.principal import Principal
from shared_kernel.presentation.security import get_current_principal

logger = getLogger(__name__)

identity_router_prefix: str = '/' + Schema.IDENTITY.value
user_router_prefix: str = '/users'
token_router_prefix: str = '/tokens'
auth_router_prefix: str = '/auth'

identity_router = APIRouter(prefix=identity_router_prefix)
user_router = APIRouter(prefix=user_router_prefix)
token_router = APIRouter(prefix=token_router_prefix)
auth_router = APIRouter(prefix=auth_router_prefix)

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"model": UserResponse},
    status.HTTP_404_NOT_FOUND: {"model": UserResponseError},
})
@inject
async def get_user_by_id(
    user_id: str,
    user_repository: Annotated[UserRepository, Depends(Closing[Provide["user_repository"]])],
    include_roles: bool = Query(default=False, description="Include roles in the response"),
    user: str = Query(default="anonymous", description="user that makes the query")
) -> UserResponse:
    """Get a user by ID."""
    logger.info(f"User {user} is querying for user with ID: {user_id}, include_roles={include_roles}")
    user = await user_repository.get_by_id(user_id, include_roles=include_roles)
    if user is None:
        logger.info(f"User with ID {user_id} not found.")
        raise UserNotFoundError(user_id=user_id)

    logger.info(f"User with ID {user_id} found: {user.username}, include_roles={include_roles}")

    return UserResponse(
        detail="ok",
        result=UserSchema(
            user_id=str(user.id),
            username=user.username,
            display_name=user.display_name,
            email=user.email,
            roles=[role.Role.code for role in user.RoleLinks] if include_roles else []
        )
    )

@user_router.get("/")
@inject
async def get_all_users(
    user_repository: Annotated[UserRepository, Depends(Closing[Provide["user_repository"]])],
    include_roles: bool = Query(default=False, description="Include roles in the response"),
) -> UsersResponse:
    """Get all users."""
    users = await user_repository.get_all_users(with_roles=include_roles)
    return UsersResponse(
            detail="ok",
            result= [UserSchema(
                user_id=str(user.id),
                username=user.username,
                display_name=user.display_name,
                email=user.email,
                roles=[role.Role.code for role in user.RoleLinks] if include_roles else []) for user in users])

@user_router.get("/by-username/{username}", response_model=UserResponse, status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"model": UserResponse},
    status.HTTP_404_NOT_FOUND: {"model": UserResponseError},
})
@inject
async def get_user_by_username(
    username: str,
    user_repository: Annotated[UserRepository, Depends(Closing[Provide["user_repository"]])],
    include_roles: bool = Query(default=False, description="Include roles in the response"),
) -> UserResponse:
    """Get a user by username."""
    user = await user_repository.get_user_by_username(username, include_roles=include_roles)
    if user is None:
        raise UserNotFoundError(username=username)

    return UserResponse(
        detail="ok",
        result=UserSchema(
            user_id=str(user.id),
            username=user.username,
            display_name=user.display_name,
            email=user.email,
            roles=[role.Role.code for role in user.RoleLinks] if include_roles else []
        )
    )

@auth_router.post("/login", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"model": TokenResponse},
})
@inject
async def login(
    request: Request,
    authentication_service: Annotated[ApplicationAuthenticationService, Depends(Provide("authentication_service"))],
    form_data: LoginFormRequest = Depends(LoginFormRequest.as_form),
) -> TokenResponse:
    """Login and get access token and refresh token."""
    user_ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent") if request.headers else None
    logger.info(f"Login attempt for username: {form_data.username} from IP: {user_ip_address}, User-Agent: {user_agent}")

    try:
        token_pair = await authentication_service.login_by_username(
            username=form_data.username,
            password=form_data.password.get_secret_value(),
            ip_address=user_ip_address,
            user_agent=user_agent,
        )
    except InvalidCredentialError:
        # Will be handled by the exception handler registered for InvalidCredentialError
        raise 
    except AccountNotActiveError:
        # Will be handled by the exception handler registered for AccountNotActiveError
        raise 
    except Exception as e:
        logger.error(f"Unexpected error during login for username: {form_data.username}. Error: {str(e)}")
        raise

    return TokenResponse(
        detail="ok",
        result=token_pair,
    )

@auth_router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"model": LogoutResponse},
    status.HTTP_401_UNAUTHORIZED: {"model": UserResponseError}
})
@inject
async def logout(
    principal: Annotated[Principal, Depends(get_current_principal)],
    authentication_service: Annotated[IAuthenticationService, Depends(Provide("authentication_service"))]
) -> LogoutResponse:
    """Logout and revoke the refresh token."""
    logger.info(f"Logout Start: User {principal.username} is attempting to logout. Session ID: {principal.session_id}")

    try:
        await authentication_service.logout(session_id=principal.session_id)

        logger.info(f"User {principal.username} logged out successfully. Session ID: {principal.session_id}")
    except InvalidAccessTokenError:
        raise
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise

    return LogoutResponse(
        detail="Logout successful!!!",
        result=LogoutModel(
            revoked_tokens=Revoked_Tokens(
                access_token=True,
                refresh_token=True)
        )
    )

identity_router.include_router(user_router)
identity_router.include_router(token_router)
identity_router.include_router(auth_router)
