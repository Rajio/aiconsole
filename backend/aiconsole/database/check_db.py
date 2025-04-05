"""
Script to check the database connection and table structure.
"""

import sys
from typing import List, Optional, Tuple

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from aiconsole.database import db_manager
from aiconsole.database.models import Material


def check_connection() -> bool:
    """Check if the database connection is working."""
    try:
        with db_manager.get_session() as session:
            session.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_table_exists() -> bool:
    """Check if the materials table exists."""
    inspector = inspect(db_manager.engine)
    tables = inspector.get_table_names()

    if "materials" in tables:
        print("✅ Materials table exists")
        return True
    else:
        print("❌ Materials table does not exist")
        return False


def check_table_structure() -> Tuple[bool, List[str]]:
    """Check if the materials table has the correct structure."""
    inspector = inspect(db_manager.engine)
    columns = {col["name"]: col for col in inspector.get_columns("materials")}

    expected_columns = [
        "id",
        "name",
        "version",
        "usage",
        "usage_examples",
        "type",
        "location",
        "default_status",
        "current_status",
        "override",
        "content",
        "content_type",
        "path",
        "created_at",
        "updated_at",
        "material_metadata",
        "agents",
    ]

    missing_columns = [col for col in expected_columns if col not in columns]

    if missing_columns:
        print(f"❌ Missing columns: {', '.join(missing_columns)}")
        return False, missing_columns
    else:
        print("✅ Table structure is correct")
        return True, []


def check_existing_materials() -> int:
    """Check if there are any existing materials in the table."""
    with db_manager.get_session() as session:
        count = session.query(Material).count()

    print(f"Found {count} materials in the database")
    return count


def test_material_creation() -> Optional[Material]:
    """Test if a new material can be created and saved."""
    try:
        material_data = {
            "name": "test_material",
            "version": "1.0",
            "usage": "Test usage",
            "type": "material",
            "location": "project",
            "default_status": "enabled",
            "current_status": "enabled",
            "content": "Test content",
            "content_type": "text",
        }

        material = db_manager.create_material(material_data)
        print(f"✅ Successfully created test material with ID: {material.id}")

        # Clean up the test material
        db_manager.delete_material(material.id)
        print("✅ Successfully deleted test material")

        return material
    except Exception as e:
        print(f"❌ Failed to create test material: {e}")
        return None


def main():
    """Main function to check the database."""
    print("🔍 Checking database connection and structure...")

    if not check_connection():
        print("❌ Cannot proceed with database check due to connection issues")
        sys.exit(1)

    if not check_table_exists():
        print("Creating materials table...")
        db_manager.create_tables()
        print("✅ Materials table created")

    structure_ok, _ = check_table_structure()
    if not structure_ok:
        print("❌ Table structure is incorrect. Please check the models.py file")
        sys.exit(1)

    material_count = check_existing_materials()

    if material_count == 0:
        print("ℹ️ No materials found in the database")
    else:
        print("ℹ️ Materials already exist in the database")

    test_material = test_material_creation()
    if test_material:
        print("✅ Database is working correctly")
    else:
        print("❌ Database is not working correctly")


if __name__ == "__main__":
    main()
