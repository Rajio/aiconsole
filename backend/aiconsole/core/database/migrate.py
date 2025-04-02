import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from aiconsole.core.database.ai_material import AIMaterial
from aiconsole.core.database.loader import load_agent, load_material
from aiconsole.core.database.models import Agent, Base, Material, Project, User

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def migrate():
    """Run database migration"""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = SessionLocal()

    try:
        # Create system user if not exists
        system_user = session.execute(select(User).where(User.id == "system")).scalar_one_or_none()

        if not system_user:
            system_user = User(
                id="system",
                username="system",
                email="system@aiconsole.local",
                password_hash="",  # No password for system user
                is_active=True,
                is_admin=True,
            )
            session.add(system_user)
            session.commit()

        # Get or create default project
        default_project = session.execute(select(Project).where(Project.id == "default")).scalar_one_or_none()

        if not default_project:
            default_project = Project(id="default", name="Default Project")
            session.add(default_project)
            session.commit()

        # Migrate materials
        materials_dir = Path("aiconsole/core/assets/materials")
        if materials_dir.exists():
            for material_file in materials_dir.glob("*.toml"):
                try:
                    material = load_material(material_file)
                    if material:
                        # Convert content type and status to uppercase
                        material.content_type = material.content_type.upper()
                        material.default_status = material.default_status.upper()

                        # Save to database
                        db_material = Material(
                            id=material.id,
                            name=material.name,
                            version=material.version,
                            usage=material.usage,
                            content_type=material.content_type,
                            content=material.content,
                            default_status=material.default_status,
                            project_id=default_project.id,
                            owner_id=system_user.id,
                        )
                        session.add(db_material)
                except Exception as e:
                    print(f"Error migrating material {material_file}: {e}")

        # Migrate agents from preinstalled directory
        agents_dir = Path("aiconsole/preinstalled/agents")
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.toml"):
                try:
                    agent_data = load_agent(agent_file)
                    if agent_data:
                        # Check if agent already exists
                        existing_agent = session.execute(
                            select(Agent).where(Agent.id == agent_data["id"])
                        ).scalar_one_or_none()

                        if not existing_agent:
                            agent = Agent(
                                id=agent_data["id"],
                                name=agent_data.get("name", agent_data["id"]),
                                description=agent_data.get("description", ""),
                                system_prompt=agent_data.get("system_prompt", ""),
                                temperature=str(agent_data.get("temperature", "0.7")),
                                max_tokens=str(agent_data.get("max_tokens")) if "max_tokens" in agent_data else None,
                                model=agent_data.get("model", "gpt-3.5-turbo"),
                                is_active=agent_data.get("is_active", True),
                                project_id=default_project.id,
                                owner_id=system_user.id,
                            )
                            session.add(agent)
                except Exception as e:
                    print(f"Error migrating agent {agent_file}: {e}")

        session.commit()
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    migrate()
