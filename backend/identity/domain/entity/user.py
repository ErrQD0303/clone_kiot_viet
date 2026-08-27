"""User entity module"""
from dataclasses import dataclass, field
from identity.domain.entity.session import Session
from identity.domain.entity.user_role import UserRole
from shared_kernel.domain.entity.entity import AggregateRoot
from identity.domain.entity.user_status import UserStatus
from datetime import UTC, datetime

# Turn off the equality comparison and hash generation for the User class
@dataclass(eq=False, slots=True)
class User(AggregateRoot):
    """User entity representing a user in the system."""
    username: str
    email: str
    status: UserStatus
    auth_version: int
    display_name: str | None = None
    email_verified_at: datetime | None = None
    last_login_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    _role_links: list["UserRole"] = field(default_factory=list, init=False, repr=False)
    _session_links: list["Session"] = field(default_factory=list, init=False, repr=False)

    @property
    def RoleLinks(self) -> tuple["UserRole", ...]:
        """Read-only navigation to role links associated with this user."""
        return tuple(self._role_links)

    @property
    def SessionLinks(self) -> tuple["Session", ...]:
        """Read-only navigation to session links associated with this user."""
        return tuple(self._session_links)

    @property
    def Roles(self) -> tuple[str, ...]:
        """Get the roles associated with this user."""
        return tuple(role_link.Role.name for role_link in self._role_links)

    @property
    def RefreshTokens(self) -> tuple[str, ...]:
        """Get the refresh tokens associated with this user."""
        tokens = []
        for session in self._session_links:
            for refresh_token in session.RefreshTokenLinks:
                tokens.append(refresh_token.token_hash.hex())
        return tuple(tokens)

    def __post_init__(self):
        """Validate core user invariants."""
        if not self.username:
            raise ValueError("username must not be empty")

        if not self.email:
            raise ValueError("email must not be empty")

        if self.auth_version <= 0:
            raise ValueError("auth_version must be greater than 0")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")

        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("updated_at must be timezone-aware")

        if self.email_verified_at is not None:
            if self.email_verified_at.tzinfo is None or self.email_verified_at.utcoffset() is None:
                raise ValueError("email_verified_at must be timezone-aware")

        if self.last_login_at is not None:
            if self.last_login_at.tzinfo is None or self.last_login_at.utcoffset() is None:
                raise ValueError("last_login_at must be timezone-aware")
