import os
import pytest
from datetime import datetime
from sqlalchemy import text

from aiconsole.database.manager import DatabaseManager
from aiconsole.database.models import Material
from aiconsole.tests.test_settings import POSTGRES_CONFIG

def setup_test_env():
    """Set up test environment variables for PostgreSQL"""
    for key, value in POSTGRES_CONFIG.items():
        os.environ[key] = str(value)

@pytest.fixture(scope="function")
def db():
    """Database fixture for PostgreSQL"""
    # Set up PostgreSQL environment
    setup_test_env()
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Create tables
    db_manager.create_tables()
    
    yield db_manager
    
    # Cleanup: Drop all tables after tests
    with db_manager.engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.commit()

def test_create_and_get_material(db):
    # Test data
    material_data = {
        "name": "test_material",
        "version": "1.0.0",
        "type": "material",
        "location": "project",
        "default_status": "enabled",
        "current_status": "enabled",
        "content": "test content",
        "content_type": "text"
    }
    
    # Create material
    material = db.create_material(material_data)
    assert material.id is not None
    assert material.name == "test_material"
    
    # Get material by id
    retrieved = db.get_material(material.id)
    assert retrieved is not None
    assert retrieved.name == material.name
    assert retrieved.content == material.content
    
    # Get material by name
    retrieved = db.get_material_by_name("test_material")
    assert retrieved is not None
    assert retrieved.id == material.id
    
    # Get all materials
    materials = db.get_all_materials()
    assert len(materials) == 1
    assert materials[0].id == material.id
    
    # Update material
    updated = db.update_material(material.id, {"content": "updated content"})
    assert updated is not None
    assert updated.content == "updated content"
    
    # Delete material
    assert db.delete_material(material.id) is True
    assert db.get_material(material.id) is None 