"""Define the ORM mappings for the User entity using SQLAlchemy."""

from identity.infra.database.mappings import start_identity_mappers

_mappers_started = False

def init_orm_mappers():
    """Initialize ORM mappings once per process."""
    global _mappers_started  # pylint: disable=global-statement

    if _mappers_started:
        return

    start_identity_mappers()
    _mappers_started = True
