"""
Script to migrate materials from filesystem to database.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import rtoml
import yaml
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from aiconsole.core.assets.materials.material import MaterialContentType
from aiconsole.core.assets.types import AssetLocation
from aiconsole.core.project.paths import (
    get_core_assets_directory,
    get_project_assets_directory,
)
from aiconsole.database import db_manager
from aiconsole.database.models import Material

_log = logging.getLogger(__name__)


def find_material_files(project_root: Path) -> List[Path]:
    """Find all material files in the project."""
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


async def parse_material_file(file_path: Path) -> Optional[Dict]:
    """Parse a material file and return its contents as a dictionary."""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Try to parse based on file extension
        if file_path.suffix == ".json":
            data = json.loads(content)
        elif file_path.suffix in [".yaml", ".yml"]:
            data = yaml.safe_load(content)
        elif file_path.suffix == ".toml":
            data = rtoml.loads(content)
        else:
            # For other file types, create a basic material entry
            data = {
                "name": file_path.stem,
                "version": "1.0",
                "usage": "",
                "content": content,
                "content_type": "text"
            }

        # Ensure required fields
        material_data = {
            "name": data.get("name", file_path.stem),
            "version": data.get("version", "1.0"),
            "usage": data.get("usage", ""),
            "usage_examples": json.dumps(data.get("usage_examples", [])) if isinstance(data.get("usage_examples"), list) else data.get("usage_examples", ""),
            "type": data.get("type", "material"),
            "location": data.get("location", "project"),
            "default_status": data.get("default_status", "enabled"),
            "current_status": data.get("current_status", "enabled"),
            "override": data.get("override", False),
            "content": data.get("content", content),
            "content_type": data.get("content_type", file_path.suffix[1:] if file_path.suffix else "text"),
            "path": str(file_path),
            "material_metadata": data.get("metadata", {}),
            "agents": data.get("agents", {})
        }

        return material_data

    except Exception as e:
        _log.error(f"Error parsing material file {file_path}: {e}")
        return None


async def migrate_material(file_path: Path) -> bool:
    """Migrate a single material file to the database."""
    try:
        material_data = await parse_material_file(file_path)
        if not material_data:
            return False

        # Check if material already exists
        async with db_manager.session() as session:
            result = await session.execute(
                select(Material).where(Material.name == material_data["name"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                _log.info(f"Material {material_data['name']} already exists in database")
                return True

            # Create new material
            material = Material(**material_data)
            session.add(material)
            await session.commit()
            _log.info(f"Successfully migrated material {material_data['name']}")
            return True

    except Exception as e:
        _log.error(f"Error migrating material {file_path}: {e}")
        return False


async def migrate_materials_to_db() -> Tuple[int, int]:
    """
    Migrate all materials from filesystem to database.
    Returns tuple of (success_count, total_count).
    """
    print("\n🔄 Starting materials migration...")

    # Find all material files
    project_root = Path.cwd()
    material_files = find_material_files(project_root)
    total_count = len(material_files)

    if total_count == 0:
        print("❌ No material files found")
        return 0, 0

    print(f"📦 Found {total_count} material files")

    # Migrate each material
    success_count = 0
    for file_path in material_files:
        if await migrate_material(file_path):
            success_count += 1
            print(f"✅ Migrated {file_path.name} ({success_count}/{total_count})")
        else:
            print(f"❌ Failed to migrate {file_path.name}")

    print(f"\n✅ Migration complete: {success_count}/{total_count} materials migrated successfully")
    return success_count, total_count


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Run migration
    asyncio.run(migrate_materials_to_db())
