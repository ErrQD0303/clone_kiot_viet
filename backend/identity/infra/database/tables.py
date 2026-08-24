from sqlalchemy import (
    Table,
    Column,
    String,
    text,
    CheckConstraint,
    DateTime,
    Integer,
    BigInteger,
    ForeignKeyConstraint,
    UniqueConstraint,
    TEXT,
    BOOLEAN,
    Index,
    LargeBinary,
)
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB

from shared_kernel.domain.entity.permission_code import PERMISSION_PATTERN_STR
from shared_kernel.infra.database.registry import metadata_object
from shared_kernel.infra.database.schema import Schema
from identity.domain.entity.user_status import UserStatus
from shared_kernel.infra.database.types.permission_code_type import PermissionCodeType

users_table = Table(
    "users",
    metadata_object,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("username", TEXT, nullable=False, unique=True),
    Column("email", TEXT, nullable=False, unique=True),
    Column("display_name", String(150), nullable=True),
    Column("status", String(16), nullable=False, server_default=UserStatus.PENDING.value),
    Column("email_verified_at", DateTime(timezone=True), nullable=True),
    Column("auth_version", Integer, nullable=False, server_default=text("1")),
    Column("last_login_at", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),

    CheckConstraint(
        "status IN (" + ", ".join(f"'{status.value}'" for status in UserStatus) + ")",
        name="status",
    ),
    CheckConstraint("auth_version > 0", name="auth_version"),

    schema=Schema.IDENTITY.value
)

password_credentials_table = Table(
    "password_credentials",
    metadata_object,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("password_hash", TEXT, nullable=False),
    Column("password_changed_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("must_change_password", BOOLEAN, nullable=False, server_default=text("false")),
    Column("failed_attempt_count", Integer, nullable=False, server_default=text("0")),
    Column("locked_until", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),

    ForeignKeyConstraint(["user_id"], [f"{Schema.IDENTITY.value}.users.id"]),

    CheckConstraint("failed_attempt_count >= 0", name="failed_attempts"),

    schema=Schema.IDENTITY.value
)


roles_table = Table(
    "roles",
    metadata_object,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("code", TEXT, nullable=False, unique=True),
    Column("name", String(150), nullable=False),
    Column("description", TEXT, nullable=True),
    Column("is_system", BOOLEAN, nullable=False, server_default=text("false")),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),

    CheckConstraint("code::text ~ '^[a-z][a-z0-9)_]*$'", name="code"),

    schema=Schema.IDENTITY.value
)

permissions_table = Table(
    "permissions",
    metadata_object,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("code", PermissionCodeType, nullable=False, unique=True),
    Column("description", TEXT, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),

    CheckConstraint(f"code::text ~ '{PERMISSION_PATTERN_STR}'", name="code"),

    schema=Schema.IDENTITY.value
)

