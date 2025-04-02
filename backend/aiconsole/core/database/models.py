from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model for storing user information"""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    projects = relationship("Project", back_populates="owner")
    materials = relationship("Material", back_populates="owner")
    agents = relationship("Agent", back_populates="owner")


class Project(Base):
    """Project model for storing project information"""

    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)

    # Relationships
    materials = relationship("Material", back_populates="project")
    owner = relationship("User", back_populates="projects")
    agents = relationship("Agent", back_populates="project")


class Material(Base):
    """Material model for storing material information"""

    __tablename__ = "materials"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False, default="0.0.1")
    usage = Column(String, nullable=False)
    content_type = Column(Enum("STATIC_TEXT", "DYNAMIC_TEXT", "API", name="material_content_type"), nullable=False)
    content = Column(Text, nullable=False)
    default_status = Column(Enum("ENABLED", "DISABLED", name="asset_status"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="materials")
    owner = relationship("User", back_populates="materials")


class Agent(Base):
    """Agent model for storing AI agent information"""

    __tablename__ = "agents"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=False)
    temperature = Column(String, nullable=False, default="0.7")
    max_tokens = Column(String, nullable=True)
    model = Column(String, nullable=False, default="gpt-3.5-turbo")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="agents")
    owner = relationship("User", back_populates="agents")
