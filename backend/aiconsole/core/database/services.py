from sqlalchemy import select
from sqlalchemy.orm import Session

from aiconsole.core.database.ai_material import AIMaterial
from aiconsole.core.database.models import Agent, Material, Project


class MaterialService:
    """Service for managing materials in the database"""

    def __init__(self, db: Session):
        """Initialize service with database session"""
        self.db = db

    def get_material(self, material_id: str) -> Material:
        """Get material by ID"""
        result = self.db.execute(select(Material).where(Material.id == material_id))
        return result.scalar_one_or_none()

    def get_project_materials(self, project_id: str) -> list[Material]:
        """Get all materials for a project"""
        result = self.db.execute(select(Material).where(Material.project_id == project_id))
        return result.scalars().all()

    def save_material(self, material: AIMaterial, project_id: str) -> Material:
        """Save new material to database"""
        db_material = Material(
            id=material.id,
            name=material.name,
            version=material.version,
            usage=material.usage,
            content_type=material.content_type,
            content=material.content,
            default_status=material.default_status,
            project_id=project_id,
        )
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def update_material(self, material: AIMaterial, project_id: str) -> Material:
        """Update existing material in database"""
        db_material = self.get_material(material.id)
        if not db_material:
            return self.save_material(material, project_id)

        db_material.name = material.name
        db_material.version = material.version
        db_material.usage = material.usage
        db_material.content_type = material.content_type
        db_material.content = material.content
        db_material.default_status = material.default_status

        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def delete_material(self, material_id: str):
        """Delete material from database"""
        material = self.get_material(material_id)
        if material:
            self.db.delete(material)
            self.db.commit()


class AgentService:
    """Service for managing AI agents in the database"""

    def __init__(self, db: Session):
        """Initialize service with database session"""
        self.db = db

    def get_agent(self, agent_id: str) -> Agent:
        """Get agent by ID"""
        result = self.db.execute(select(Agent).where(Agent.id == agent_id))
        return result.scalar_one_or_none()

    def get_project_agents(self, project_id: str) -> list[Agent]:
        """Get all agents for a project"""
        result = self.db.execute(select(Agent).where(Agent.project_id == project_id))
        return result.scalars().all()

    def get_user_agents(self, user_id: str) -> list[Agent]:
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
