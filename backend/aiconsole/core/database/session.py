from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from aiconsole.core.config import get_settings
from aiconsole.core.database.errors import handle_db_error

settings = get_settings()

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Get a database session with automatic cleanup

    Yields:
        Session: A database session

    Raises:
        ConnectionError: If there is an error connecting to the database
    """
    session: Optional[Session] = None
    try:
        session = SessionLocal()
        yield session
    except Exception as e:
        handle_db_error(e, "Error getting database session")
    finally:
        if session:
            session.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables

    Raises:
        ConnectionError: If there is an error connecting to the database
    """
    try:
        from aiconsole.core.database.models import Base

        Base.metadata.create_all(bind=engine)
    except Exception as e:
        handle_db_error(e, "Error initializing database")
