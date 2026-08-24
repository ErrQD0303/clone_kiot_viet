"""Define the PermissionCodeType for database representation of permission codes."""
from sqlalchemy import TEXT
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

from shared_kernel.domain.entity.permission_code import PermissionCode

class PermissionCodeType(TypeDecorator[PermissionCode]):
    """Map PermissionCode between the domain and database."""
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value: PermissionCode | None, dialect: Dialect) -> str | None:
        """Convert PermissionCode to TEXT for database storage."""

        if value is None:
            return None
        
        if not isinstance(value, PermissionCode):
            raise TypeError(
                "PermissionCodeType expects PermissionCode,",
                f"received {type(value).__name__}"
            )

        return value.value

    def process_result_value(self, value: str | None, dialect: Dialect) -> PermissionCode | None:
        """Convert TEXT from database back to PermissionCode."""
        if value is None:
            return None
        
        return PermissionCode(value)