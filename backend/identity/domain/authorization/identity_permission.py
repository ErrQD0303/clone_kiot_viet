"""Define the IdentityPermission value object for user roles in the system."""
from enum import Enum

from shared_kernel.domain.entity.value_object import ValueObject

class IdentityPermission(ValueObject, str, Enum):
    """IdentityPermission value object representing user roles."""
    IDENTITY_USER_READ = "IDENTITY_USER_READ"
