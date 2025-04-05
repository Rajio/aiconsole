"""
Script to create the tables in the PostgreSQL database.
"""

import sys

from sqlalchemy import text

from aiconsole.database import db_manager
from aiconsole.database.models import Base


def drop_tables() -> None:
    """Drop all tables in the PostgreSQL database."""
    try:
        print("🔍 Dropping existing tables...")
        Base.metadata.drop_all(bind=db_manager.engine)
        print("✅ Tables dropped successfully")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        sys.exit(1)


def create_tables() -> None:
    """Create the tables in the PostgreSQL database."""
    try:
        print("🔍 Creating tables in the PostgreSQL database...")

        # Create the tables
        Base.metadata.create_all(bind=db_manager.engine)

        print("✅ Tables created successfully")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def main() -> None:
    """Main function to create tables."""
    print("🔍 Checking PostgreSQL database connection...")

    try:
        # Test database connection
        with db_manager.get_session() as session:
            session.execute(text("SELECT 1"))
        print("✅ PostgreSQL connection successful")

        # Drop and recreate tables
        drop_tables()
        create_tables()

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
