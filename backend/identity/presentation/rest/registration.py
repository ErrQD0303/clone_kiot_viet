from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

from identity.presentation.rest.response_error import UserNotFoundError, UserResponseError
from identity.presentation.rest.api import identity_router
from shared_kernel.infra.fastapi.registration import ExceptionHandlerRegistration, FastAPIModule


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

identity_fastapi_module = FastAPIModule(
    routers=(identity_router,),
    exception_handlers=[
        ExceptionHandlerRegistration(
            exception_type=UserNotFoundError,
            handler=handle_user_not_found)
        ]
    )

