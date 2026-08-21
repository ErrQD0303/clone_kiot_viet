"""Password Credential Entity Module"""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared_kernel.domain.entity.entity import AggregateRoot

@dataclass(eq=False, slots=True)
class PasswordCredential(AggregateRoot):
    """PasswordCredential entity representing a user's password credential."""
    password_hash: str
    password_changed_at = field(default_factory=lambda: datetime.now(UTC))
    must_change_password: bool = False
    failed_attempt_count: int = 0
    locked_until: datetime | None = None
    created_at = field(default_factory=lambda: datetime.now(UTC))
    updated_at = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        """Validate password credential invariants."""
        if not self.password_hash:
            raise ValueError("password_hash must not be empty")

        if self.failed_attempt_count < 0:
            raise ValueError("failed_attempt_count must be non-negative")

        for field_name in ("password_changed_at", "created_at", "updated_at"):
            value = getattr(self, field_name)
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{field_name} must be timezone-aware")

        if self.locked_until is not None:
            if self.locked_until.tzinfo is None or self.locked_until.utcoffset() is None:
                raise ValueError("locked_until must be timezone-aware")
