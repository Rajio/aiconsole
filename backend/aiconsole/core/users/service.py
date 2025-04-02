from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from aiconsole.core.database.manager import DatabaseManager
from aiconsole.core.database.models import User
from aiconsole.core.users.types import UserProfile


class UserService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create_user(self, username: str, email: str, password_hash: str, is_admin: bool = False) -> User:
        with self.db.get_session() as session:
            user = User(
                id=str(uuid4()),
                username=username,
                email=email,
                password_hash=password_hash,
                is_admin=is_admin,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            session.commit()
            return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        with self.db.get_session() as session:
            return session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self.db.get_session() as session:
            return session.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> Optional[User]:
        with self.db.get_session() as session:
            return session.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def update_user_profile(self, user_id: str, profile: UserProfile) -> Optional[User]:
        with self.db.get_session() as session:
            user = self.get_user_by_id(user_id)
            if user:
                user.username = profile.username or user.username
                user.email = profile.email or user.email
                user.avatar_url = profile.avatar_url or user.avatar_url
                user.updated_at = datetime.utcnow()
                session.commit()
            return user

    def update_password(self, user_id: str, new_password_hash: str) -> bool:
        with self.db.get_session() as session:
            user = self.get_user_by_id(user_id)
            if user:
                user.password_hash = new_password_hash
                user.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False

    def deactivate_user(self, user_id: str) -> bool:
        with self.db.get_session() as session:
            user = self.get_user_by_id(user_id)
            if user:
                user.is_active = False
                user.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False

    def activate_user(self, user_id: str) -> bool:
        with self.db.get_session() as session:
            user = self.get_user_by_id(user_id)
            if user:
                user.is_active = True
                user.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False

    def make_admin(self, user_id: str) -> bool:
        with self.db.get_session() as session:
            user = self.get_user_by_id(user_id)
            if user:
                user.is_admin = True
                user.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False

    def remove_admin(self, user_id: str) -> bool:
        with self.db.get_session() as session:
            user = self.get_user_by_id(user_id)
            if user:
                user.is_admin = False
                user.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False
