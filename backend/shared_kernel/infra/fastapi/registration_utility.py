"""Define the FastAPI module registration utilities."""

from collections.abc import Callable, Coroutine, Sequence
from dataclasses import dataclass
from typing import Any
from fastapi import APIRouter, FastAPI
from starlette.responses import Response


ExceptionHandler = Callable[
    ...,
    Coroutine[Any, Any, Response]
]

@dataclass(frozen=True, slots=True)
class ExceptionHandlerRegistration:
    exception_type: type[Exception]
    handler: ExceptionHandler

@dataclass(frozen=True, slots=True)
class FastAPIModule:
    routers: tuple[APIRouter, ...]
    exception_handlers: tuple[ExceptionHandlerRegistration, ...] = ()

def is_included_router_exist(router: APIRouter):
    return len(router.routes) > 0

def install_fastapi_modules(
        app: FastAPI,
        modules: Sequence[FastAPIModule],
):
    """Install FastAPI modules into the FastAPI application."""
    for module in modules:
        for router in module.routers:
            app.include_router(router)

        for exc_handler in module.exception_handlers:
            app.add_exception_handler(
                exc_handler.exception_type,
                exc_handler.handler
            )