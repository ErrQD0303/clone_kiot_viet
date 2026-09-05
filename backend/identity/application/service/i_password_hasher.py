"""Define the IPasswordHasher Interface for hashing and verifying passwords."""

from typing import Protocol


class IPasswordHasher(Protocol):
    """Interface for Password Hasher."""
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        ...

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        ...