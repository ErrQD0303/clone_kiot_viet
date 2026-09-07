"""RBAC Manifest file"""

from dataclasses import dataclass

from identity.application.permissions import IDENTITY_PERMISSIONS,SELF_USER_ACTION_PERMISSIONS
from identity.domain.authorization.identity_role import IdentityRole
from shared_kernel.domain.entity.permission_code import PermissionCode
from shared_kernel.domain.entity.permission_definition import PermissionDefinition

@dataclass(frozen=True, slots=True)
class RbacManifest:
    """RBAC Manifest class for the role-based access control system."""
    permissions: tuple[PermissionDefinition, ...]
    role_grants: dict[IdentityRole, frozenset[PermissionCode]]

ALL_PERMISSIONS: tuple[PermissionDefinition, ...] = (
    *IDENTITY_PERMISSIONS,
    *SELF_USER_ACTION_PERMISSIONS,
)

ROLE_GRANTS: dict[IdentityRole, frozenset[PermissionCode]] = {
    IdentityRole.ADMIN: frozenset(definition.code for definition in ALL_PERMISSIONS),
    IdentityRole.USER: frozenset({
        *(definition.code for definition in SELF_USER_ACTION_PERMISSIONS)
    })
}

APPLICATION_RBAC = RbacManifest(
    permissions=ALL_PERMISSIONS,role_grants=ROLE_GRANTS)