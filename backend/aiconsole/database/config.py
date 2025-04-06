import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "aiconsole")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Database folder path
DB_FOLDER = Path(__file__).parent.parent / "database"
DB_FOLDER.mkdir(exist_ok=True)

# SQLite database path (for testing purposes)
SQLITE_DB_PATH = DB_FOLDER / "materials.db"


# Connection string
def get_connection_string() -> str:
    # PostgreSQL connection string
    encoded_password = quote_plus(DB_PASSWORD)
    return f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?client_encoding=utf8"

    # SQLite connection string (commented out for production)
    # return f"sqlite:///{SQLITE_DB_PATH}"