user_roles_table = Table(
    "user_roles",
    metadata_object,
    Column("user_id", UUID(as_uuid=True), primary_key=True),
    Column("role_id", UUID(as_uuid=True), primary_key=True),
    Column("assigned_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("assigned_by", UUID(as_uuid=True), nullable=True),
    Column("expired_at", DateTime(timezone=True), nullable=True),

    ForeignKeyConstraint(["user_id"], [f"{Schema.IDENTITY.value}.users.id"]),
    ForeignKeyConstraint(["role_id"], [f"{Schema.IDENTITY.value}.roles.id"]),
    ForeignKeyConstraint(["assigned_by"], [f"{Schema.IDENTITY.value}.users.id"]),

    CheckConstraint("expired_at IS NULL OR expired_at > assigned_at", name="expiry"),

    Index("idx_user_roles_role_id", "role_id"),
    Index("idx_user_roles_user_expiry", "user_id", "expired_at"),

    schema=Schema.IDENTITY.value
)

role_permissions_table = Table(
    "role_permissions",
    metadata_object,
    Column("role_id", UUID(as_uuid=True), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), primary_key=True),
    Column("granted_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),

    ForeignKeyConstraint(["role_id"], [f"{Schema.IDENTITY.value}.roles.id"], ondelete="CASCADE"),
    ForeignKeyConstraint(["permission_id"], [f"{Schema.IDENTITY.value}.permissions.id"], ondelete="CASCADE"),

    Index("ix_role_permissions_role_id", "role_id"),
    Index("ix_role_permissions_permission_id", "permission_id"),

    schema=Schema.IDENTITY.value,
)

sessions_table = Table(
    "sessions",
    metadata_object,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("last_seen_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("revoked_at", DateTime(timezone=True), nullable=True),
    Column("revoke_reason", String(50), nullable=True),
    Column("ip_address", INET, nullable=True),
    Column("user_agent", TEXT, nullable=True),

    ForeignKeyConstraint(["user_id"], [f"{Schema.IDENTITY.value}.users.id"], ondelete="CASCADE"),

    CheckConstraint("expires_at > created_at", name="expiry"),
    CheckConstraint("revoked_at IS NULL OR revoked_at >= created_at", name="revoked"),

    Index("ix_sessions_user_state", "user_id", "revoked_at", "expires_at"),

    schema=Schema.IDENTITY.value,
)

refresh_tokens_table = Table(
    "refresh_tokens",
    metadata_object,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("session_id", UUID(as_uuid=True), nullable=False),
    Column("token_hash", LargeBinary(32), nullable=False, unique=True),
    Column("parent_token_id", UUID(as_uuid=True), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("used_at", DateTime(timezone=True), nullable=True),
    Column("revoked_at", DateTime(timezone=True), nullable=True),

    ForeignKeyConstraint(
        ["session_id"],
        [f"{Schema.IDENTITY.value}.sessions.id"],
        ondelete="CASCADE",
    ),
    ForeignKeyConstraint(
        ["parent_token_id"],
        [f"{Schema.IDENTITY.value}.refresh_tokens.id"],
        ondelete="SET NULL",
    ),

    CheckConstraint("octet_length(token_hash) = 32", name="hash_size"),
    CheckConstraint("expires_at > created_at", name="expiry"),
    CheckConstraint("used_at IS NULL OR used_at >= created_at", name="used"),
    CheckConstraint("revoked_at IS NULL OR revoked_at >= created_at", name="revoked"),

    Index("ix_refresh_tokens_session", "session_id", text("created_at DESC")),
    Index("ix_refresh_tokens_parent", "parent_token_id"),

    schema=Schema.IDENTITY.value,
)

action_tokens_table = Table(
    "action_tokens",
    metadata_object,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("purpose", String(24), nullable=False),
    Column("token_hash", LargeBinary(32), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("consumed_at", DateTime(timezone=True), nullable=True),
    Column("requested_ip", INET, nullable=True),

    ForeignKeyConstraint(["user_id"], [f"{Schema.IDENTITY.value}.users.id"], ondelete="CASCADE"),

    UniqueConstraint("token_hash", name="uq_action_tokens_hash"),
    CheckConstraint(
        "purpose IN ('verify_email', 'reset_password')",
        name="ck_action_tokens_purpose",
    ),
    CheckConstraint("octet_length(token_hash) = 32", name="ck_action_token_hash_size"),
    CheckConstraint("expires_at > created_at", name="ck_action_tokens_expiry"),
    CheckConstraint("consumed_at IS NULL OR consumed_at >= created_at", name="ck_action_tokens_consumed"),

    Index("ix_action_tokens_user_purpose", "user_id", "purpose", text("created_at DESC")),

    schema=Schema.IDENTITY.value,
)

auth_events_table = Table(
    "auth_events",
    metadata_object,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", UUID(as_uuid=True), nullable=True),
    Column("session_id", UUID(as_uuid=True), nullable=True),
    Column("event_type", String(60), nullable=False),
    Column("success", BOOLEAN, nullable=False, server_default=text("false")),
    Column("ip_address", INET, nullable=True),
    Column("user_agent", TEXT, nullable=True),
    Column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb")),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("now()")),

    ForeignKeyConstraint(["user_id"], [f"{Schema.IDENTITY.value}.users.id"], ondelete="SET NULL"),
    ForeignKeyConstraint(["session_id"], [f"{Schema.IDENTITY.value}.sessions.id"], ondelete="SET NULL"),

    Index("ix_auth_events_user_time", "user_id", text("created_at DESC")),
    Index("ix_auth_events_type_time", "event_type", text("created_at DESC")),

    schema=Schema.IDENTITY.value,
)