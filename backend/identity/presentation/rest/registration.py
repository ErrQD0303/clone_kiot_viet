from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

from identity.application.exceptions import InvalidCredentialError, NotEnoughPermissionError, TokenGenerationError, UserNotFoundError, InvalidAccessTokenError
from identity.presentation.rest.models.response_error import UserResponseError
from identity.presentation.rest.api import identity_router
from shared_kernel.infra.fastapi.registration_utility import FastAPIModule, ExceptionHandlerRegistration


logger = getLogger(__name__)

async def handle_user_not_found(_request: Request, exc: UserNotFoundError) -> JSONResponse:
    """Handle UserNotFoundError exceptions."""
    logger.warning(f"User not found: {exc.message}")
    
    response = UserResponseError(
        detail=exc.message,
        error={"user_id": f"User with id {exc.user_id} does not exist."} if hasattr(exc, 'user_id') else {"username": f"User with username {exc.username} does not exist."}
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=response.model_dump(mode="json")
    )

async def handle_token_generation_error(_request: Request, exc: TokenGenerationError) -> JSONResponse:
    """Handle TokenGenerationError exceptions."""
    logger.error(f"Token generation error: {exc.message}")
    
    response = UserResponseError(
        detail=exc.message,
        error={"user_id": f"Error generating token for user with id {exc.user_id}: {exc.error}"}
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=""  # Return an empty string as the content for 500 errors
    )

async def handle_invalid_access_token_error(_request: Request, exc: InvalidAccessTokenError) -> JSONResponse:
    """Handle InvalidAccessTokenError exceptions."""
    logger.warning(f"{exc.message}")
    
    response = UserResponseError(
        detail=exc.message,
        error={"token": "Invalid access token provided."} if exc.token else {"token": "No access token provided."}
    )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=response.model_dump(mode="json")
    )

async def handle_invalid_credential_error(_request: Request, exc: InvalidCredentialError) -> JSONResponse:
    """Handle InvalidCredentialError exceptions."""
    logger.warning(f"Invalid credentials: {exc.message}")
    
    response = UserResponseError(
        detail=exc.message,
        error={"username": "Invalid username or password."}
    )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=response.model_dump(mode="json")
    )

async def handle_not_enough_permission_error(_request: Request, exc: NotEnoughPermissionError) -> JSONResponse:
    """Handle NotEnoughPermissionError exceptions."""
    logger.warning(f"Not enough permissions: {exc.message}")
    
    response = UserResponseError(
        detail=exc.message,
        error={"missing_permissions": exc.required_permissions}
    )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=response.model_dump(mode="json")
    )

identity_fastapi_module = FastAPIModule(
    routers=(identity_router,),
    exception_handlers=[
        ExceptionHandlerRegistration(
            exception_type=UserNotFoundError,
            handler=handle_user_not_found)
        ,
        ExceptionHandlerRegistration(
            exception_type=TokenGenerationError,
            handler=handle_token_generation_error
        ),
        ExceptionHandlerRegistration(
            exception_type=InvalidCredentialError,
            handler=handle_invalid_credential_error
        ),
        ExceptionHandlerRegistration(
            exception_type=InvalidAccessTokenError,
            handler=handle_invalid_access_token_error
        ),
        ExceptionHandlerRegistration(
            exception_type=NotEnoughPermissionError,
            handler=handle_not_enough_permission_error
        )
    ]
)

