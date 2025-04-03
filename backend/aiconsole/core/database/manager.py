import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from aiconsole.core.database.models import Base


class DatabaseManager:
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL must be provided")

        # Convert database URL to async format
        self.async_database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://")

        # Sync engine and session
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

        # Async engine and session
        self.async_engine = create_async_engine(self.async_database_url)
        self.AsyncSession = sessionmaker(class_=AsyncSession, expire_on_commit=False)
        self.AsyncSession.configure(bind=self.async_engine)

    async def init_db(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def get_session(self):
        return self.Session()

    async def get_async_session(self):
        return self.AsyncSession()

    @property
    def async_session(self):
        return self.AsyncSession()
