#!/usr/bin/env python
"""
Script to run the database check and synchronization.
"""

import sys
from pathlib import Path

from aiconsole.database.check_db import (
    check_connection,
    check_existing_materials,
    check_table_exists,
    check_table_structure,
)
from aiconsole.database.migrate_materials import migrate_materials


def main():
    """Main function to run the database check and synchronization."""
    print("🔍 Checking and synchronizing materials database...")

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent.parent

    # Check if the database is ready
    if not check_connection():
        print("❌ Cannot proceed with synchronization due to database connection issues")
        sys.exit(1)

    if not check_table_exists():
        print("Creating materials table...")
        from aiconsole.database import db_manager

        db_manager.create_tables()
        print("✅ Materials table created")

    structure_ok, _ = check_table_structure()
    if not structure_ok:
        print("❌ Table structure is incorrect. Please check the models.py file")
        sys.exit(1)

    # Check if there are any existing materials in the database
    material_count = check_existing_materials()

    if material_count == 0:
        print("ℹ️ No materials found in the database, scanning for materials to migrate...")
        found_count, migrated_count = migrate_materials(project_root)
        print(f"✅ Migration complete: {migrated_count} of {found_count} materials migrated to the database")
    else:
        print(f"ℹ️ Found {material_count} materials in the database")
        print("ℹ️ Skipping migration as materials already exist in the database")

    print("✅ Database synchronization complete")
    print("ℹ️ All new materials will be saved to the database")


if __name__ == "__main__":
    main()
