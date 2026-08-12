class ValueObjectEnumError(Exception):
    """Exception raised for errors in the value object enum."""

    def __str__(self):
        return "Value Object got invalid value."