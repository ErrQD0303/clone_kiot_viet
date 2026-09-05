"""Define the Principal security object for identity management."""

from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class Principal:
    user_id: UUID
    username: str
    email: str
    status: str
    roles: frozenset[str]
    permissions: frozenset[str]
    display_name: str | None = None
    session_id: UUID | None = None

    def has_role(self, role: str) -> bool:
        """Check if the principal has a specific role."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Check if the principal has a specific permission."""
        return permission in self.permissions