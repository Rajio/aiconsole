"""
Script to verify and migrate the database.
"""

import asyncio
import logging
import sys
from pathlib import Path

from aiconsole.database import db_manager
from aiconsole.database.check_db import verify_database
from aiconsole.database.migrate_materials import migrate_materials_to_db

_log = logging.getLogger(__name__)


async def verify_and_migrate() -> bool:
    """
    Verify database connection and migrate materials.
    Returns True if successful, False otherwise.
    """
    try:
        print("\n🔍 Starting database verification and migration...")

        # Verify database
        if not await verify_database():
            print("❌ Database verification failed")
            return False

        # Create tables if they don't exist
        print("\n📦 Creating tables if they don't exist...")
        db_manager.create_tables()

        # Migrate materials
        success_count, total_count = await migrate_materials_to_db()
        
        if success_count == total_count:
            print("\n✅ All materials migrated successfully!")
        else:
            print(f"\n⚠️ Only {success_count} out of {total_count} materials migrated successfully")
            print("Please check the logs for details on failed migrations")

        return True

    except Exception as e:
        _log.error(f"Error during verification and migration: {e}")
        return False


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run verification and migration
    success = asyncio.run(verify_and_migrate())
    sys.exit(0 if success else 1) 