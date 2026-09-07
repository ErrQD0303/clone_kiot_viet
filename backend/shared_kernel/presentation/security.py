"""Define the security utilities for FastAPI."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from identity.application.exceptions import InvalidAccessTokenError, NotEnoughPermissionError
from identity.application.service.token_handler import TokenHandler
from identity.domain.authorization.identity_role import IdentityRole
from shared_kernel.domain.entity.permission_definition import PermissionDefinition
from shared_kernel.infra.fastapi.security import get_access_token_scheme
from shared_kernel.infra.fastapi.config import settings
from shared_kernel.presentation.dependencies.principal import Principal
import logging

logger = logging.getLogger(__name__)


@inject
def get_current_principal(
    token_handler: Annotated[TokenHandler, Depends(Provide("token_handler"))],
    access_token: Annotated[str, Depends(get_access_token_scheme)]
) -> Principal:
    """Get the current principal from the access token."""
    try:
        is_token_valid, token_data = token_handler.validate_access_token(access_token, valid_issuer=settings.ISSUER, valid_audience=settings.AUDIENCE)
        if not is_token_valid or token_data is None:
            logger.warning("Invalid access token provided during logout.")
            raise InvalidAccessTokenError(token=access_token)

        return Principal(
            user_id=token_data.user_id,
            username=token_data.username,
            email=token_data.email,
            status=token_data.status,
            roles=token_data.roles,
            permissions=token_data.permissions,
            display_name=token_data.display_name,
            session_id=token_data.session_id
        )
    except Exception as e:
        logger.error(f"Error validating access token: {str(e)}")
        raise InvalidAccessTokenError(token=access_token)


def require_permission(*permissions: PermissionDefinition):
    """Dependency to require specific permissions for an endpoint."""
    def permission_dependency(principal: Annotated[Principal, Depends(get_current_principal)]):
        # if principal.has_role(IdentityRole.ADMIN.value):
        #     return principal
        
        missing = [
            permission_definition.code.value 
            for permission_definition in permissions 
            if not principal.has_permission(permission_definition.code.value)
        ]

        if missing:
            logger.warning(f"User {principal.username} is missing required permissions: {', '.join(missing)}")

            raise NotEnoughPermissionError(
                username=principal.username,
                missing_permissions=missing
            )

        return principal

    return permission_dependency
