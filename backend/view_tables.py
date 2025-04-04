from sqlalchemy import create_engine, text

# Create database engine
DATABASE_URL = "postgresql://postgres:123321@localhost:5432/aiconsole"
engine = create_engine(DATABASE_URL)

# Tables to check
tables = ["users", "user_profiles", "projects", "materials", "agents", "user_avatars"]

# View contents of each table
with engine.connect() as connection:
    for table in tables:
        print(f"\n=== Contents of {table} table ===")
        try:
            result = connection.execute(text(f"SELECT * FROM {table};"))
            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No data in table")
        except Exception as e:
            print(f"Error accessing table {table}: {e}")
