import uuid
from datetime import datetime
from typing import Any, BinaryIO, Dict, List, Optional, Sequence, cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from aiconsole.core.database.ai_material import AIMaterial
from aiconsole.core.database.errors import DuplicateError, NotFoundError
from aiconsole.core.database.models import (
    Agent,
    Material,
    Project,
    User,
    UserAvatar,
    UserProfile,
)
from aiconsole.core.database.session import get_db
from aiconsole.core.users.types import UserProfile as UserProfileType


class MaterialService:
    """Service for managing materials in the database"""

    def __init__(self, db: Session):
        """Initialize service with database session"""
        self.db = db

    def get_material(self, material_id: str) -> Optional[Material]:
        """Get material by ID"""
        result = self.db.execute(select(Material).where(Material.id == material_id))
        return result.scalar_one_or_none()

    def get_project_materials(self, project_id: str) -> Sequence[Material]:
        """Get all materials for a project"""
        result = self.db.execute(select(Material).where(Material.project_id == project_id))
        return result.scalars().all()

    def save_material(self, material: AIMaterial, project_id: str) -> Material:
        """Save new material to database"""
        data = {
            "id": material.id,
            "name": material.name,
            "version": material.version,
            "usage": material.usage,
            "content_type": material.content_type,
            "content": material.content,
            "default_status": material.default_status,
            "project_id": project_id,
        }
        db_material = Material(**data)
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def update_material(self, material: AIMaterial, project_id: str) -> Material:
        """Update existing material in database"""
        db_material = self.get_material(material.id)
        if not db_material:
            return self.save_material(material, project_id)

        data = {
            "name": material.name,
            "version": material.version,
            "usage": material.usage,
            "content_type": material.content_type,
            "content": material.content,
            "default_status": material.default_status,
        }
        for key, value in data.items():
            setattr(db_material, key, value)

        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def delete_material(self, material_id: str):
        """Delete material from database"""
        material = self.get_material(material_id)
        if material:
            self.db.delete(material)
            self.db.commit()

    def get_materials(self, project_id: str) -> Sequence[Material]:
        """
        Get all materials for a project

        Args:
            project_id: Project ID

        Returns:
            Sequence[Material]: List of materials
        """
        with get_db() as db:
            return db.query(Material).filter(Material.project_id == project_id).all()

    def create_material(
        self,
        project_id: str,
        name: str,
        version: str,
        usage: str,
        content_type: str,
        content: str,
        default_status: str,
    ) -> Material:
        """
        Create a new material

        Args:
            project_id: Project ID
            name: Material name
            version: Material version
            usage: Material usage
            content_type: Content type
            content: Material content
            default_status: Default status

        Returns:
            Material: Created material
        """
        with get_db() as db:
            data: Dict[str, Any] = {
                "id": str(uuid.uuid4()),
                "project_id": project_id,
                "name": name,
                "version": version,
                "usage": usage,
                "content_type": content_type,
                "content": content,
                "default_status": default_status,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            material = Material(**data)
            db.add(material)
            db.commit()
            db.refresh(material)
            return material


class AgentService:
    """Service for managing AI agents in the database"""

    def __init__(self, db: Session):
        """Initialize service with database session"""
        self.db = db

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Get agent by ID

        Args:
            agent_id: Agent ID

        Returns:
            Optional[Agent]: Agent if found
        """
        with get_db() as db:
            return db.query(Agent).filter(Agent.id == agent_id).first()

    def get_project_agents(self, project_id: str) -> Sequence[Agent]:
        """Get all agents for a project"""
        result = self.db.execute(select(Agent).where(Agent.project_id == project_id))
        return result.scalars().all()

    def get_user_agents(self, user_id: str) -> Sequence[Agent]:
        """Get all agents for a user"""
        result = self.db.execute(select(Agent).where(Agent.owner_id == user_id))
        return result.scalars().all()

    def create_agent(
        self,
        name: str,
        system_prompt: str,
        project_id: str,
        owner_id: str,
        description: str | None = None,
        temperature: str = "0.7",
        max_tokens: str | None = None,
        model: str = "gpt-3.5-turbo",
        is_active: bool = True,
    ) -> Agent:
        """Create a new agent"""
        agent = Agent(
            name=name,
            system_prompt=system_prompt,
            project_id=project_id,
            owner_id=owner_id,
            description=description,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
            is_active=is_active,
        )
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        return agent

    def update_agent(self, agent_id: str, **kwargs) -> Agent:
        """Update agent information"""
        agent = self.get_agent(agent_id)
        if agent:
            for key, value in kwargs.items():
                setattr(agent, key, value)
            self.db.commit()
            self.db.refresh(agent)
        return agent

    def delete_agent(self, agent_id: str) -> bool:
        """Delete agent from database"""
        agent = self.get_agent(agent_id)
        if agent:
            self.db.delete(agent)
            self.db.commit()
            return True
        return False

    def get_agents(self, project_id: str) -> Sequence[Agent]:
        """
        Get all agents for a project

        Args:
            project_id: Project ID

        Returns:
            Sequence[Agent]: List of agents
        """
        with get_db() as db:
            return db.query(Agent).filter(Agent.project_id == project_id).all()


class UserProfileService:
    """Service for managing user profiles in the database"""

    def get_profile(self, user_id: str) -> Optional[UserProfileType]:
        """Get user profile"""
        with get_db() as db:
            profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
            if not profile:
                return None

            return UserProfileType(
                id=user_id,
                username=profile.username,
                email=profile.email,
                avatar_url=profile.avatar_url,
                gravatar=False,
            )

    def save_profile(self, profile: UserProfileType) -> UserProfileType:
        """Save user profile"""
        with get_db() as db:
            # Check if username exists
            existing = (
                db.query(UserProfile)
                .filter(UserProfile.username == profile.username, UserProfile.id != profile.id)
                .first()
            )

            if existing:
                raise DuplicateError(f"Username already exists: {profile.username}")

            # Get or create profile
            db_profile = db.query(UserProfile).filter(UserProfile.id == profile.id).first()

            if not db_profile:
                db_profile = UserProfile(
                    id=profile.id,
                    username=profile.username,
                    email=profile.email or "",
                    avatar_url=profile.avatar_url,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.add(db_profile)
            else:
                db_profile.username = profile.username
                db_profile.email = profile.email or ""
                db_profile.avatar_url = profile.avatar_url
                db_profile.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(db_profile)

            return UserProfileType(
                id=profile.id,
                username=db_profile.username,
                email=db_profile.email,
                avatar_url=db_profile.avatar_url,
                gravatar=False,
            )

    def save_avatar(self, email: str, avatar_url: str) -> None:
        """Save user avatar URL"""
        with get_db() as db:
            profile = db.query(UserProfile).filter(UserProfile.email == email).first()
            if not profile:
                raise NotFoundError(f"Profile not found for email: {email}")

            profile.avatar_url = avatar_url
            db.commit()

    def _create_default_profile(self, db: Session) -> UserProfileType:
        """Create default user profile"""
        profile = UserProfile(
            id=str(uuid.uuid4()),
            username="default",
            email="default@example.com",
            avatar_url=self._get_default_avatar(),
        )
        db.add(profile)
        db.commit()
        return self._convert_to_type(profile)

    def _create_profile(self, db: Session, email: str) -> UserProfileType:
        """Create new user profile"""
        profile = UserProfile(
            id=str(uuid.uuid4()), username=email.split("@")[0], email=email, avatar_url=self._get_default_avatar(email)
        )
        db.add(profile)
        db.commit()
        return self._convert_to_type(profile)

    def _get_default_avatar(self, email: Optional[str] = None) -> str:
        """Get default avatar URL"""
        # TODO: Implement default avatar generation logic
        return "default_avatar.png"

    def _convert_to_type(self, profile: UserProfile) -> UserProfileType:
        """Convert database model to type"""
        return UserProfileType(username=profile.username, email=profile.email, avatar_url=profile.avatar_url)


class UserAvatarService:
    """Service for managing user avatars in the database"""

    def save_avatar(self, user_id: str, file: BinaryIO, filename: str, content_type: str) -> UserAvatar:
        """
        Save user avatar to database

        Args:
            user_id: User ID
            file: Binary file data
            filename: Original filename
            content_type: File content type

        Returns:
            UserAvatar: Created avatar record

        Raises:
            NotFoundError: If user not found
        """
        with get_db() as db:
            # Check if user exists
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError(f"User not found: {user_id}")

            # Read file data
            file_data = file.read()

            # Create avatar record
            data: Dict[str, Any] = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "filename": filename,
                "content_type": content_type,
                "data": file_data,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            avatar = UserAvatar(**data)

            db.add(avatar)
            db.commit()
            db.refresh(avatar)

            return avatar

    def get_avatar(self, user_id: str, filename: str) -> Optional[UserAvatar]:
        """
        Get user avatar by filename

        Args:
            user_id: User ID
            filename: Avatar filename

        Returns:
            Optional[UserAvatar]: Avatar record if found
        """
        with get_db() as db:
            return db.query(UserAvatar).filter(UserAvatar.user_id == user_id, UserAvatar.filename == filename).first()

    def get_user_avatars(self, user_id: str) -> Sequence[UserAvatar]:
        """
        Get all avatars for a user

        Args:
            user_id: User ID

        Returns:
            Sequence[UserAvatar]: List of user avatars
        """
        with get_db() as db:
            return db.query(UserAvatar).filter(UserAvatar.user_id == user_id).all()

    def delete_avatar(self, user_id: str, filename: str) -> bool:
        """
        Delete user avatar

        Args:
            user_id: User ID
            filename: Avatar filename

        Returns:
            bool: True if deleted
        """
        with get_db() as db:
            avatar = self.get_avatar(user_id, filename)
            if avatar:
                db.delete(avatar)
                db.commit()
                return True
            return False
