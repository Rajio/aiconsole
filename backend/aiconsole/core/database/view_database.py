import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select

from aiconsole.core.database.manager import DatabaseManager
from aiconsole.core.database.models import Material, Project, User


def view_database_contents():
    """View all contents of the database"""
    # Load environment variables
    backend_dir = Path(__file__).parent.parent.parent.parent
    load_dotenv(backend_dir / ".env")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL environment variable is not set")
        return

    db = DatabaseManager(database_url)
    with db.get_session() as session:
        # View users
        print("\n=== Users ===")
        users = session.execute(select(User)).scalars().all()
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Is Admin: {user.is_admin}")
            print(f"Is Active: {user.is_active}")
            print(f"Created: {user.created_at}")
            print(f"Updated: {user.updated_at}")

        # View projects
        print("\n=== Projects ===")
        projects = session.execute(select(Project)).scalars().all()
        for project in projects:
            print(f"\nProject ID: {project.id}")
            print(f"Name: {project.name}")
            print(f"Owner ID: {project.owner_id}")
            print(f"Created: {project.created_at}")
            print(f"Updated: {project.updated_at}")

        # View materials
        print("\n=== Materials ===")
        materials = session.execute(select(Material)).scalars().all()
        for material in materials:
            print(f"\nMaterial ID: {material.id}")
            print(f"Name: {material.name}")
            print(f"Version: {material.version}")
            print(f"Usage: {material.usage}")
            print(f"Content Type: {material.content_type}")
            print(f"Content: {material.content[:100]}...")  # Show first 100 characters
            print(f"Status: {material.default_status}")
            print(f"Project ID: {material.project_id}")
            print(f"Owner ID: {material.owner_id}")
            print(f"Created: {material.created_at}")
            print(f"Updated: {material.updated_at}")


if __name__ == "__main__":
    view_database_contents()

# How to view database:
# cd backend
# python -m aiconsole.core.database.view_database
