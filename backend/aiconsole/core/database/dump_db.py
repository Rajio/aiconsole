import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Format: postgresql://user:password@host:port/dbname
db_parts = DATABASE_URL.replace("postgresql://", "").split("/")
db_auth = db_parts[0].split("@")
db_user, db_pass = db_auth[0].split(":")
db_host, db_port = db_auth[1].split(":")
db_name = db_parts[1]


dumps_dir = Path("dumps")
dumps_dir.mkdir(exist_ok=True)

# Create dump file path
dump_file = dumps_dir / "init.sql"

# Create dump command
dump_cmd = [
    "pg_dump",
    "-h",
    db_host,
    "-p",
    db_port,
    "-U",
    db_user,
    "-d",
    db_name,
    "--clean", 
    "--if-exists",
    "-f",
    str(dump_file),
]

os.environ["PGPASSWORD"] = db_pass

try:
    # Run pg_dump
    subprocess.run(dump_cmd, check=True)
    print(f"Database dump created successfully at {dump_file}")
except subprocess.CalledProcessError as e:
    print(f"Error creating database dump: {e}")
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    raise


# how to dump database
# python -m aiconsole.core.database.dump_db
