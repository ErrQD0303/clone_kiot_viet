"""Define the Models that are used in FastAPI applications."""

from typing import Annotated

from pydantic import SecretStr, AfterValidator

from shared_kernel.infra.fastapi.exception import PasswordStrengthError
from shared_kernel.infra.fastapi.regex_constant import PASSWORD_REGEX

def check_password_strength(s: SecretStr) -> SecretStr:
    if not PASSWORD_REGEX.match(s.get_secret_value()):
        raise PasswordStrengthError()
    return s

StrongPassword = Annotated[SecretStr, AfterValidator(check_password_strength)]