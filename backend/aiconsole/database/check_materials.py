from sqlalchemy import create_engine, text

from aiconsole.database.config import get_connection_string


def check_materials():
    try:
        # Create engine
        engine = create_engine(get_connection_string())

        # Execute query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, version, location FROM materials"))
            rows = result.fetchall()

            print(f"\n📦 Found {len(rows)} materials:")
            for row in rows:
                print(f"- ID: {row[0]}, Name: {row[1]}, Version: {row[2]}, Location: {row[3]}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    check_materials()
