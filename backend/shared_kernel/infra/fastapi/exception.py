"""Define the Exception module for FastAPI applications."""

DEFAULT_PASSWORD_STRENGTH_ERROR_MESSAGE = (
    "Password does not meet strength requirements. "
    "Password must be 8-128 characters long, contain at least one uppercase letter, "
    "one lowercase letter, one digit, and one special character (!@#$%&*?)."
)

class PasswordStrengthError(Exception):
    """Custom exception for password strength validation errors."""
    def __init__(self, message: str = DEFAULT_PASSWORD_STRENGTH_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)