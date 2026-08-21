"""Define the ORM mappings for the Identity module using SQLAlchemy."""

from identity.domain.entity.permission import Permission
from identity.domain.entity.role import Role
from identity.domain.entity.user_role import UserRole
from identity.domain.entity.session import Session
from identity.domain.entity.refresh_token import RefreshToken
from identity.domain.entity.action_token import ActionToken
from identity.domain.entity.auth_event import AuthEvent
from shared_kernel.infra.database.registry import mapper_registry

from identity.domain.entity.user import User
from identity.domain.entity.password_credential import PasswordCredential

from tables import (
    users_table,
    password_credentials_table,
    roles_table,
    permissions_table,
    user_roles_table,
    sessions_table,
    refresh_tokens_table,
    action_tokens_table,
    auth_events_table,
)

def start_identity_mappers():
    """Initialize the ORM mappings for the Identity module."""
    
    mapper_registry.map_imperatively(
        User,
        users_table,
    )

    mapper_registry.map_imperatively(
        PasswordCredential,
        password_credentials_table,
        properties={
            # Map DB PK/FK column user_id to the aggregate id in the domain model.
            "id": password_credentials_table.c.user_id,
        },
    )

    mapper_registry.map_imperatively(
        Role,
        roles_table
    )

    mapper_registry.map_imperatively(
        Permission,
        permissions_table
    )

    mapper_registry.map_imperatively(
        UserRole,
        user_roles_table,
    )

    mapper_registry.map_imperatively(
        Session,
        sessions_table,
    )

    mapper_registry.map_imperatively(
        RefreshToken,
        refresh_tokens_table,
    )

    mapper_registry.map_imperatively(
        ActionToken,
        action_tokens_table,
    )

    mapper_registry.map_imperatively(
        AuthEvent,
        auth_events_table,
    )
