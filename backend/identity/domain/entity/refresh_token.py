"""Refresh token entity module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from shared_kernel.domain.entity.entity import AggregateRoot


@dataclass(eq=False, slots=True)
class RefreshToken(AggregateRoot):
    """RefreshToken entity used for token rotation and revocation."""

    session_id: UUID
    token_hash: bytes
    expires_at: datetime
    parent_token_id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    used_at: datetime | None = None
    revoked_at: datetime | None = None

    def __post_init__(self):
        """Validate hash and timestamp constraints."""
        if len(self.token_hash) != 32:
            raise ValueError("token_hash must be exactly 32 bytes")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
            raise ValueError("expires_at must be timezone-aware")

        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be later than created_at")

        if self.used_at is not None:
            if self.used_at.tzinfo is None or self.used_at.utcoffset() is None:
                raise ValueError("used_at must be timezone-aware")
            if self.used_at < self.created_at:
                raise ValueError("used_at must be equal to or later than created_at")

        if self.revoked_at is not None:
            if self.revoked_at.tzinfo is None or self.revoked_at.utcoffset() is None:
                raise ValueError("revoked_at must be timezone-aware")
            if self.revoked_at < self.created_at:
                raise ValueError("revoked_at must be equal to or later than created_at")
