import os
from pathlib import Path

import rtoml

from aiconsole.core.assets.materials.material import Material as MaterialModel
from aiconsole.core.database.config import db_manager
from aiconsole.core.database.services import MaterialService


def migrate_materials_to_db(project_id: str):
    """Migrate materials from filesystem to database"""
    session = db_manager.get_session()
    service = MaterialService(session)

    # gtm
    materials_dir = Path(os.getenv("MATERIALS_DIR", "materials"))
    if not materials_dir.exists():
        return

    for toml_file in materials_dir.glob("*.toml"):
        # Load material data from .toml file
        material_data = rtoml.load(toml_file.open("r"))

        # Create material object
        material = MaterialModel(
            id=material_data.get("id"),
            name=material_data.get("name"),
            version=material_data.get("version", "0.0.1"),
            usage=material_data.get("usage", ""),
            content_type=material_data.get("content_type", "STATIC_TEXT"),
            content=material_data.get("content", ""),
            default_status=material_data.get("default_status", "ENABLED"),
        )

        service.save_material(material, project_id)
