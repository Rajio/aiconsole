from functools import lru_cache
from typing import Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Database settings
    DATABASE_URL: str

    # Optional database settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # Application settings
    APP_NAME: str = "AIConsole"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGIN: str = "http://localhost:3000"
    PROJECT_PATH: str = "."

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str]) -> str:
        """Validate and assemble database URL"""
        if isinstance(v, str):
            return v
        return "postgresql://postgres:postgres@localhost:5432/aiconsole"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
