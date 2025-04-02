from sqlalchemy import text

from aiconsole.core.database.manager import DatabaseManager


def reset_database():
    db = DatabaseManager()
    with db.engine.connect() as connection:
        # Drop
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        connection.execute(text("GRANT ALL ON SCHEMA public TO public"))
        connection.commit()


if __name__ == "__main__":
    reset_database()

# how to reset database
# cd backend
# python -m aiconsole.core.database.reset_db
