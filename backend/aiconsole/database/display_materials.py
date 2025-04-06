"""
Script to display the contents of the materials database.
"""

import sys

from sqlalchemy import text

from aiconsole.database import db_manager


def display_materials() -> None:
    """Display all materials in the database."""
    try:
        # Get all materials from the database
        materials = db_manager.get_all_materials()

        if not materials:
            print("❌ No materials found in the database.")
            return

        # Display materials in a readable format
        print(f"📦 Found {len(materials)} materials:")
        for material in materials:
            print(
                f"\nMaterial: {material.name}"
                f"\n  ID: {material.id}"
                f"\n  Version: {material.version}"
                f"\n  Location: {material.location}"
                f"\n  Status: {material.current_status}"
                f"\n  Type: {material.type}"
                f"\n  Content Type: {material.content_type}"
                f"\n  Created: {material.created_at}"
                f"\n  Updated: {material.updated_at}"
                f"\n  {'-' * 50}"
            )

    except Exception as e:
        print(f"❌ Error displaying materials: {e}")
        sys.exit(1)


def main() -> None:
    """Main function to display materials."""
    print("🔍 Checking PostgreSQL database connection...")

    try:
        # Test database connection
        with db_manager.get_session() as session:
            session.execute(text("SELECT 1"))
        print("✅ PostgreSQL connection successful")

        # Display materials
        display_materials()

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
