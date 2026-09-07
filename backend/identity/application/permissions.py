"""Define the Permissions for this Domain."""
from shared_kernel.domain.entity.permission_code import PermissionCode
from shared_kernel.domain.entity.permission_definition import PermissionDefinition
from shared_kernel.infra.database.schema import Schema

domain = Schema.IDENTITY.value

# Define permission codes for the Identity domain
SELF_USER_INFO_READ = PermissionDefinition(
    code=PermissionCode(f"{domain}.me.info.read"),
    description="Permission to read own user information.",
)

SELF_USER_INFO_MANAGE = PermissionDefinition(
    code=PermissionCode(f"{domain}.me.info.manage"),
    description="Permission to manage own user information.",
)

SELF_USER_LOGOUT = PermissionDefinition(
    code=PermissionCode(f"{domain}.me.logout"),
    description="Permission to logout and revoke own refresh token.",
)

SELF_USER_ACTION_PERMISSIONS = frozenset({
    SELF_USER_INFO_READ,
    SELF_USER_INFO_MANAGE,
    SELF_USER_LOGOUT,
})

USER_READ = PermissionDefinition(
    code=PermissionCode(f"{domain}.user.read"),
    description="Permission to read user information.",
)

USER_MANAGE = PermissionDefinition(
    code=PermissionCode(f"{domain}.user.manage"),
    description="Permission to manage user information.",
)

ROLE_MANAGE = PermissionDefinition(
    code=PermissionCode(f"{domain}.role.manage"),
    description="Permission to manage roles.",
)

PERMISSION_MANAGE = PermissionDefinition(
    code=PermissionCode(f"{domain}.permission.manage"),
    description="Permission to manage permissions.",
)

# Define permission codes for role management
IDENTITY_PERMISSIONS = frozenset(
    {
        USER_READ,
        USER_MANAGE,
        ROLE_MANAGE,
        PERMISSION_MANAGE,
        *SELF_USER_ACTION_PERMISSIONS
    }
)