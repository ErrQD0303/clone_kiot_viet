"""Define the Application Authentication Service for user authentication and session management."""

from datetime import UTC, datetime

from identity.application.exceptions import AccountNotActiveError, InvalidCredentialError
from identity.application.service.i_password_hasher import IPasswordHasher
from identity.application.service.models.token import Token
from identity.application.service.token_service import TokenService
from identity.domain.entity.password_credential import PasswordCredential
from identity.domain.entity.session import Session
from identity.domain.entity.user_status import UserStatus
from identity.domain.repository.session_repository import SessionRepository
from identity.domain.repository.user_repository import UserRepository
from shared_kernel.domain.unit_of_work import UnitOfWork
from shared_kernel.infra.fastapi.config import Setting
from shared_kernel.presentation.dependencies.principal import Principal
import logging

logger = logging.getLogger(__name__)


class ApplicationAuthenticationService:
    """Application Authentication Service for user authentication and session management."""

    def __init__(
        self,
        session_repository: SessionRepository,
        token_service: TokenService,
        user_repository: UserRepository,
        unit_of_work: UnitOfWork,
        password_hasher: IPasswordHasher,
        setting: Setting
    ):
        self._session_repository = session_repository
        self._token_service = token_service
        self._user_repository = user_repository
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    def _is_valid_password_credential(self, user_status: UserStatus, credential: PasswordCredential) -> bool:
        now = datetime.now(UTC)
        return credential is not None and (
                credential.locked_until is None or credential.locked_until <= now
            ) and user_status == UserStatus.ACTIVE

    async def login_by_username(
        self, username: str, password: str, ip_address: str | None = None, user_agent: str | None = None
    ) -> Token:
        """Authenticate a user and return a token pair (access and refresh tokens)."""
        async with self._unit_of_work:
            user = await self._user_repository.get_user_by_username(
                username=username,
                with_roles=True,
                with_password_credential=True,
            )

            if user is None:
                raise InvalidCredentialError()

            credential = user.PasswordCredential
            if not self._is_valid_password_credential(user.status, credential):
                raise AccountNotActiveError(username=username)

            if not self._password_hasher.verify_password(
                password,
                credential.password_hash,
            ):
                raise InvalidCredentialError(username=username)

            current_user_valid_sessions = await self._session_repository.get_current_valid_sessions(user.id)
            if current_user_valid_sessions and len(current_user_valid_sessions) > 0:
                # If a valid session exists, first check the cache for the token pair associated with that session. If found, return it. If not found, issue a new token pair for the existing session.
                # If more than one valid session exists, you may choose to handle it according to your application's requirements (e.g., return the most recent session, or handle multiple sessions differently).
                logger.info(f"User {user.username} has {len(current_user_valid_sessions)} valid sessions. Revoking all but the most recent session.")
                for i in range(1, len(current_user_valid_sessions)):
                    current_user_valid_sessions[i].revoke(reason="More than one valid session for user")  # Revoke all but the most recent valid session

                current_user_valid_session = current_user_valid_sessions[0]  # Get the most recent valid session

                # Add cache retrieval logic here (not implemented in this snippet)

                # If not found in cache, issue a new token pair for the existing session
                principal = Principal(
                    user_id=user.id,
                    username=user.username,
                    email=user.email,
                    status=user.status,
                    display_name=user.display_name,
                    roles=frozenset(role_link.Role.code for role_link in user.RoleLinks),
                    permissions=frozenset(),
                    session_id=current_user_valid_session.id  # Associate the principal with the existing session ID
                )
                
                return await self._token_service.issue_token_pair_for_session(
                    principal=principal,
                    session=current_user_valid_session
                )
            
            principal = Principal(
                user_id=user.id,
                username=user.username,
                email=user.email,
                status=user.status,
                display_name=user.display_name,
                roles=frozenset(role_link.Role.code for role_link in user.RoleLinks),
                permissions=frozenset(),
            )

            return await self._token_service.issue_token_pair(
                principal=principal,
                ip_address=ip_address,
                user_agent=user_agent,
            )

    async def logout(self, session_id: str) -> None:
        """Logout a user by revoking the session and associated tokens."""
        await self._token_service.revoke_session(session_id)