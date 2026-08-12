from enum import Enum, EnumMeta
from typing import Any
from shared_kernel.domain.exception.value_object_enum_error import ValueObjectEnumError


class ValueObject:
    # sqlalchemy save this value to database
    def __composite_values__(self):
        return self.value

    # sqlalchemy load this value from database
    @classmethod
    def from_value(cls, value: Any):
        if isinstance(cls, EnumMeta):
            for item in cls:
                if item.value == value:
                    return item
            raise ValueObjectEnumError

        instance = cls(value=value)
        return instance

class UserRole(ValueObject, str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
