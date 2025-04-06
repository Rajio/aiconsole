"""
Script to recreate database tables.
"""

from aiconsole.database import db_manager
from aiconsole.database.models import Base

def recreate_tables():
    """Drop all tables and recreate them."""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=db_manager.engine)
    
    print("Creating tables...")
    Base.metadata.create_all(bind=db_manager.engine)
    
    print("Tables recreated successfully!")

if __name__ == "__main__":
    recreate_tables() 