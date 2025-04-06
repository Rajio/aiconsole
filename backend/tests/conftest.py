"""
Test configuration and fixtures.
"""

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aiconsole.database import db_manager
from aiconsole.database.models import Base


@pytest.fixture(scope="session")
def test_db():
    """Create a test database."""
    # Use SQLite for testing
    test_db_url = "sqlite:///test.db"
    engine = create_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Override the db_manager's engine and session
    db_manager.engine = engine
    db_manager.SessionLocal = SessionLocal

    yield db_manager

    # Clean up
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture(autouse=True)
def setup_test_db(test_db):
    """Set up the test database before each test."""
    # Create tables
    Base.metadata.create_all(bind=test_db.engine)

    yield

    # Drop tables after each test
    Base.metadata.drop_all(bind=test_db.engine)
