"""Define the API endpoints for identity management."""
from typing import Annotated
from starlette import status

from dependency_injector.wiring import inject, Provide, Closing
from fastapi import APIRouter, Depends, Query

from identity.domain.repository.user_repository import UserRepository
from identity.presentation.rest.response import UserResponse, UserSchema, UsersResponse
from identity.presentation.rest.response_error import UserNotFoundError, UserResponseError
from shared_kernel.infra.database.schema import Schema

identity_router_prefix: str = '/' + Schema.IDENTITY.value
user_router_prefix: str = '/users'

identity_router = APIRouter(prefix=identity_router_prefix)
user_router = APIRouter(prefix=user_router_prefix)

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"model": UserResponse},
    status.HTTP_404_NOT_FOUND: {"model": UserResponseError},
})
@inject
async def get_user_by_id(
    user_id: str,
    user_repository: Annotated[UserRepository, Depends(Closing[Provide["user_repository"]])],
    include_roles: bool = Query(default=False, description="Include roles in the response"),
) -> UserResponse:
    """Get a user by ID."""
    user = await user_repository.get_by_id(user_id, include_roles=include_roles)
    if user is None:
        raise UserNotFoundError(user_id=user_id)

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
    users = await user_repository.get_all_users(include_roles=include_roles)
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

identity_router.include_router(user_router)
