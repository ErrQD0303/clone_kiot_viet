"""Define the Database Token Service for generating and validating JWT tokens."""

from datetime import UTC, datetime, timedelta
from typing import Protocol
from uuid import UUID

from identity.application.service.models.token import Token, TokenData
from identity.application.service.token_handler import TokenHandler
from identity.domain.entity.session import Session
from identity.domain.repository.refreshtoken_repository import RefreshTokenRepository
from identity.domain.repository.session_repository import SessionRepository
from shared_kernel.domain.unit_of_work import UnitOfWork
from shared_kernel.presentation.dependencies.principal import Principal
from shared_kernel.infra.fastapi.config import settings
import logging

logging.getLogger(__name__)


class DatabaseTokenService:
    """Database Token Service for generating and validating JWT tokens."""
    def __init__(self, token_handler: TokenHandler, refresh_token_repository: RefreshTokenRepository, session_repository: SessionRepository, unit_of_work: UnitOfWork, issuer: str, audience: str):
        self._token_handler = token_handler
        self._refresh_token_repository = refresh_token_repository
        self._session_repository = session_repository
        self._unit_of_work = unit_of_work
        self._issuer = issuer
        self._audience = audience

    async def issue_token_pair(self, principal: Principal, ip_address: str | None, user_agent: str | None) -> Token:
        """Issue a new token pair (access and refresh tokens) for a given user's session."""
        logging.info(f"Issuing token pair for user_id: {principal.user_id}")

        # Retrieve the existing session for the user

        # Create a new session for the user
        new_session = Session.create(user_id=principal.user_id,
                           ip_address=ip_address,
                           user_agent=user_agent,
                           session_expired_minute=settings.SESSION_EXPIRE_MINUTES)
        await self._session_repository.save(new_session)
        await self._unit_of_work.flush()  # Ensure the session is saved before proceeding

        # Generate a refresh token
        refresh_token = self._token_handler.generate_refresh_token()

        # Create token data for the access token
        token_data = TokenData(
            user_id=str(principal.user_id),
            username=principal.username,
            email=principal.email,
            status=principal.status,
            display_name=principal.display_name,
            roles=principal.roles,
            permissions=principal.permissions,
            session_id=str(new_session.id)  # Associate the access token with the session ID
        )

        # Generate an access token
        access_token = self._token_handler.generate_access_token(token_data, self._issuer, self._audience)

        # Save the refresh token in the repository
        await self._refresh_token_repository.save_token(
            session=new_session,
            refresh_token=refresh_token.refresh_token,
            parent_token=None,  # No parent token for the initial issuance
            expires_time=refresh_token.expires_at
        )

        return Token(
            access_token=access_token.access_token,
            refresh_token=refresh_token.refresh_token,
            token_type=access_token.token_type,
            expires_in=access_token.expires_at - int(datetime.now(UTC).timestamp()),
            refresh_expires_at=refresh_token.expires_at
        )

    async def issue_token_pair_for_session(self, principal: Principal, session: Session) -> Token:
        """Issue a new token pair (access and refresh tokens) for a given user's session."""
        logging.info(f"Issuing token pair for user_id: {principal.user_id}, session_id: {principal.session_id}")

        current_refresh_token = await self._refresh_token_repository.get_token_by_session(session.id)

        current_refresh_token.revoke()  # Mark the current refresh token as revoked because a new token pair is being issued, and we want to ensure that the old refresh token cannot be used to obtain new access tokens.

        await self._unit_of_work.flush()  # Ensure the token revocation is saved before proceeding, we do not need to save the revoked token because it is already in the database, we just need to update it.

        refresh_token_expired_in_minute = min(settings.REFRESH_TOKEN_EXPIRE_MINUTES, (session.expires_at - datetime.now(UTC)).total_seconds() // 60)
        
        refresh_token = self._token_handler.generate_refresh_token(expired_in_minute=refresh_token_expired_in_minute)

        token_data = TokenData(
            user_id=str(principal.user_id),
            username=principal.username,
            email=principal.email,
            status=principal.status,
            display_name=principal.display_name,
            roles=principal.roles,
            session_id=str(principal.session_id)  # Associate the access token with the session ID
        )

        access_token_expired_in_minute = min(settings.ACCESS_TOKEN_EXPIRE_MINUTES, (session.expires_at - datetime.now(UTC)).total_seconds() // 60)
        
        access_token = self._token_handler.generate_access_token(token_data, self._issuer, self._audience, expired_in_minute=access_token_expired_in_minute)

        await self._refresh_token_repository.save_token(
            session=session,
            refresh_token=refresh_token.refresh_token,
            parent_token=None,  # No parent token for the initial issuance
            expires_time=refresh_token.expires_at
        )

        return Token(
            access_token=access_token.access_token,
            refresh_token=refresh_token.refresh_token,
            token_type=access_token.token_type,
            expires_in=access_token.expires_at - int(datetime.now(UTC).timestamp()),
            refresh_expires_at=refresh_token.expires_at
        )

    def validate_access_token(self, token: str) -> Principal:
        """Validate an access token and return the associated principal."""
        ...

    def revoke_refresh_token(self, refresh_token: str) -> None:
        """Revoke a refresh token."""
        ...

    def revoke_session(self, session_id: UUID) -> None:
        """Revoke all tokens associated with a given session ID."""
        ...

    def refresh_token_pair(self, refresh_token: str) -> Token:
        """Refresh the token pair (access and refresh tokens) using a valid refresh token."""
        ...
