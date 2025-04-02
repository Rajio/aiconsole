from sqlalchemy import select

from aiconsole.core.database.config import db_manager
from aiconsole.core.database.models import Material, Project


def check_database():
    session = db_manager.get_session()

    # Check
    projects = session.execute(select(Project)).scalars().all()
    print("\nProjects:")
    for project in projects:
        print(f"- {project.id}")

    materials = session.execute(select(Material)).scalars().all()
    print("\nMaterials:")
    for material in materials:
        print(f"- {material.name} (ID: {material.id})")
        print(f"  Project: {material.project_id}")
        print(f"  Content Type: {material.content_type}")
        print(f"  Status: {material.default_status}")
        print()


if __name__ == "__main__":
    check_database()

# how to check database
# cd backend
# python -m aiconsole.core.database.test_db_data
