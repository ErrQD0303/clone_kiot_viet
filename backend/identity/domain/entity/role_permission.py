"""Role Permission entity module"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID
from shared_kernel.domain.entity.entity import Entity
from datetime import UTC, datetime

if TYPE_CHECKING:
    from identity.domain.entity.role import Role
    from identity.domain.entity.permission import Permission

# This represents a composite key in the database, combining user_id and role_id to uniquely identify a user role.
@dataclass(eq=False, slots=True)
class RolePermissionId:
    """RolePermissionId value object representing the identity of a role permission."""
    role_id: UUID
    permission_id: UUID

    def __post_init__(self):
        """Validate composite key values."""
        if self.permission_id is None:
            raise ValueError("permission_id must not be None")

        if self.role_id is None:
            raise ValueError("role_id must not be None")

@dataclass(eq=False, slots=True)
class RolePermission(Entity[RolePermissionId]):
    """Role Permission entity representing a relation between a permission and a role in a system."""
    role_id: UUID
    permission_id: UUID
    granted_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    granted_by: UUID | None = None
    
    _role: Role | None = field(default=None, init=False, repr=False)
    _permission: Permission | None = field(default=None, init=False, repr=False)

    @property
    def Role(self) -> Role | None:
        """Read-only navigation to the role associated with this permission."""
        return self._role

    @property
    def Permission(self) -> Permission | None:
        """Read-only navigation to the permission associated with this role."""
        return self._permission
    
    def __post_init__(self):
        """Post-initialization to ensure the identity is set correctly."""
        if self.granted_at.tzinfo is None or self.granted_at.utcoffset() is None:
            raise ValueError("granted_at must be timezone-aware")

    @property
    def identify(self) -> UUID:
            """Get the identity of the entity."""
            return RolePermissionId(permission_id=self.permission_id, role_id=self.role_id)

