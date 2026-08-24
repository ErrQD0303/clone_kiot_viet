"""Define Permission Code's Definition entities for Shared Kernel"""
from dataclasses import dataclass

from shared_kernel.domain.entity.permission_code import PermissionCode

@dataclass(frozen=True, slots=True)
class PermissionDefinition:
    """PermissionDefinition value object representing a permission code' description."""
    code: PermissionCode
    description: str
