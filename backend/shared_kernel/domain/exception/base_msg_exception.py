"""Define the BaseMsgException class for exceptions with a message."""

class BaseMsgException(Exception):
    """Base class for exceptions with a message."""
    message: str

    def __str__(self):
        return self.message
