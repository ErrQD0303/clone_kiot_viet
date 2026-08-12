from dataclasses import field
from uuid import UUID, uuid4
from typing import Any

class Entity:
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
    pass