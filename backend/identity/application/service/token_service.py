"""Define the Token Service interface for generating and validating JWT tokens."""

from collections.abc import Callable
from typing import Protocol, TypeVar
from uuid import UUID

from identity.application.service.models.token import Token
from identity.application.service.token_handler import TokenHandler
from identity.domain.entity.session import Session
from identity.domain.repository.refreshtoken_repository import RefreshTokenRepository
from identity.domain.repository.session_repository import SessionRepository
from shared_kernel.domain.unit_of_work import UnitOfWork
from shared_kernel.presentation.dependencies.principal import Principal

TTokenService = TypeVar("TTokenService", bound="TokenService")


class TokenService(Protocol):
    """Token Service"""
    async def issue_token_pair_for_session(self, principal: Principal, session: Session) -> Token:
        """Issue a new token pair (access and refresh tokens) for a given user's session."""
        ...

    async def issue_token_pair(self, principal: Principal, ip_address: str | None, user_agent: str | None) -> Token:
        """Issue a new token pair (access and refresh tokens) for a new user's session."""
        ...

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

def get_token_service(
        implementation: Callable[
            [TokenHandler, RefreshTokenRepository], TTokenService
        ],
        token_handler: TokenHandler,
        refresh_token_repository: RefreshTokenRepository,
        session_repository: SessionRepository,
        unit_of_work: UnitOfWork,
        issuer: str,
        audience: str
) -> TTokenService:
    """Factory function to create a TokenService instance."""
    return implementation(token_handler, refresh_token_repository, session_repository, unit_of_work, issuer, audience)