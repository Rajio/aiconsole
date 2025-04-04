import re
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    LargeBinary,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()


class UserProfile(Base):
    """User profile model for storing user profile information"""

    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile", uselist=False)

    # Indexes
    __table_args__ = (Index("idx_userprofile_username_email", "username", "email"),)

    def __init__(self, **kwargs):
        """Initialize UserProfile with keyword arguments"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @validates("email")
    def validate_email(self, key: str, email: str) -> str:
        """Validate email format"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @validates("username")
    def validate_username(self, key: str, username: str) -> str:
        """Validate username format"""
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            raise ValueError("Username can only contain letters, numbers, underscores and hyphens")
        return username


class User(Base):
    """User model for storing user information"""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    projects = relationship("Project", back_populates="owner")
    materials = relationship("Material", back_populates="owner")
    agents = relationship("Agent", back_populates="owner")
    avatars = relationship("UserAvatar", back_populates="user")

    # Indexes
    __table_args__ = (Index("idx_user_username_email", "username", "email"),)

    @validates("email")
    def validate_email(self, key: str, email: str) -> str:
        """Validate email format"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @validates("username")
    def validate_username(self, key: str, username: str) -> str:
        """Validate username format"""
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            raise ValueError("Username can only contain letters, numbers, underscores and hyphens")
        return username


class Project(Base):
    """Project model for storing project information"""

    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)

    # Relationships
    materials = relationship("Material", back_populates="project")
    owner = relationship("User", back_populates="projects")
    agents = relationship("Agent", back_populates="project")

    # Indexes
    __table_args__ = (Index("idx_project_owner_name", "owner_id", "name"),)

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        """Validate project name"""
        if not name.strip():
            raise ValueError("Project name cannot be empty")
        return name.strip()


class Material(Base):
    """Material model for storing material information"""

    __tablename__ = "materials"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    version = Column(String, nullable=False, default="0.0.1")
    usage = Column(String, nullable=False)
    content_type = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    default_status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)

    # Relationships
    project = relationship("Project", back_populates="materials")
    owner = relationship("User", back_populates="materials")

    # Indexes
    __table_args__ = (Index("idx_material_project_type", "project_id", "content_type"),)

    @validates("content_type")
    def validate_content_type(self, key: str, content_type: str) -> str:
        """Validate content type"""
        valid_types = ["text", "code", "image", "file"]
        if content_type not in valid_types:
            raise ValueError(f"Content type must be one of: {', '.join(valid_types)}")
        return content_type


class Agent(Base):
    """Agent model for storing agent information"""

    __tablename__ = "agents"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=False)
    temperature = Column(String, nullable=True)
    max_tokens = Column(String, nullable=True)
    model = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)

    # Relationships
    project = relationship("Project", back_populates="agents")
    owner = relationship("User", back_populates="agents")

    # Indexes
    __table_args__ = (Index("idx_agent_project_model", "project_id", "model"),)

    @validates("temperature")
    def validate_temperature(self, key: str, temperature: Optional[str]) -> Optional[str]:
        """Validate temperature value"""
        if temperature is not None:
            try:
                temp = float(temperature)
                if not 0 <= temp <= 2:
                    raise ValueError("Temperature must be between 0 and 2")
            except ValueError:
                raise ValueError("Temperature must be a valid number")
        return temperature

    @validates("model")
    def validate_model(self, key: str, model: str) -> str:
        """Validate model name"""
        valid_models = ["gpt-3.5-turbo", "gpt-4", "claude-2", "claude-instant"]
        if model not in valid_models:
            raise ValueError(f"Model must be one of: {', '.join(valid_models)}")
        return model


class UserAvatar(Base):
    """User avatar model for storing avatar images in the database"""

    __tablename__ = "user_avatars"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="avatars")

    # Indexes
    __table_args__ = (Index("idx_useravatar_user_filename", "user_id", "filename"),)

    @validates("content_type")
    def validate_content_type(self, key: str, content_type: str) -> str:
        """Validate content type"""
        valid_types = ["image/jpeg", "image/png", "image/gif"]
        if content_type not in valid_types:
            raise ValueError(f"Content type must be one of: {', '.join(valid_types)}")
        return content_type
