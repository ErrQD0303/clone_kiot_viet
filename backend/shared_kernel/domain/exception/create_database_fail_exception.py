"""Shared Kernel domain exception for database creation failure."""

class CreateDatabaseFailException(Exception):
    """Exception raised when database creation fails."""
    def __init__(self, message: str = "Failed to create the database."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
