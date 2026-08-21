"""Define the ORM schema for the database using SQLAlchemy."""

from enum import Enum

from shared_kernel.domain.entity.value_object import ValueObject


class Schema(ValueObject, str, Enum):
    """Schema value object representing the database schema."""
    IDENTITY = "identity"