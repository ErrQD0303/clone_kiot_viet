"""Define the utilities for permission manifest in the Identity domain."""

from bootstrap.rbac_manifest import RbacManifest
from shared_kernel.domain.entity.permission_definition import PermissionDefinition


def validate_permission_manifest(manifest: RbacManifest) -> bool:
    """
    Validate the permission manifest.
    """
    codes = [
        definition.code for definition in manifest.permissions
    ]

    duplicated_permissions = set(
        code for code in codes if codes.count(code) > 1
    )

    if duplicated_permissions is not None and len(duplicated_permissions) > 0:
        raise ValueError(
            f"Duplicated permission codes found in the manifest: {duplicated_permissions}"
        )

    declared_codes = set(codes)

    for role, granted_codes in manifest.role_grants.items():
        unknown_codes = granted_codes - declared_codes
        if unknown_codes:
            raise ValueError(
                f"Role {role} has unknown permission codes: {unknown_codes}"
            )