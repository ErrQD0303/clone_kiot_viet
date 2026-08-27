"""Define the Sync RBAC Service"""
from bootstrap.rbac_manifest import RbacManifest
from identity.application.service.models.sync_rbac_result import SyncRbacResult
from identity.domain.authorization.identity_role import IdentityRole
from identity.domain.entity.permission import Permission
from identity.domain.entity.role import Role
from identity.domain.repository.permission_repository import PermissionRepository
from identity.domain.repository.role_repository import RoleRepository
from shared_kernel.domain.entity.permission_code import PermissionCode
from shared_kernel.domain.unit_of_work import UnitOfWork   

class SyncRbacService:
    """Sync Rbac Service"""
    def __init__(
        self,
        permission_repository: PermissionRepository,
        role_repository: RoleRepository,
        unit_of_work: UnitOfWork
    ):
        self._permission_repository = permission_repository
        self._role_repository = role_repository
        self._unit_of_work = unit_of_work

    async def execute(self, manifest: RbacManifest) -> SyncRbacResult:
        created_permissions = 0
        updated_permissions = 0
        created_roles = 0
        added_grants = 0

        await self._unit_of_work.start()
        try:
            permission_codes = {
                definition.code for definition in manifest.permissions
            }

            existing_permissions = await self._permission_repository.get_by_codes(permission_codes)

            permissions_by_code = {
                permission.code: permission for permission in existing_permissions
            }

            for definition in manifest.permissions:
                permission = permissions_by_code.get(definition.code)

                if permission is None:
                    # Create new permission
                    permission = Permission.create(
                        code=definition.code,
                        description=definition.description
                    )

                    self._permission_repository.create(permission)

                    permissions_by_code[definition.code] = permission

                    created_permissions += 1
                elif (permission.description != definition.description):
                    permission.change_description(definition.description)

                    updated_permissions += 1

            await self._unit_of_work.flush()

            role_codes = set({role.value for role in manifest.role_grants})
            existing_roles = await self._role_repository.get_by_codes(role_codes)
            roles_by_name = {role.name: role for role in existing_roles}

            for role_name, granted_codes in manifest.role_grants.items():
                role_name_key = role_name.value.upper()
                role = roles_by_name.get(role_name_key)

                if role is None:
                    new_role = IdentityRole(role_name)
                    role = Role.create(
                        code=new_role.value,
                        name=new_role.name,
                        description=new_role.name,
                    )
                    self._role_repository.create(role)
                    roles_by_name[role_name] = role
                    created_roles += 1

                for permission_code in granted_codes:
                    permission = permissions_by_code.get(permission_code)

                    if permission is None:
                        raise ValueError(
                            f"Permission with code '{permission_code}' not found."
                        )

                    if role.grant(permission):
                        added_grants += 1

            await self._unit_of_work.commit()
        except Exception as e:
            await self._unit_of_work.rollback()
            raise

        return SyncRbacResult(
            permissions_created=created_permissions,
            permissions_updated=updated_permissions,
            roles_created=created_roles,
            grants_added=added_grants
        )
        
