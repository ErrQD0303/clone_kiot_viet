"""Define the PyJWT Token Handler for generating and validating JWT tokens. for generating and validating JWT tokens."""

import datetime
import secrets
import logging

from identity.application.service.hash_strategy import HashStrategyFactory
from identity.application.service.models.token import CreatedRefreshToken
from identity.application.service.token_handler import TokenHandler

logging.getLogger(__name__)


class PyJWTTokenHandler:
    """PyJWT Token Handler for generating and validating JWT tokens."""
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expiration_minute: int = 30, refresh_token_expiration_minute: int = 14400, token_type: str = "Bearer"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expiration_minute = access_token_expiration_minute
        self.refresh_token_expiration_minute = refresh_token_expiration_minute
        self.token_type = token_type

    def generate_access_token(self, user_id: str) -> str:
        """Generate an access token for a given user ID."""
        # Implementation for generating access token using PyJWT


    def generate_refresh_token(self) -> str:
        """Generate a refresh token."""
        # Implementation for generating refresh token using PyJWT
        try:
            # 1. Generate a random 64-character hex string
            raw_token = secrets.token_hex(32)

            # 2. Hash the token before storing it in your database)
            token_hash = HashStrategyFactory.get_strategy(self.algorithm).hash_token(raw_token)

            # 3. Calculate the expiration time for the refresh token
            expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=self.refresh_token_expiration_minute)

            return CreatedRefreshToken(
                refresh_token=raw_token,
                expires_at=int(expires_at.timestamp())
            )
        except ValueError as err:
            logging.error(err)

            # We can raise a custom exception here if needed, or handle it as per your application's requirements
            raise ValueError(f"Error generating refresh token with algorithm {self.algorithm}, error: {err}")
        

    def validate_access_token(self, token: str) -> bool:
        """Validate an access token."""
        # Implementation for validating access token using PyJWT
        pass

    def validate_refresh_token(self, token: str) -> bool:
        """Validate a refresh token."""
        # Implementation for validating refresh token using PyJWT
        pass

def get_token_handler(secret_key: str, algorithm: str = "HS256", access_token_expiration_minute: int = 30, refresh_token_expiration_minute: int = 14400, token_type: str = "Bearer") -> TokenHandler:
    """Dependency injection for PyJWTTokenService."""
    return PyJWTTokenHandler(secret_key, algorithm, access_token_expiration_minute, refresh_token_expiration_minute, token_type)
            