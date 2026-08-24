"""Define the IdentityUserRole value object for user roles in the system."""
from enum import Enum

from shared_kernel.domain.entity.value_object import ValueObject

class IdentityRole(ValueObject, str, Enum):
    """UserRole value object representing user roles."""
    ADMIN = "admin"
    USER = "user"
