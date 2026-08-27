"""Define the concrete implementation of the Token Service for generating and validating JWT tokens."""

import logging
from identity.application.service.token_handler import TokenHandler

logging.getLogger(__name__)


class TokenService:
    """Concrete implementation of the Token Service for generating and validating JWT tokens."""
    def __init__(self, token_handler: TokenHandler, token_repository: TokenRepository):
        if not token_handler:
            raise ValueError("TokenHandler cannot be None")
        if not token_repository:
            raise ValueError("TokenRepository cannot be None")
        
        self._token_handler = token_handler
        self._token_repository = token_repository

    def generate_access_token(self, user_id: str) -> str:
        """Generate an access token for a given user ID."""
        pass

    def generate_refresh_token(self, user_id: str) -> str:
        """Generate a refresh token."""
        logging.info("Generating refresh token for user_id: %s", user_id)
        try:
            self._token_handler.generate_refresh_token()
        except ValueError as err:
            logging.error(err)
            raise ValueError(f"Error generating refresh token for user_id: {user_id}, error: {err}")

    def validate_access_token(self, token: str) -> bool:
        """Validate an access token."""
        pass

    def validate_refresh_token(self, token: str) -> bool:
        """Validate a refresh token."""
        pass