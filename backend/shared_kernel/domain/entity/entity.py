"""Define domain entities for Shared Kernel"""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any, Generic, TypeVar, Hashable

TIdentity = TypeVar("TIdentity", bound=Hashable) # pylint: disable=invalid-name

class Entity(Generic[TIdentity]):
    """Base class for entities with any identity type."""

    @property
    def identity(self) -> TIdentity:
        """Get the identity of the entity."""
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        """Check equality based on identity."""
        if isinstance(other, type(self)):
            return self.identity == other.identity
        return False

    def __hash__(self):
        """Generate a hash based on identity."""
        return hash(self.identity)

@dataclass(eq=False, init=False)
class UUIDEntity(Entity[UUID]):
    """Base class for entities using a UUID identity."""
    id: UUID = field(default_factory=uuid4, init=False)

    def identify(self) -> UUID:
        """Get the identity of the entity."""
        return self.id

class AggregateRoot(UUIDEntity):
    """
    An entry point of aggregate.
    """
