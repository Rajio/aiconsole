"""
Extended tests for database operations.
"""

import pytest
from sqlalchemy.exc import SQLAlchemyError

from aiconsole.core.assets.types import AssetLocation, AssetStatus, AssetType
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
        "material_metadata": {"key": "value"},
        "agents": {"agent1": {"skills": ["skill1", "skill2"]}},
    }


def test_material_with_metadata(test_db_manager, test_material_data):
    """Test material creation and retrieval with metadata."""
    try:
        # Create material with metadata
        material = test_db_manager.create_material(test_material_data)
        
        # Retrieve and verify metadata
        retrieved_material = test_db_manager.get_material(material.id)
        assert retrieved_material.material_metadata == test_material_data["material_metadata"]
        assert retrieved_material.agents == test_material_data["agents"]
        
        # Clean up
        test_db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material metadata test failed: {e}")


def test_material_status_transitions(test_db_manager, test_material_data):
    """Test material status transitions."""
    try:
        # Create material
        material = test_db_manager.create_material(test_material_data)
        
        # Test status transitions
        statuses = ["enabled", "disabled", "forced"]
        for status in statuses:
            # Update status
            update_data = test_material_data.copy()
            update_data["current_status"] = status
            updated_material = test_db_manager.update_material(material.id, update_data)
            
            # Verify status
            assert updated_material.current_status == status
            
            # Retrieve and verify status
            retrieved_material = test_db_manager.get_material(material.id)
            assert retrieved_material.current_status == status
        
        # Clean up
        test_db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material status transitions test failed: {e}")


def test_material_location_changes(test_db_manager, test_material_data):
    """Test material location changes."""
    try:
        # Create material in project location
        material = test_db_manager.create_material(test_material_data)
        
        # Change location to aiconsole
        update_data = test_material_data.copy()
        update_data["location"] = "aiconsole"
        updated_material = test_db_manager.update_material(material.id, update_data)
        
        # Verify location change
        assert updated_material.location == "aiconsole"
        
        # Retrieve and verify location
        retrieved_material = test_db_manager.get_material(material.id)
        assert retrieved_material.location == "aiconsole"
        
        # Clean up
        test_db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material location changes test failed: {e}")


def test_material_content_updates(test_db_manager, test_material_data):
    """Test material content updates."""
    try:
        # Create material
        material = test_db_manager.create_material(test_material_data)
        
        # Update content
        new_content = "Updated test content"
        update_data = test_material_data.copy()
        update_data["content"] = new_content
        updated_material = test_db_manager.update_material(material.id, update_data)
        
        # Verify content update
        assert updated_material.content == new_content
        
        # Retrieve and verify content
        retrieved_material = test_db_manager.get_material(material.id)
        assert retrieved_material.content == new_content
        
        # Clean up
        test_db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material content updates test failed: {e}")


def test_material_version_management(test_db_manager, test_material_data):
    """Test material version management."""
    try:
        # Create material
        material = test_db_manager.create_material(test_material_data)
        
        # Update version
        new_version = "2.0"
        update_data = test_material_data.copy()
        update_data["version"] = new_version
        updated_material = test_db_manager.update_material(material.id, update_data)
        
        # Verify version update
        assert updated_material.version == new_version
        
        # Retrieve and verify version
        retrieved_material = test_db_manager.get_material(material.id)
        assert retrieved_material.version == new_version
        
        # Clean up
        test_db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material version management test failed: {e}")


def test_material_duplicate_name_handling(test_db_manager, test_material_data):
    """Test handling of duplicate material names."""
    try:
        # Create first material
        material1 = test_db_manager.create_material(test_material_data)
        
        # Try to create second material with same name
        with pytest.raises(SQLAlchemyError):
            test_db_manager.create_material(test_material_data)
        
        # Clean up
        test_db_manager.delete_material(material1.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material duplicate name handling test failed: {e}")


def test_material_bulk_operations(test_db_manager, test_material_data):
    """Test bulk material operations."""
    try:
        # Create multiple materials
        materials = []
        for i in range(5):
            data = test_material_data.copy()
            data["name"] = f"test_material_{i}"
            material = test_db_manager.create_material(data)
            materials.append(material)
        
        # Verify all materials were created
        all_materials = test_db_manager.get_all_materials()
        assert len(all_materials) >= 5
        
        # Clean up
        for material in materials:
            test_db_manager.delete_material(material.id)
    except SQLAlchemyError as e:
        pytest.fail(f"Material bulk operations test failed: {e}") 