import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent.parent
sys.path.append(str(backend_dir))

# Load environment variables
load_dotenv(backend_dir / ".env")

from sqlalchemy import select

from aiconsole.core.database.manager import DatabaseManager
from aiconsole.core.database.models import User


def add_user(username: str, email: str, password: str, is_admin: bool = False):
    """Add a new user to the database"""
    db = DatabaseManager()

    with db.get_session() as session:
        # Check if user already exists
        existing_user = session.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if existing_user:
            print(f"User {username} already exists!")
            return

        # Create new user
        new_user = User(
            id=username,  # Using username as ID for simplicity
            username=username,
            email=email,
            password_hash=password,  # Note: In production, password should be hashed
            is_admin=is_admin,
            is_active=True,
        )

        session.add(new_user)
        session.commit()
        print(f"User {username} created successfully!")


if __name__ == "__main__":
    # Example usage
    add_user(username="Yura", email="gerraldofrivia@gmail.com", password="pass321", is_admin=True)

# how to add user
# cd backend
# python -m aiconsole.core.database.add_user
