"""Define the PyJWT Token Handler for generating and validating JWT tokens. for generating and validating JWT tokens."""

import datetime
import secrets
import logging

import jwt

from identity.application.service.hash_strategy import HashStrategyFactory
from identity.application.service.models.token import AccessTokenPayload, CreatedAccessToken, CreatedRefreshToken, TokenData
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

    def generate_access_token(self, data: TokenData, issuer: str, audience: str, expired_in_minute: int | None = None) -> CreatedAccessToken:
        """Generate an access token for a given user ID."""
        # Implementation for generating access token using PyJWT
        # 1. Create the payload for the access token
        payload: AccessTokenPayload = AccessTokenPayload(
            sub=str(data.user_id),
            username=data.username,
            email=data.email,
            account_status=data.status,
            display_name=data.display_name,
            roles=data.roles,
            permissions=data.permissions,
            iss=issuer,
            aud=audience,
            iat=int(datetime.datetime.now(datetime.UTC).timestamp()),
            exp=int((datetime.datetime.now(datetime.UTC) + (datetime.timedelta(minutes=expired_in_minute) if expired_in_minute else datetime.timedelta(minutes=self.access_token_expiration_minute))).timestamp()),
            sid=data.session_id
        )

        # 2. Encode the payload to generate the access token
        access_token = jwt.encode(payload.model_dump(mode="json"), self.secret_key, algorithm=self.algorithm)

        return CreatedAccessToken(
            access_token=access_token,
            expires_at=payload.exp,
            token_type=self.token_type
        )


    def generate_refresh_token(self, expired_in_minute: int | None = None) -> CreatedRefreshToken:
        """Generate a refresh token."""
        # Implementation for generating refresh token using PyJWT
        try:
            # 1. Generate a random 64-character hex string
            raw_token = secrets.token_hex(32)

            # 2. Hash the token before storing it in your database)
            token_hash = HashStrategyFactory.get_strategy(self.algorithm).hash_token(raw_token)

            # 3. Calculate the expiration time for the refresh token
            expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expired_in_minute if expired_in_minute else self.refresh_token_expiration_minute)

            return CreatedRefreshToken(
                refresh_token=raw_token,
                expires_at=int(expires_at.timestamp())
            )
        except ValueError as err:
            logging.error(err)

            # We can raise a custom exception here if needed, or handle it as per your application's requirements
            raise ValueError(f"Error generating refresh token with algorithm {self.algorithm}, error: {err}")
        

    def validate_access_token(self, token: str, valid_issuer: str, valid_audience: str) -> tuple[bool, TokenData | None]:
        """Validate an access token."""
        # Implementation for validating access token using PyJWT
        try:
            # 1. Decode the token to get the payload
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], issuer=valid_issuer, audience=valid_audience)

            # 2. Create a TokenData object from the payload
            token_data = TokenData(
                user_id=payload.get("sub"),
                username=payload.get("username"),
                email=payload.get("email"),
                status=payload.get("account_status"),
                display_name=payload.get("display_name"),
                roles=frozenset(payload.get("roles", [])),
                permissions=frozenset(payload.get("permissions", [])),
                session_id=payload.get("sid")
            )

            if not token_data.user_id:
                raise jwt.MissingRequiredClaimError("sub")

            if not token_data.session_id:
                raise jwt.MissingRequiredClaimError("sid")

            return True, token_data
        except jwt.MissingRequiredClaimError as e:
            logging.warning(f"Access token is missing required claims: {e.claim}.")
            return False, None
        except jwt.ExpiredSignatureError:
            logging.warning("Access token has expired.")
            return False, None
        except jwt.InvalidTokenError:
            logging.warning("Invalid access token.")
            return False, None

    def validate_refresh_token(self, token: str) -> bool:
        """Validate a refresh token."""
        # Implementation for validating refresh token using PyJWT
        pass

def get_token_handler(secret_key: str, algorithm: str = "HS256", access_token_expiration_minute: int = 30, refresh_token_expiration_minute: int = 14400, token_type: str = "Bearer") -> TokenHandler:
    """Dependency injection for PyJWTTokenService."""
    return PyJWTTokenHandler(secret_key, algorithm, access_token_expiration_minute, refresh_token_expiration_minute, token_type)
            