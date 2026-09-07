"""Role entity module"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from identity.domain.authorization.identity_role import IdentityRole
from identity.domain.entity.role_permission import RolePermission
from identity.domain.entity.user_role import UserRole
from shared_kernel.domain.entity.entity import AggregateRoot
from datetime import UTC, datetime

if TYPE_CHECKING:
    from identity.domain.entity.permission import Permission

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

    _permission_links: list["RolePermission"] = field(init=False, repr=False)
    _user_links: list["UserRole"] = field(init=False, repr=False)

    @property
    def PermissionLinks(self) -> tuple["RolePermission", ...]:
        """Read-only navigation to permission links associated with this role."""
        return tuple(self._permission_links)

    @property
    def Permissions(self) -> tuple["Permission", ...]:
        """Read-only navigation to permissions granted to this role."""
        return tuple(link.Permission for link in self._permission_links)

    @property
    def UserLinks(self) -> tuple["UserRole", ...]:
        """Read-only navigation to user links associated with this role."""
        return tuple(self._user_links)

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

    @classmethod
    def create(cls, code: str, name: str, description: str | None = None) -> "Role":
        """Create a new role instance."""
        is_system_role = (
            code == IdentityRole.ADMIN.value
            or name == IdentityRole.ADMIN.name
        )

        return cls(
            code=code,
            name=name,
            description=description,
            is_system=is_system_role,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    def has_permission(self, permission: "Permission") -> bool:
        """Check whether a permission is already granted."""
        return any(existing_permission.code == permission.code for existing_permission in self.Permissions)

    def grant(self, permission: "Permission", granted_user=None) -> bool:
        """Grant a permission to the role once."""
        if self.has_permission(permission):
            return False

        from identity.domain.entity.role_permission import RolePermission

        permission_link = RolePermission(
            role_id=self.identify(),
            permission_id=permission.identify(),
            granted_at=datetime.now(UTC),
            granted_by=granted_user,
        )
        permission_link._role = self
        permission_link._permission = permission
        self._permission_links.append(permission_link)
        self.updated_at = datetime.now(UTC)
        return True
