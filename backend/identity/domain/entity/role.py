"""Role entity module"""
from dataclasses import dataclass, field
from shared_kernel.domain.entity.entity import AggregateRoot
from datetime import UTC, datetime

# Turn off the equality comparison and hash generation for the User class
@dataclass(eq=False, slots=True)
class Role(AggregateRoot):
    """Role entity representing a role belonged to a user entity in a system."""
    code: str
    name: str
    description: str | None = None
    is_system: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        """Validate role invariants."""
        if not self.code:
            raise ValueError("code must not be empty")

        if not self.name:
            raise ValueError("name must not be empty")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")

        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("updated_at must be timezone-aware")
