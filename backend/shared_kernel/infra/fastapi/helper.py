"""Define the helpers for FastAPI applications."""

# Decorators
# as_form: A decorator to convert a Pydantic model into a form data model for FastAPI endpoints.
from functools import wraps
import inspect
from typing import Any, Awaitable, Callable, TypeVar

from pydantic import BaseModel
from fastapi import Form
import logging

META_MAPPING_DICT = {
    "MinLen": "min_length",
    "MaxLen": "max_length",
    "Pattern": "pattern",
    "Gt": "gt",
    "Ge": "ge",
    "Lt": "lt",
    "Le": "le",
}

ModelType = TypeVar("ModelType", bound=BaseModel)

def as_form(cls: type[ModelType]) -> type[ModelType]:
    """
    A decorator to convert a Pydantic model into a form data model for FastAPI endpoints.

    This decorator adds a class method `as_form` to the Pydantic model, which allows
    the model to be used as a form data model in FastAPI endpoints.

    Args:
        cls (type[ModelType]): The Pydantic model class to be converted.

    Returns:
        type[ModelType]: The modified Pydantic model class with the `as_form` method.
    """
    new_parameters: list[inspect.Parameter] = []

    for field_name, model_field in cls.model_fields.items():
        is_required = model_field.is_required()
        default_value = ... if is_required else model_field.default

        field_description = model_field.description

        form_kwargs: dict[str, Any] = {
            "description": field_description,
        }

        for meta in model_field.metadata:
            meta_cls_name = meta.__class__.__name__

            if meta_cls_name in META_MAPPING_DICT and hasattr(meta, META_MAPPING_DICT[meta_cls_name]):
               form_kwargs[META_MAPPING_DICT[meta_cls_name]] = getattr(meta, META_MAPPING_DICT[meta_cls_name])

        new_parameters.append(
            inspect.Parameter(
                name=field_name,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, # Allow the parameter to be passed as a positional or keyword argument
                default=Form(default_value, **form_kwargs), # Use Form to indicate that this parameter should be extracted from form data
                annotation=model_field.annotation, # The type of the field, e.g., str, int, etc.
            )
        )

    def as_form_func(**kwargs):
        return cls(**kwargs)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig

    cls.as_form = as_form_func
    return cls

logger = logging.getLogger(__name__)

Endpoint = TypeVar("Endpoint", bound=Callable[..., Awaitable[Any]]) # Callable[..., Awaitable[Any]] represents an asynchronous function that can take any number of arguments and returns an awaitable result.
def log_endpoint_errors(endpoint: Endpoint) -> Endpoint:
    """A decorator to log errors in FastAPI endpoints."""
    @wraps(endpoint)
    async def wrapper(*args, **kwargs):
        try:
            return await endpoint(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in endpoint {endpoint.__name__}: {str(e)}")
            raise

    return wrapper