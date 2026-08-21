"""Define domain entities for Shared Kernel"""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any, TypeVar

TEntity = TypeVar("TEntity", bound="Entity") # pylint: disable=invalid-name

@dataclass(eq=False, init=False)
class Entity:
    """Base class for domain entities."""
    id: UUID = field(default_factory=uuid4, init=False)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

class AggregateRoot(Entity):
    """
    An entry point of aggregate.
    """
