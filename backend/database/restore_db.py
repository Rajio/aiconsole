import os
import subprocess
from urllib.parse import urlparse

from dotenv import load_dotenv


def restore_database():
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in .env file")

    parsed = urlparse(database_url)
    db_user = parsed.username
    db_password = parsed.password
    db_host = parsed.hostname
    db_port = str(parsed.port or "5432")
    db_name = parsed.path[1:]

    if not all([db_name, db_user, db_password]):
        raise ValueError("Missing required database connection parameters")

    dump_file = os.path.join(os.path.dirname(__file__), "init.sql")

    if not os.path.exists(dump_file):
        raise FileNotFoundError(f"Dump file not found: {dump_file}")

    cmd = ["psql", "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-f", dump_file]

    if db_password is not None:
        os.environ["PGPASSWORD"] = db_password

    try:
        subprocess.run(cmd, check=True)
        print(f"Database restored successfully from {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error restoring database: {e}")
    finally:
        if "PGPASSWORD" in os.environ:
            del os.environ["PGPASSWORD"]


if __name__ == "__main__":
    restore_database()
