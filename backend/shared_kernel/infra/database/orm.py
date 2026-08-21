"""Define the ORM mappings for the User entity using SQLAlchemy."""
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Text
from sqlalchemy.orm import registry, composite
from identity.domain.entity.user import User as IdentityUserEntity
from shared_kernel.domain.entity.user_role import UserRole

metadata = MetaData()
mapper_registry = registry()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("display_name", String(50), nullable=False),
    Column("username", String(50), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("role", String(20), nullable=False),
    Column("phone_number", String(20), nullable=True),
    Column("email", String(255), nullable=True),
    Column("date_of_birth", Date, nullable=True),
    Column("address", String(200), nullable=True),
    Column("user_note", Text, nullable=True),
)

def init_orm_mappers():
    """
    initialize orm mappings
    """

    mapper_registry.map_imperatively(
        IdentityUserEntity,
        user,
        exclude_properties={"role"},
        properties={
            "display_name": user.c.display_name,
            "username": user.c.username,
            "password": user.c.password,
            "role": composite(UserRole.from_value, user.c.role),
            "phone_number": user.c.phone_number,
            "email": user.c.email,
            "date_of_birth": user.c.date_of_birth,
            "address": user.c.address,
            "user_note": user.c.user_note,
        },
    )
