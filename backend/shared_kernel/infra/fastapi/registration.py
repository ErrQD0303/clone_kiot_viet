"""Define the Registration module for FastAPI applications in the shared kernel."""

import logging

from fastapi import status, Request
from fastapi.responses import JSONResponse

from shared_kernel.infra.fastapi.exception import PasswordStrengthError
from shared_kernel.infra.fastapi.model.error import PasswordStrengthResponseError
from shared_kernel.infra.fastapi.registration_utility import ExceptionHandlerRegistration, FastAPIModule

logging.getLogger(__name__)

async def handle_password_strength_error(_request: Request, exc: PasswordStrengthError):
    """Handle PasswordStrengthError exceptions."""
    logging.info(f"Password strength error: {exc.message}")

    response = PasswordStrengthResponseError(
        detail=exc.message
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,  # Unprocessable Entity
        content=response.model_dump(mode="json")
    )

shared_kernel_fastapi_module = FastAPIModule(
    routers=(),
    exception_handlers=[
        ExceptionHandlerRegistration(
            exception_type=PasswordStrengthError,
            handler=handle_password_strength_error
        )
    ]
)