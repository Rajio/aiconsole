import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from aiconsole.core.database.models import Base


class DatabaseManager:
    def __init__(self, database_url=None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()
