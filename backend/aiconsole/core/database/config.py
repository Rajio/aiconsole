import os

from aiconsole.core.database.manager import DatabaseManager

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123321@localhost:5432/aiconsole")

# Create database manager instance
db_manager = DatabaseManager(DATABASE_URL)
