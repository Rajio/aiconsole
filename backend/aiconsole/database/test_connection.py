#!/usr/bin/env python
"""
Script to test the database connection without creating tables.
"""

import sys

from sqlalchemy import create_engine, text

from aiconsole.database.config import get_connection_string


def main():
    """Test the database connection."""
    print("🔍 Testing database connection...")

    try:
        # Get the connection string
        connection_string = get_connection_string()
        print(f"Connection string: {connection_string}")

        # Create an engine
        engine = create_engine(connection_string)

        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")

            # Check if PostgreSQL is being used
            result = connection.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Database version: {version}")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
