#!/usr/bin/env python
"""
Example script demonstrating how to use the database integration for managing materials.
"""

from aiconsole.database import db_manager


def main():
    """Main function to demonstrate database usage."""
    print("🔍 Demonstrating database usage...")

    try:
        # Example: Create a new material
        material_data = {
            "name": "example_material",
            "version": "1.0",
            "usage": "Example usage description",
            "usage_examples": "Example 1: ...\nExample 2: ...",
            "type": "material",
            "location": "project",
            "default_status": "enabled",
            "current_status": "enabled",
            "content": "This is the content of the material",
            "content_type": "text",
            "material_metadata": {"key": "value"},
            "agents": {"agent1": {"skills": ["skill1", "skill2"]}},
        }

        # Create a new material
        with db_manager.get_session() as session:
            material = db_manager.create_material(material_data)
            session.add(material)
            session.commit()
            material_id = int(material.id)
            print(f"✅ Created material with ID: {material_id}")

        # Get a material by ID
        with db_manager.get_session() as session:
            retrieved_material = db_manager.get_material(material_id)
            if retrieved_material:
                print(f"✅ Retrieved material: {retrieved_material.name}")
            else:
                print("❌ Material not found")

        # Update a material
        with db_manager.get_session() as session:
            update_data = {"current_status": "disabled"}
            updated_material = db_manager.update_material(material_id, update_data)
            if updated_material:
                print(f"✅ Updated material status: {updated_material.current_status}")
            else:
                print("❌ Material not found")

        # Get all materials
        with db_manager.get_session() as session:
            all_materials = db_manager.get_all_materials()
            print(f"✅ Total materials: {len(all_materials)}")

        # Delete a material
        with db_manager.get_session() as session:
            success = db_manager.delete_material(material_id)
            print(f"✅ Material deleted: {success}")

        print("✅ Database usage demonstration complete")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
