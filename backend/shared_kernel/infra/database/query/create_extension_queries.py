"""Define the create extension queries for supported databases in the system."""
from shared_kernel.domain.entity.supported_database import SupportedDatabase

CREATE_EXTENSION_QUERIES = {
    SupportedDatabase.POSTGRESQL: (
        "CREATE EXTENSION IF NOT EXISTS {extension_name};"
    ),
}   
