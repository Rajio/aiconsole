"""
Example script demonstrating how to use the database integration for managing materials.
"""

from aiconsole.database import Material, db_manager


def main():
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
        "metadata": {"key": "value"},
        "agents": {"agent1": {"skills": ["skill1", "skill2"]}},
    }

    # Create a new material
    material = db_manager.create_material(material_data)
    print(f"Created material with ID: {material.id}")

    # Get a material by ID
    retrieved_material = db_manager.get_material(material.id)
    print(f"Retrieved material: {retrieved_material.name}")

    # Update a material
    update_data = {"current_status": "disabled"}
    updated_material = db_manager.update_material(material.id, update_data)
    print(f"Updated material status: {updated_material.current_status}")

    # Get all materials
    all_materials = db_manager.get_all_materials()
    print(f"Total materials: {len(all_materials)}")

    # Delete a material
    success = db_manager.delete_material(material.id)
    print(f"Material deleted: {success}")


if __name__ == "__main__":
    main()
