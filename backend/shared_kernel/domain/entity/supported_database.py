"""Define the SupportedDatabase value object for supported databases in the system."""

from sqlalchemy import Enum

from clone_kiot_viet.backend.shared_kernel.domain.entity.value_object import ValueObject


class SupportedDatabase(ValueObject, str, Enum):
    """SupportedDatabase value object representing supported databases for this project."""
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
