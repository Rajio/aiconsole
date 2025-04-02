import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse

from dotenv import load_dotenv


def dump_database():
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

    dumps_dir = os.path.dirname(__file__)
    os.makedirs(dumps_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_file = os.path.join(dumps_dir, f"dump_{timestamp}.sql")

    cmd = ["pg_dump", "-h", db_host, "-p", db_port, "-U", db_user, "-d", db_name, "-f", dump_file]

    os.environ["PGPASSWORD"] = db_password

    try:
        subprocess.run(cmd, check=True)
        print(f"Database dump created successfully: {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating database dump: {e}")
    finally:
        if "PGPASSWORD" in os.environ:
            del os.environ["PGPASSWORD"]


if __name__ == "__main__":
    dump_database()
