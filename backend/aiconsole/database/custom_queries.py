#!/usr/bin/env python
"""
Example script demonstrating how to use custom queries with the database integration.
"""

from sqlalchemy import text

from aiconsole.database import db_manager


def main():
    """Main function to demonstrate custom queries."""
    print("🔍 Demonstrating custom queries...")

    try:
        # Example 1: Get all materials with a specific type
        with db_manager.get_session() as session:
            result = session.execute(text("SELECT * FROM materials WHERE type = 'material'"))
            materials = result.fetchall()
            print(f"✅ Found {len(materials)} materials with type 'material'")

            for material in materials:
                print(f"  - ID: {material.id}, Name: {material.name}, Version: {material.version}")

        # Example 2: Get materials created in the last 24 hours
        with db_manager.get_session() as session:
            result = session.execute(text("SELECT * FROM materials WHERE created_at > NOW() - INTERVAL '24 hours'"))
            recent_materials = result.fetchall()
            print(f"✅ Found {len(recent_materials)} materials created in the last 24 hours")

            for material in recent_materials:
                print(f"  - ID: {material.id}, Name: {material.name}, Created: {material.created_at}")

        # Example 3: Count materials by location
        with db_manager.get_session() as session:
            result = session.execute(text("SELECT location, COUNT(*) FROM materials GROUP BY location"))
            location_counts = result.fetchall()
            print("✅ Materials by location:")

            for location, count in location_counts:
                print(f"  - {location}: {count}")

        print("✅ Custom queries demonstration complete")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
