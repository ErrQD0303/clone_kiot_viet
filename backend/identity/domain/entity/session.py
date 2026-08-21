"""Session entity module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from shared_kernel.domain.entity.entity import AggregateRoot


@dataclass(eq=False, slots=True)
class Session(AggregateRoot):
    """Session entity representing a user login session."""

    user_id: UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_seen_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime
    revoked_at: datetime | None = None
    revoke_reason: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None

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
