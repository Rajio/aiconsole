# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import traceback
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

from aiconsole.core.assets.materials.documentation_from_code import (
    documentation_from_code,
)
from aiconsole.core.assets.materials.rendered_material import RenderedMaterial
from aiconsole.core.assets.types import Asset, AssetLocation, AssetStatus, AssetType
from aiconsole.database import db_manager
from aiconsole.database.models import Material as DBMaterial
from aiconsole.utils.events import InternalEvent, internal_events

if TYPE_CHECKING:
    from aiconsole.core.assets.materials.content_evaluation_context import (
        ContentEvaluationContext,
    )


@dataclass(frozen=True, slots=True)
class MaterialRenderErrorEvent(InternalEvent):
    pass


class MaterialContentType(str, Enum):
    STATIC_TEXT = "static_text"
    DYNAMIC_TEXT = "dynamic_text"
    API = "api"


class Material(Asset):
    type: AssetType = AssetType.MATERIAL
    id: str
    name: str
    version: str = "0.0.1"
    usage: str
    defined_in: AssetLocation

    # Content, either static or dynamic
    content_type: MaterialContentType = MaterialContentType.STATIC_TEXT
    content: str = ""

    @classmethod
    async def from_db(cls, db_material: DBMaterial) -> "Material":
        """Create a Material instance from a database model."""
        return cls(
            id=str(db_material.id),
            name=db_material.name,
            version=db_material.version,
            usage=db_material.usage or "",
            defined_in=AssetLocation.PROJECT_DIR if db_material.location == "project" else AssetLocation.AICONSOLE,
            content_type=(
                MaterialContentType(db_material.content_type)
                if db_material.content_type
                else MaterialContentType.STATIC_TEXT
            ),
            content=db_material.content or "",
        )

    @classmethod
    async def get_by_id(cls, material_id: str) -> Optional["Material"]:
        """Get a material by its ID from the database."""
        async with db_manager.session() as session:
            db_material = await session.get(DBMaterial, int(material_id))
            if db_material:
                return await cls.from_db(db_material)
            return None

    async def save_to_db(self) -> None:
        """Save the material to the database."""
        db_material = DBMaterial(
            name=self.name,
            version=self.version,
            usage=self.usage,
            type=self.type.value,
            location="project" if self.defined_in == AssetLocation.PROJECT_DIR else "aiconsole",
            default_status="enabled",
            current_status="enabled",
            content=self.content,
            content_type=self.content_type.value,
        )

        async with db_manager.session() as session:
            session.add(db_material)
            await session.commit()

    def __hash__(self):
        return hash(self.id + self.version + self.name + self.usage + self.content_type + self.content)

    @property
    def inlined_content(self):
        # if starts with file:// then load the file, take into account file://./relative paths
        if self.content.startswith("file://"):
            content_file = self.content[len("file://") :]

            from aiconsole.core.project.paths import (
                get_core_assets_directory,
                get_project_assets_directory,
            )

            project_dir_path = get_project_assets_directory(self.type)
            core_resource_path = get_core_assets_directory(self.type)

            if (project_dir_path / content_file).exists():
                base_search_path = project_dir_path
            else:
                base_search_path = core_resource_path

            with open(base_search_path / content_file, "r", encoding="utf8", errors="replace") as file:
                return file.read()

        return self.content

    async def render(self, context: "ContentEvaluationContext"):
        header = f"# {self.name}\n\n"

        match self.content_type:
            case MaterialContentType.STATIC_TEXT:
                return RenderedMaterial(id=self.id, content=header + self.inlined_content, error="")
            case MaterialContentType.DYNAMIC_TEXT:
                return await self._handle_dynamic_text_content(context, header)
            case MaterialContentType.API:
                return await self._handle_api_content(context, header)
            case _:
                raise ValueError("Material has no content")

    async def _handle_dynamic_text_content(self, context, header):
        try:
            source_code = compile(self.inlined_content, "<string>", "exec")
            local_vars = {}
            exec(source_code, local_vars)
            content_func = local_vars.get("content")
            if callable(content_func):
                content = await content_func(context)
                return RenderedMaterial(id=self.id, content=header + content, error="")
            else:
                raise ValueError("No callable content function found!")
        except Exception:
            await internal_events().emit(
                MaterialRenderErrorEvent(), details=f"Error in DYNAMIC_TEXT material `{self.id}`"
            )
            error_details = RenderedMaterial(id=self.id, content="", error=traceback.format_exc())
            raise ValueError("Error in Dynamic Note material", error_details)

    async def _handle_api_content(self, context, header):
        try:
            compile(self.inlined_content, "temp_module", "exec")
            content = documentation_from_code(self, self.inlined_content)(context)
            return RenderedMaterial(id=self.id, content=header + content, error="")
        except Exception:
            await internal_events().emit(MaterialRenderErrorEvent(), details=f"Error in API material `{self.id}`")
            error_details = RenderedMaterial(id=self.id, content="", error=traceback.format_exc())
            raise ValueError("Error in Python API material", error_details)


class MaterialWithStatus(Material):
    status: AssetStatus = AssetStatus.ENABLED
