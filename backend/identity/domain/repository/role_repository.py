"""Define the RoleRepository interface for role-related operations."""
from typing import Protocol

from identity.domain.entity.role import Role

class RoleRepository(Protocol):
    """RoleRepository interface for role-related operations."""

    async def get_by_names(self, names: set[str]) -> list[Role]:
        """Get roles by their unique names."""

    async def get_by_codes(self, codes: list[str]) -> list[Role]:
        """Get roles by their unique codes."""

    def create(self, role: Role) -> None:
        """Create a new role in the repository."""
