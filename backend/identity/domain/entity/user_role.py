"""User Role entity module"""
from dataclasses import dataclass, field
from uuid import UUID
from shared_kernel.domain.entity.entity import Entity
from datetime import UTC, datetime

# This represents a composite key in the database, combining user_id and role_id to uniquely identify a user role.
@dataclass(eq=False, slots=True)
class UserRoleId:
    """UserRoleId value object representing the identity of a user role."""
    user_id: UUID
    role_id: UUID

    def __post_init__(self):
        """Validate composite key values."""
        if self.user_id is None:
            raise ValueError("user_id must not be None")

        if self.role_id is None:
            raise ValueError("role_id must not be None")

@dataclass(eq=False, slots=True)
class UserRole(Entity[UserRoleId]):
    """User Role entity representing a relation between a user and a role in a system."""
    user_id: UUID
    role_id: UUID 
    assigned_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    assigned_by: UUID | None = None
    expires_at: datetime | None = None

    def __post_init__(self):
        """Post-initialization to ensure the identity is set correctly."""
        if self.assigned_at.tzinfo is None or self.assigned_at.utcoffset() is None:
            raise ValueError("assigned_at must be timezone-aware")

        if self.expires_at is not None and self.expires_at <= self.assigned_at:
            raise ValueError("expires_at must be later than assigned_at")

    @property
    def identify(self) -> UUID:
            """Get the identity of the entity."""
            return UserRoleId(user_id=self.user_id, role_id=self.role_id)

