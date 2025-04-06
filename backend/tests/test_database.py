"""
Tests for database operations.
"""

import pytest
from sqlalchemy.exc import SQLAlchemyError

from aiconsole.database import db_manager
from aiconsole.database.models import Material


@pytest.fixture
def test_material_data():
    return {
        "name": "test_material",
        "version": "1.0",
        "usage": "Test usage",
        "type": "material",
        "location": "project",
        "default_status": "enabled",
        "current_status": "enabled",
        "content": "Test content",
        "content_type": "text",
    }


def test_database_connection():
    """Test database connection."""
    try:
        with db_manager.get_session() as session:
            session.execute("SELECT 1")
    except SQLAlchemyError as e:
        pytest.fail(f"Database connection failed: {e}")


def test_material_creation(test_material_data):
    """Test material creation."""
    try:
        material = db_manager.create_material(test_material_data)
        assert material.name == test_material_data["name"]
        assert material.version == test_material_data["version"]
        assert material.usage == test_material_data["usage"]
        assert material.type == test_material_data["type"]
        assert material.location == test_material_data["location"]
        assert material.default_status == test_material_data["default_status"]
        assert material.current_status == test_material_data["current_status"]
        assert material.content == test_material_data["content"]
        assert material.content_type == test_material_data["content_type"]

        # Clean up
        db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material creation failed: {e}")


def test_material_retrieval(test_material_data):
    """Test material retrieval."""
    try:
        # Create a test material
        material = db_manager.create_material(test_material_data)

        # Retrieve the material
        retrieved_material = db_manager.get_material(material.id)
        assert retrieved_material is not None
        assert retrieved_material.name == test_material_data["name"]
        assert retrieved_material.version == test_material_data["version"]
        assert retrieved_material.usage == test_material_data["usage"]
        assert retrieved_material.type == test_material_data["type"]
        assert retrieved_material.location == test_material_data["location"]
        assert retrieved_material.default_status == test_material_data["default_status"]
        assert retrieved_material.current_status == test_material_data["current_status"]
        assert retrieved_material.content == test_material_data["content"]
        assert retrieved_material.content_type == test_material_data["content_type"]

        # Clean up
        db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material retrieval failed: {e}")


def test_material_update(test_material_data):
    """Test material update."""
    try:
        # Create a test material
        material = db_manager.create_material(test_material_data)

        # Update the material
        updated_data = test_material_data.copy()
        updated_data["name"] = "updated_material"
        updated_data["version"] = "2.0"
        updated_material = db_manager.update_material(material.id, updated_data)

        assert updated_material is not None
        assert updated_material.name == updated_data["name"]
        assert updated_material.version == updated_data["version"]
        assert updated_material.usage == updated_data["usage"]
        assert updated_material.type == updated_data["type"]
        assert updated_material.location == updated_data["location"]
        assert updated_material.default_status == updated_data["default_status"]
        assert updated_material.current_status == updated_data["current_status"]
        assert updated_material.content == updated_data["content"]
        assert updated_material.content_type == updated_data["content_type"]

        # Clean up
        db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material update failed: {e}")


def test_material_deletion(test_material_data):
    """Test material deletion."""
    try:
        # Create a test material
        material = db_manager.create_material(test_material_data)

        # Delete the material
        success = db_manager.delete_material(material.id)
        assert success is True

        # Verify the material is deleted
        deleted_material = db_manager.get_material(material.id)
        assert deleted_material is None
    except SQLAlchemyError as e:
        pytest.fail(f"Material deletion failed: {e}")


def test_material_listing(test_material_data):
    """Test material listing."""
    try:
        # Create a test material
        material = db_manager.create_material(test_material_data)

        # Get all materials
        materials = db_manager.get_all_materials()
        assert len(materials) > 0
        assert any(m.id == material.id for m in materials)

        # Clean up
        db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material listing failed: {e}")


def test_material_by_name(test_material_data):
    """Test getting material by name."""
    try:
        # Create a test material
        material = db_manager.create_material(test_material_data)

        # Get material by name
        retrieved_material = db_manager.get_material_by_name(test_material_data["name"])
        assert retrieved_material is not None
        assert retrieved_material.name == test_material_data["name"]
        assert retrieved_material.version == test_material_data["version"]
        assert retrieved_material.usage == test_material_data["usage"]
        assert retrieved_material.type == test_material_data["type"]
        assert retrieved_material.location == test_material_data["location"]
        assert retrieved_material.default_status == test_material_data["default_status"]
        assert retrieved_material.current_status == test_material_data["current_status"]
        assert retrieved_material.content == test_material_data["content"]
        assert retrieved_material.content_type == test_material_data["content_type"]

        # Clean up
        db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Getting material by name failed: {e}")


def test_database_error_handling():
    """Test database error handling."""
    try:
        # Try to create a material with invalid data
        invalid_data = {
            "name": None,  # This should cause an error
            "version": "1.0",
        }
        db_manager.create_material(invalid_data)
        pytest.fail("Expected an error when creating material with invalid data")
    except SQLAlchemyError:
        # This is expected
        pass
