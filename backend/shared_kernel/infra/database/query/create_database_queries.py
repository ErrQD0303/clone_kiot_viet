"""Define the create database queries for supported databases in the system."""
from shared_kernel.domain.entity.supported_database import SupportedDatabase

CREATE_DATABASE_QUERIES = {
    SupportedDatabase.MYSQL: (
        "CREATE DATABASE IF NOT EXISTS {database_name} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    ),
    SupportedDatabase.POSTGRESQL: (
        "CREATE DATABASE {database_name} "
        "WITH ENCODING 'UTF8' "
        "LC_COLLATE='en_US.UTF-8' "
        "LC_CTYPE='en_US.UTF-8' "
        "TEMPLATE=template0"
    ),
}
