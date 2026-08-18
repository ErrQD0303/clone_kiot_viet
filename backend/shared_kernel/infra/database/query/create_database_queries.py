"""Define the SupportedDatabase value object for supported databases in the system."""
from shared_kernel.domain.entity.supported_database import SupportedDatabase

CREATE_DATABASE_QUERIES = {
    SupportedDatabase.MYSQL: (
        "CREATE DATABASE IF NOT EXISTS {database_name} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
}
