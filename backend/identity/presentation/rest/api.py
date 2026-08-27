"""Define the API endpoints for identity management."""
from typing import Annotated
from starlette import status

from dependency_injector.wiring import inject, Provide, Closing
from fastapi import APIRouter, Depends, Query

from identity.application.service.models.token import CreatedRefreshToken
from identity.application.service.token_handler import TokenHandler
from identity.domain.repository.token_repository import TokenRepository
from identity.domain.repository.user_repository import UserRepository
from identity.presentation.rest.models.response import UserResponse, UserSchema, UsersResponse
from identity.presentation.rest.models.response_error import UserNotFoundError, UserResponseError
from shared_kernel.infra.database.schema import Schema
from logging import INFO, getLogger

logger = getLogger(__name__)

identity_router_prefix: str = '/' + Schema.IDENTITY.value
user_router_prefix: str = '/users'
token_router_prefix: str = '/tokens'

identity_router = APIRouter(prefix=identity_router_prefix)
user_router = APIRouter(prefix=user_router_prefix)
token_router = APIRouter(prefix=token_router_prefix)

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

@token_router.post("/{refresh_token}", response_model=CreatedRefreshToken, status_code=status.HTTP_200_OK, responses={
    status.HTTP_201_CREATED: {"model": CreatedRefreshToken}, 
})
@inject
def generate_refresh_token(
    token_handler: Annotated[TokenHandler, Depends(Closing[Provide["token_handler"]])],
) -> CreatedRefreshToken:
    """Get a refresh token by its value."""
    refresh_token_entity = token_handler.generate_refresh_token()

    return refresh_token_entity

identity_router.include_router(user_router)
identity_router.include_router(token_router)
