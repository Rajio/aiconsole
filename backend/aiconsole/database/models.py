from datetime import datetime
from typing import Dict

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Index, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    version = Column(String(50), nullable=False)
    usage = Column(Text, nullable=True)
    usage_examples = Column(Text, nullable=True)
    type = Column(String(50), nullable=False, default="material")
    location = Column(String(50), nullable=False)  # "project" or "aiconsole"
    default_status = Column(String(20), nullable=False)  # "enabled", "disabled", "forced"
    current_status = Column(String(20), nullable=False)  # "enabled", "disabled", "forced"
    override = Column(Boolean, default=False)
    content = Column(Text, nullable=True)
    content_type = Column(String(50), nullable=True)
    path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    material_metadata = Column(JSON, nullable=True)
    agents = Column(JSON, nullable=True)

    # Define indexes
    __table_args__ = (
        Index('ix_materials_name', 'name', unique=True),
    )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "usage": self.usage,
            "usage_examples": self.usage_examples,
            "type": self.type,
            "location": self.location,
            "default_status": self.default_status,
            "current_status": self.current_status,
            "override": self.override,
            "content": self.content,
            "content_type": self.content_type,
            "path": self.path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "material_metadata": self.material_metadata,
            "agents": self.agents,
        }
