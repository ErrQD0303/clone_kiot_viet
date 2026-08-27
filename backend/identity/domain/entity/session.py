"""Session entity module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID
from typing import TYPE_CHECKING

from identity.domain.entity.refresh_token import RefreshToken
from shared_kernel.domain.entity.entity import AggregateRoot

if TYPE_CHECKING:
    from identity.domain.entity.user import User

@dataclass(eq=False, slots=True)
class Session(AggregateRoot):
    """Session entity representing a user login session."""

    user_id: UUID
    expires_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_seen_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    revoked_at: datetime | None = None
    revoke_reason: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None

    _user: "User" = field(default=None, init=False, repr=False)
    _refresh_token_links: list[RefreshToken] = field(default_factory=list, init=False, repr=False)

    @property
    def User(self) -> "User":
        """Read-only navigation to the user associated with this session."""
        return self._user

    @property
    def RefreshTokenLinks(self) -> tuple[RefreshToken, ...]:
        """Read-only navigation to refresh token links associated with this session."""
        return tuple(self._refresh_token_links)

    def __post_init__(self):
        """Validate invariants for timestamps and revoke metadata."""
        for value in (self.created_at, self.last_seen_at, self.expires_at):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError("session timestamps must be timezone-aware")

        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be later than created_at")

        if self.revoked_at is not None:
            if self.revoked_at.tzinfo is None or self.revoked_at.utcoffset() is None:
                raise ValueError("revoked_at must be timezone-aware")
            if self.revoked_at < self.created_at:
                raise ValueError("revoked_at must be equal to or later than created_at")

        if self.revoke_reason is not None and len(self.revoke_reason) > 50:
            raise ValueError("revoke_reason must be at most 50 characters")

    @classmethod
    def create(cls, user_id: UUID, expires_at: datetime, ip_address: str | None = None, user_agent: str | None = None) -> "Session":
        """Factory method to create a new Session instance."""
        return cls(user_id=user_id, expires_at=expires_at, ip_address=ip_address, user_agent=user_agent)

    def revoke(self, reason: str) -> None:
        """Revoke the session with a given reason."""
        if not reason or len(reason) > 50:
            raise ValueError("reason must be non-empty and at most 50 characters")
        self.revoked_at = datetime.now(UTC)
        self.revoke_reason = reason
        self.update_last_seen()

    def update_last_seen(self) -> None:
        """Update the last seen timestamp for the session."""
        self.last_seen_at = datetime.now(UTC)

    def is_active(self) -> bool:
        """Check if the session is currently active (not revoked and not expired)."""
        now = datetime.now(UTC)
        return self.revoked_at is None and self.expires_at > now

    def is_expired(self) -> bool:
        """Check if the session has expired."""
        now = datetime.now(UTC)
        return self.expires_at <= now

    def is_revoked(self) -> bool:
        """Check if the session has been revoked."""
        return self.revoked_at is not None

    def is_valid(self) -> bool:
        """Check if the session is valid (active and not expired)."""
        return self.is_active() and not self.is_expired()

