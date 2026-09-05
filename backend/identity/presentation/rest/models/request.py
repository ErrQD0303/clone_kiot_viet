"""Define the Request Models for identity management."""

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field

from shared_kernel.infra.fastapi.helper import as_form
from shared_kernel.infra.fastapi.model.annotated import StrongPassword
from shared_kernel.infra.fastapi.regex_constant import PASSWORD_REGEX

@as_form
class LoginFormRequest(BaseModel):
    """Define the login form request model for identity management."""
    model_config = ConfigDict(
        extra="forbid",
    )
    
    username: str = Field(..., description="The username of the user.")
    password: StrongPassword = Field(..., description="The password of the user.", min_length=8, max_length=128)