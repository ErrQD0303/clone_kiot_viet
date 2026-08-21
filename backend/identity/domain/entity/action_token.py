"""Action token entity module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from shared_kernel.domain.entity.entity import AggregateRoot


ALLOWED_ACTION_TOKEN_PURPOSES = ("verify_email", "reset_password")


@dataclass(eq=False, slots=True)
class ActionToken(AggregateRoot):
    """ActionToken entity for one-time user actions."""

    user_id: UUID
    purpose: str
    token_hash: bytes
    expires_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    consumed_at: datetime | None = None
    requested_ip: str | None = None

    def __post_init__(self):
        """Validate purpose, hash and timestamp constraints."""
        if self.purpose not in ALLOWED_ACTION_TOKEN_PURPOSES:
            raise ValueError(
                f"purpose must be one of {ALLOWED_ACTION_TOKEN_PURPOSES}, got {self.purpose!r}"
            )

        if len(self.token_hash) != 32:
            raise ValueError("token_hash must be exactly 32 bytes")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
            raise ValueError("expires_at must be timezone-aware")

        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be later than created_at")

        if self.consumed_at is not None:
            if self.consumed_at.tzinfo is None or self.consumed_at.utcoffset() is None:
                raise ValueError("consumed_at must be timezone-aware")
            if self.consumed_at < self.created_at:
                raise ValueError("consumed_at must be equal to or later than created_at")
