from pathlib import Path
from typing import Optional

import rtoml

from aiconsole.core.database.ai_material import AIMaterial


def load_material(file_path: Path) -> Optional[AIMaterial]:
    """Load material from TOML file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = rtoml.load(f)

        return AIMaterial(
            id=file_path.stem,
            name=data.get("name", file_path.stem),
            version=data.get("version", "0.0.1"),
            usage=data.get("usage", ""),
            content_type=data.get("content_type", "STATIC_TEXT"),
            content=data.get("content", ""),
            default_status=data.get("default_status", "ENABLED"),
        )
    except Exception as e:
        print(f"Error loading material {file_path}: {e}")
        return None


def load_agent(file_path: Path) -> Optional[dict]:
    """Load agent from TOML file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = rtoml.load(f)
            data["id"] = file_path.stem
            return data
    except Exception as e:
        print(f"Error loading agent {file_path}: {e}")
        return None
