"""Permission entity module"""
from dataclasses import dataclass, field
from shared_kernel.domain.entity.entity import AggregateRoot
from datetime import UTC, datetime

from shared_kernel.domain.entity.permission_code import PermissionCode
from identity.domain.entity.role_permission import RolePermission

# Turn off the equality comparison and hash generation for the User class
@dataclass(eq=False, slots=True)
class Permission(AggregateRoot):
    """Permission entity representing a permission belonged to a user entity in a system."""
    code: PermissionCode
    description: str | None = None
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    _role_links: list["RolePermission"] = field(init=False, repr=False)

    @property
    def RoleLinks(self) -> tuple["RolePermission", ...]:
        """Read-only navigation to role links associated with this permission."""
        return tuple(self._role_links)

    def __post_init__(self):
        """Validate permission invariants."""
        if not self.code:
            raise ValueError("code must not be empty")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")

        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("updated_at must be timezone-aware")

    @classmethod
    def create(cls, code: str, description: str | None = None) -> "Permission":
        """Factory method to create a new Permission instance."""
        return cls(code=code, description=description)

    def change_description(self, new_description: str | None):
        """Change the description of the permission."""
        self.description = new_description
        self.updated_at = datetime.now(UTC)
