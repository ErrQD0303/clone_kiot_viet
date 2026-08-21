"""Define the User Status value object for user statuses in the system."""

from enum import Enum
from tkinter import DISABLED

from shared_kernel.domain.entity.value_object import ValueObject


class UserStatus(ValueObject, str, Enum):
    """UserStatus value object representing user current status."""
    PENDING = "pending"
    ACTIVE = "active"
    LOCKED = "locked"
    DISABLED = "disabled"
