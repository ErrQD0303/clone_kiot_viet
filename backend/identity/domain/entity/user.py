from dataclasses import dataclass
from shared_kernel.domain.entity.entity import AggregateRoot
from shared_kernel.domain.entity.value_object import UserRole

# Turn off the equality comparison and hash generation for the User class
@dataclass(eq=False, slots=True)
class User(AggregateRoot):
    display_name: str
    username: str
    password: str
    role: UserRole
    phone_number: str | None = None
    email: str | None = None
    date_of_birth: str | None = None
    address: str | None = None
    user_note: str | None = None