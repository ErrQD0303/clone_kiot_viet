"""Database connection module"""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, inspect, Engine
from sqlalchemy.orm import Session, sessionmaker

from shared_kernel.domain.exception.create_database_fail_exception import CreateDatabaseFailException
from shared_kernel.infra.fastapi.config import settings
from shared_kernel.infra.database.query.create_database_queries import CREATE_DATABASE_QUERIES

sys_engine: Engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


def database_exists(db_engine: Engine) -> bool:
    """Check if the database exists"""
    inspector = inspect(db_engine)
    return inspector.get_schema_names() is not None

def parse_database_type(url: str) -> str:
    """Parse the database type from the SQLAlchemy URL"""
    return url.split(':')[0].split('+')[0]  # e.g., 'mysql+pymysql' -> 'mysql'


def create_database(db_engine: Engine = None, database_name: str = None):
    """Create the database if it does not exist"""
    if db_engine is None:
        raise CreateDatabaseFailException("Database engine is not provided.")

    if database_name is None:
        raise CreateDatabaseFailException("Database name is not provided.")

    with db_engine.connect() as connection:
        db_type = parse_database_type(str(db_engine.url))
        if not db_type:
            raise CreateDatabaseFailException(
                "Database type could not be determined from the URL.")

        create_query = CREATE_DATABASE_QUERIES.get(db_type)\
            .format(database_name=database_name)

        if not create_query:
            raise CreateDatabaseFailException(
                f"The database type '{db_type}' is not supported for automatic creation.")

        connection.execute(create_query)

def get_engine():
    """Get SQLAlchemy engine"""
    db_engine = sys_engine if sys_engine\
          else create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

    if not database_exists(db_engine.url):
        create_database(db_engine, settings.DATABASE_NAME)

    return db_engine

engine = get_engine()
session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

@contextmanager
def get_db_session() -> Generator[Session]:
    """Provide a transactional scope around a series of operations."""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
