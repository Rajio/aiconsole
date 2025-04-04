import pytest
from sqlalchemy.exc import SQLAlchemyError

from aiconsole.core.database.manager import DatabaseManager
from aiconsole.core.database.models import Agent, Material, Project, User


def test_database_connection():
    """Test database connection"""
    db = DatabaseManager()
    assert db.engine is not None
    assert db.async_engine is not None


def test_user_creation():
    """Test user creation and validation"""
    db = DatabaseManager()
    with db.get_session() as session:
        # Create test user
        user = User(
            id="test_user", username="test_user", email="test@example.com", password_hash="test_hash", is_active=True
        )
        session.add(user)
        session.commit()

        # Verify user was created
        created_user = session.query(User).filter_by(username="test_user").first()
        assert created_user is not None
        assert created_user.email == "test@example.com"

        # Test email validation
        with pytest.raises(ValueError):
            user.email = "invalid_email"
            session.commit()


def test_project_creation():
    """Test project creation and relationships"""
    db = DatabaseManager()
    with db.get_session() as session:
        # Create test user
        user = User(
            id="project_test_user",
            username="project_test_user",
            email="project_test@example.com",
            password_hash="test_hash",
            is_active=True,
        )
        session.add(user)

        # Create test project
        project = Project(id="test_project", name="Test Project", owner_id=user.id)
        session.add(project)
        session.commit()

        # Verify project was created
        created_project = session.query(Project).filter_by(id="test_project").first()
        assert created_project is not None
        assert created_project.name == "Test Project"
        assert created_project.owner_id == user.id


def test_material_creation():
    """Test material creation and relationships"""
    db = DatabaseManager()
    with db.get_session() as session:
        # Create test project
        project = Project(id="material_test_project", name="Material Test Project")
        session.add(project)

        # Create test material
        material = Material(
            id="test_material",
            name="Test Material",
            content_type="text",
            content="Test content",
            project_id=project.id,
        )
        session.add(material)
        session.commit()

        # Verify material was created
        created_material = session.query(Material).filter_by(id="test_material").first()
        assert created_material is not None
        assert created_material.name == "Test Material"
        assert created_material.project_id == project.id


def test_agent_creation():
    """Test agent creation and relationships"""
    db = DatabaseManager()
    with db.get_session() as session:
        # Create test project
        project = Project(id="agent_test_project", name="Agent Test Project")
        session.add(project)

        # Create test agent
        agent = Agent(
            id="test_agent",
            name="Test Agent",
            description="Test agent description",
            system_prompt="Test system prompt",
            temperature="0.7",
            model="gpt-3.5-turbo",
            project_id=project.id,
        )
        session.add(agent)
        session.commit()

        # Verify agent was created
        created_agent = session.query(Agent).filter_by(id="test_agent").first()
        assert created_agent is not None
        assert created_agent.name == "Test Agent"
        assert created_agent.project_id == project.id


def test_database_error_handling():
    """Test database error handling"""
    db = DatabaseManager()
    with db.get_session() as session:
        # Try to create user with duplicate username
        user1 = User(
            id="duplicate_test", username="duplicate_user", email="test1@example.com", password_hash="test_hash"
        )
        session.add(user1)
        session.commit()

        # Try to create another user with same username
        user2 = User(
            id="duplicate_test2",
            username="duplicate_user",  # This should fail
            email="test2@example.com",
            password_hash="test_hash",
        )
        session.add(user2)

        with pytest.raises(SQLAlchemyError):
            session.commit()
