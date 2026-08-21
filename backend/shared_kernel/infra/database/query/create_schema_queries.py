"""Define the create schema queries for supported databases in the system."""
from shared_kernel.domain.entity.supported_database import SupportedDatabase

CREATE_SCHEMA_QUERIES = {
    SupportedDatabase.POSTGRESQL: (
        "CREATE SCHEMA IF NOT EXISTS {schema_name};"
    ),
}
