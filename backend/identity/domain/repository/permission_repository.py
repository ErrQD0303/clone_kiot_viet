"""Define the PermissionRepository interface for user-related operations."""
from typing import Protocol

from identity.domain.entity.permission import Permission
from shared_kernel.domain.entity.permission_code import PermissionCode

class PermissionRepository(Protocol):
    """PermissionRepository interface for user-related operations."""

    async def get_by_codes(self, codes: list[PermissionCode]) -> list[Permission]:
        """Get permissions by their unique codes."""

    async def get_by_code(self, code: PermissionCode) -> Permission | None:
        """Get a permission by its unique code."""

    def create(self, permission: Permission) -> None:
        """Create a new permission in the repository."""
