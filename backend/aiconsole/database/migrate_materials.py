"""
Script to scan the project folder for materials and migrate them to the database.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from aiconsole.database import db_manager
from aiconsole.database.models import Material


def find_material_files(project_root: Path) -> List[Path]:
    """
    Find all material files in the project.

    This function assumes materials are stored as JSON or YAML files in specific directories.
    You may need to adjust the search patterns based on your actual project structure.
    """
    material_files: List[Path] = []

    # Common patterns for material files
    patterns = [
        "**/materials/**/*.json",
        "**/materials/**/*.yaml",
        "**/materials/**/*.yml",
        "**/materials/**/*.toml",
        "**/materials/**/*.txt",
        "**/materials/**/*.md",
    ]

    for pattern in patterns:
        material_files.extend(project_root.glob(pattern))

    # Also check for specific directories that might contain materials
    material_dirs = [
        project_root / "materials",
        project_root / "aiconsole" / "materials",
        project_root / "backend" / "aiconsole" / "materials",
        project_root / "backend" / "aiconsole" / "preinstalled" / "materials",
    ]

    for material_dir in material_dirs:
        if material_dir.exists():
            for file in material_dir.rglob("*"):
                if file.is_file() and file.suffix in [".json", ".yaml", ".yml", ".toml", ".txt", ".md"]:
                    material_files.append(file)

    return list(set(material_files))  # Remove duplicates


def parse_material_file(file_path: Path) -> Optional[Dict]:
    """
    Parse a material file and extract its content and metadata.

    This function assumes materials are stored as JSON, YAML, TOML, or text files.
    You may need to adjust the parsing logic based on your actual file formats.
    """
    try:
        content = file_path.read_text(encoding="utf-8")

        # Try to parse as JSON
        if file_path.suffix == ".json":
            try:
                data = json.loads(content)
                return {
                    "name": data.get("name", file_path.stem),
                    "version": data.get("version", "1.0"),
                    "usage": data.get("usage", ""),
                    "usage_examples": data.get("usage_examples", ""),
                    "type": data.get("type", "material"),
                    "location": data.get("location", "project"),
                    "default_status": data.get("default_status", "enabled"),
                    "current_status": data.get("current_status", "enabled"),
                    "override": data.get("override", False),
                    "content": content,
                    "content_type": "json",
                    "path": str(file_path),
                    "material_metadata": data.get("metadata", {}),
                    "agents": data.get("agents", {}),
                }
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {file_path} as JSON")

        # For other file types, create a basic material entry
        return {
            "name": file_path.stem,
            "version": "1.0",
            "usage": "",
            "usage_examples": "",
            "type": "material",
            "location": "project",
            "default_status": "enabled",
            "current_status": "enabled",
            "override": False,
            "content": content,
            "content_type": file_path.suffix[1:] if file_path.suffix else "text",
            "path": str(file_path),
            "material_metadata": {},
            "agents": {},
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def migrate_materials(project_root: Path) -> Tuple[int, int]:
    """
    Migrate materials from the filesystem to the database.

    Returns:
        Tuple[int, int]: Number of materials found and number of materials migrated
    """
    material_files = find_material_files(project_root)
    print(f"Found {len(material_files)} material files")

    migrated_count = 0
    with db_manager.get_session() as session:
        for file_path in material_files:
            material_data = parse_material_file(file_path)
            if material_data:
                try:
                    # Check if material with the same name already exists
                    existing_material = session.query(Material).filter_by(name=material_data["name"]).first()
                    if existing_material:
                        print(f"Material '{material_data['name']}' already exists in the database, skipping")
                        continue

                    # Create the material in the database
                    material = Material(**material_data)
                    session.add(material)
                    session.commit()
                    print(f"Migrated material '{material.name}' from {file_path}")
                    migrated_count += 1
                except Exception as e:
                    print(f"Error migrating {file_path}: {e}")
                    session.rollback()

    return len(material_files), migrated_count


def main():
    """Main function to migrate materials."""
    print("🔍 Scanning for materials to migrate...")

    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent.parent

    # Check if the database is ready
    from aiconsole.database.check_db import (
        check_connection,
        check_table_exists,
        check_table_structure,
    )

    if not check_connection():
        print(" Cannot proceed with migration due to database connection issues")
        sys.exit(1)

    if not check_table_exists():
        print("Creating materials table...")
        db_manager.create_tables()
        print(" Materials table created")

    structure_ok, _ = check_table_structure()
    if not structure_ok:
        print(" Table structure is incorrect. Please check the models.py file")
        sys.exit(1)

    # Migrate materials
    found_count, migrated_count = migrate_materials(project_root)

    print(f" Migration complete: {migrated_count} of {found_count} materials migrated to the database")


if __name__ == "__main__":
    main()
