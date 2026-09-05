"""Define the Admin Initialization Result for AdminInitService"""
from dataclasses import dataclass   

@dataclass(frozen=True, slots=True, init=True)
class AdminInitResult:
    """Result of AdminInitService"""
    user_created: bool
    permissions_created: int
    permissions_updated: int
    roles_created: int
    grants_added: int
