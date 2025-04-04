from sqlalchemy import create_engine, text

# Create database engine
DATABASE_URL = "postgresql://postgres:123321@localhost:5432/aiconsole"
engine = create_engine(DATABASE_URL)


def reset_tables():
    """Reset specific tables in the database"""
    with engine.connect() as connection:
        try:
            # Drop and recreate user_profiles table
            connection.execute(text("DROP TABLE IF EXISTS user_profiles CASCADE"))
            connection.commit()
            print("Tables reset successfully!")
        except Exception as e:
            print(f"Error resetting tables: {e}")


if __name__ == "__main__":
    reset_tables()
