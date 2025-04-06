import os
from pathlib import Path

from aiconsole.api.websockets.connection_manager import connection_manager
from aiconsole.api.websockets.server_messages import ErrorServerMessage
from aiconsole.core.assets.assets import Assets
from aiconsole.core.assets.fs.load_asset_from_fs import load_asset_from_fs
from aiconsole.core.assets.types import Asset, AssetLocation, AssetStatus, AssetType
from aiconsole.core.project.paths import (
    get_core_assets_directory,
    get_project_assets_directory,
)
from aiconsole.database import db_manager
from aiconsole.database.models import Material as DBMaterial
from aiconsole.utils.list_files_in_file_system import list_files_in_file_system


async def load_all_assets(asset_type: AssetType) -> dict[str, list[Asset]]:
    _assets: dict[str, list[Asset]] = {}

    # Load from database first if it's materials
    if asset_type == AssetType.MATERIAL:
        async with db_manager.session() as session:
            db_materials = await session.query(DBMaterial).all()
            for db_material in db_materials:
                try:
                    from aiconsole.core.assets.materials.material import Material

                    material = await Material.from_db(db_material)
                    if str(db_material.id) not in _assets:
                        _assets[str(db_material.id)] = []
                    _assets[str(db_material.id)].append(material)
                except Exception as e:
                    await connection_manager().send_to_all(
                        ErrorServerMessage(
                            error=f"Invalid material {db_material.id} {e}",
                        )
                    )
                    continue

    # Then load from filesystem
    locations = [
        [AssetLocation.PROJECT_DIR, get_project_assets_directory(asset_type)],
        [AssetLocation.AICONSOLE_CORE, get_core_assets_directory(asset_type)],
    ]

    for [location, dir] in locations:
        ids = set(
            [
                os.path.splitext(os.path.basename(path))[0]
                for path in list_files_in_file_system(dir)
                if os.path.splitext(Path(path))[-1] == ".toml"
            ]
        )

        for id in ids:
            try:
                asset = await load_asset_from_fs(asset_type, id, location)

                # Legacy support (for v. prior to 0.2.11)
                if Assets.get_status(asset.type, asset.id) == AssetStatus.FORCED:
                    Assets.set_status(asset.type, asset.id, AssetStatus.ENABLED)

                if id not in _assets:
                    _assets[id] = []
                _assets[id].append(asset)
            except Exception as e:
                await connection_manager().send_to_all(
                    ErrorServerMessage(
                        error=f"Invalid {asset_type} {id} {e}",
                    )
                )
                continue

    return _assets
