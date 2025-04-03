from sqlalchemy import create_engine, text

# Create database engine
DATABASE_URL = "postgresql://postgres:123321@localhost:5432/aiconsole"
engine = create_engine(DATABASE_URL)

# Test connection and create a table
with engine.connect() as connection:
    try:
        # Try to create a test table
        connection.execute(text("CREATE TABLE test_table (id serial PRIMARY KEY, name varchar);"))
        connection.commit()
        print("Successfully created test table!")

        # Try to insert some data
        connection.execute(text("INSERT INTO test_table (name) VALUES ('test');"))
        connection.commit()
        print("Successfully inserted data!")

        # Query the data
        result = connection.execute(text("SELECT * FROM test_table;"))
        print("Query result:", result.fetchall())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        connection.execute(text("DROP TABLE IF EXISTS test_table;"))
        connection.commit()
        print("Cleanup complete")
