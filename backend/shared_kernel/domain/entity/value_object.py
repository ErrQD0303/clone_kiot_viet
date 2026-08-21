"""Define value objects for Shared Kernel"""
from enum import Enum, EnumMeta
from typing import Any, TypeVar, cast
from shared_kernel.domain.exception.value_object_enum_error import ValueObjectEnumError

TValueObject = TypeVar("TValueObject", bound="ValueObject") # pylint: disable=invalid-name


class ValueObject:
    """Base class for value objects."""
    value: Any

    # sqlalchemy save this value to database
    def __composite_values__(self):
        """Return the composite values of the value object. This method is used for saving value objects to the database.""" # pylint: disable=line-too-long
        return self.value

    # sqlalchemy load this value from database
    @classmethod
    def from_value(cls, value: Any) -> TValueObject:
        """Create a value object from a given value. This method is used for loading value objects from the database.""" # pylint: disable=line-too-long
        if isinstance(cls, EnumMeta):
            enum_cls = cast(type[Enum], cls)
            for item in enum_cls.__members__.values():
                if item.value == value:
                    return cast(TValueObject, item)
            raise ValueObjectEnumError

        instance = cls(value=value)
        return instance
