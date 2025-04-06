from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_connection_string, get_async_connection_string
from .models import Base, Material


class DatabaseManager:
    def __init__(self):
        # Sync engine and session
        self.engine = create_engine(get_connection_string())
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Async engine and session
        self.async_engine = create_async_engine(get_async_connection_string())
        self.AsyncSessionLocal = sessionmaker(
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            bind=self.async_engine
        )

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

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.AsyncSessionLocal()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

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
