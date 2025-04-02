import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Format: postgresql://user:password@host:port/dbname
db_parts = DATABASE_URL.replace("postgresql://", "").split("/")
db_auth = db_parts[0].split("@")
db_user, db_pass = db_auth[0].split(":")
db_host, db_port = db_auth[1].split(":")
db_name = db_parts[1]

dump_file = Path("dumps/init.sql")

if not dump_file.exists():
    raise FileNotFoundError(f"Database dump file not found at {dump_file}")

restore_cmd = [
    "psql",
    "-h",
    db_host,
    "-p",
    db_port,
    "-U",
    db_user,
    "-d",
    db_name,
    "-f",
    str(dump_file),
]

os.environ["PGPASSWORD"] = db_pass

try:
    subprocess.run(restore_cmd, check=True)
    print("Database restored successfully")
except subprocess.CalledProcessError as e:
    print(f"Error restoring database: {e}")
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    raise

# how to restore database
# python -m aiconsole.core.database.restore_db
