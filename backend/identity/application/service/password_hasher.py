"""Define the Password Hasher for hashing and verifying passwords."""
from pwdlib import PasswordHash

class PasswordHasher:
    """Password Hasher for hashing and verifying passwords."""
    def __init__(self, password_hash):
        self._password_hash = password_hash

    def hash_password(self, password: str) -> str:
        """Hash a password using the specified hashing strategy."""
        if not password:
            raise ValueError("Password cannot be empty.")

        return self._password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password using the specified hashing strategy."""
        if not password or not hashed_password:
            raise ValueError("Password and hashed password cannot be empty.")

        return self._password_hash.verify(password, hashed_password)