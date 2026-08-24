"""Define Permission Code entities for Shared Kernel"""
import re
from dataclasses import dataclass

PERMISSION_PATTERN_STR = r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}$"

_PERMISSION_PATTERN = re.compile(PERMISSION_PATTERN_STR)

@dataclass(frozen=True, slots=True, order=True)
class PermissionCode:
    """PermissionCode value object representing a permission code in the system."""
    value: str

    def __post_init__(self):
        """Validate the permission code format."""
        if not _PERMISSION_PATTERN.fullmatch(self.value):
            raise ValueError(
                f"Invalid permission code format: {self.value}. "
                "Expected format: 'module.submodule.permission'."
            )

    def __str__(self) -> str:
        """Return the string representation of the permission code."""
        return self.value