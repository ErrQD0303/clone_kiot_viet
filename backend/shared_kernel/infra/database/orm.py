"""Define the ORM mappings for the User entity using SQLAlchemy."""

from identity.infra.database.mappings import start_identity_mappers

def init_orm_mappers():
    """
    initialize orm mappings
    """

    start_identity_mappers()
