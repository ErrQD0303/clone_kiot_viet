"""Define the Sync RBAC Result for Sync RBAC Service"""
from dataclasses import dataclass   

@dataclass(frozen=True, slots=True, init=True)
class SyncRbacResult:
    """Result of SyncRcbaService"""
    permissions_created: int
    permissions_updated: int
    roles_created: int
    grants_added: int
