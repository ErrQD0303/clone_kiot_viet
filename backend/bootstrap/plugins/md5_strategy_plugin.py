"""Define the MD5Strategy for hashing tokens using the MD5 algorithm."""
import hashlib

from identity.application.service.hash_strategy import register_algorithm

@register_algorithm("MD5")
class MD5Strategy:
    """MD5Strategy for hashing tokens using the MD5 algorithm."""
    def hash_token(self, token: str) -> str:
        """Hash the token using the MD5 algorithm."""
        return hashlib.md5(token.encode()).hexdigest()