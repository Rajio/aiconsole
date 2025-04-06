from contextlib import contextmanager
from typing import Generator, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_connection_string
from .models import Base, Material


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(get_connection_string())
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_material(self, material_data: dict) -> Material:
        session = self.SessionLocal()
        try:
            material = Material(**material_data)
            session.add(material)
            session.commit()
            session.refresh(material)
            return material
        finally:
            session.close()

    def get_material(self, material_id: int) -> Optional[Material]:
        session = self.SessionLocal()
        try:
            return session.query(Material).filter(Material.id == material_id).first()
        finally:
            session.close()

    def get_material_by_name(self, name: str) -> Optional[Material]:
        session = self.SessionLocal()
        try:
            return session.query(Material).filter(Material.name == name).first()
        finally:
            session.close()

    def get_all_materials(self) -> List[Material]:
        session = self.SessionLocal()
        try:
            materials = session.query(Material).all()
            # Ensure all materials are loaded
            for material in materials:
                session.refresh(material)
            return materials
        finally:
            session.close()

    def update_material(self, material_id: int, material_data: dict) -> Optional[Material]:
        session = self.SessionLocal()
        try:
            material = session.query(Material).filter(Material.id == material_id).first()
            if material:
                for key, value in material_data.items():
                    setattr(material, key, value)
                session.commit()
                session.refresh(material)
            return material
        finally:
            session.close()

    def delete_material(self, material_id: int) -> bool:
        session = self.SessionLocal()
        try:
            material = session.query(Material).filter(Material.id == material_id).first()
            if material:
                session.delete(material)
                session.commit()
                return True
            return False
        finally:
            session.close()


# Create a global instance of the database manager
db_manager = DatabaseManager()
