from .manager import db_manager
from .models import Material

# Initialize the database tables
# db_manager.create_tables()  # Commented out to avoid automatic table creation

__all__ = ["db_manager", "Material"]
