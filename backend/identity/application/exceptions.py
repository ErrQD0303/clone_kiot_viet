"""Define the exceptions for the identity application."""


class UserNotFoundError(Exception):
    """Raise this exception when a user is not exists in the repository."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found."
        super().__init__(self.message)

    def __init__(self, username: str):
        self.username = username
        self.message = f"User with username {username} not found."
        super().__init__(self.message)

class InvalidCredentialError(Exception):
    """Raise this exception when a user provides invalid credentials."""

    def __init__(self, username: str):
        self.username = username
        self.message = f"Invalid credentials provided for username {username}."
        super().__init__(self.message)

class InvalidAccessTokenError(Exception):
    """Raise this exception when an access token is invalid."""

    def __init__(self, token: str | None = None):
        self.token = token
        self.message = f"Invalid access token: {token}." if token else "No access token provided."
        super().__init__(self.message)

class TokenGenerationError(Exception):
    """Raise this exception when there is an error generating a token."""

    def __init__(self, user_id: str, error: BaseException):
        self.user_id = user_id
        self.error = error
        self.message = f"Error generating token for user with ID {user_id}: {error}"
        super().__init__(self.message)

class AccountNotActiveError(Exception):
    """Raise this exception when an account cannot be used for authentication."""

    def __init__(self, username: str):
        self.username = username
        self.message = f"Account with username {username} is not active."
        super().__init__(self.message)