import psycopg2

try:
    conn = psycopg2.connect(dbname="aiconsole", user="postgres", password="123321", host="localhost", port="5432")
    print("Successfully connected to the database!")
    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")

# how to test database
# cd backend
# python -m aiconsole.core.database.test_db
