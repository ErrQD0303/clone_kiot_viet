"""Authentication event entity module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from shared_kernel.domain.entity.entity import Entity


@dataclass(eq=False, slots=True)
class AuthEvent(Entity[int | None]):
    """AuthEvent entity for authentication and authorization audit logs."""

    event_type: str
    success: bool
    id: int | None = None
    user_id: UUID | None = None
    session_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def identity(self) -> int | None:
        """Return identity used by base entity equality/hash semantics."""
        return self.id

    def __post_init__(self):
        """Validate event payload shape and timestamps."""
        if not self.event_type:
            raise ValueError("event_type must not be empty")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")

        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dict")
