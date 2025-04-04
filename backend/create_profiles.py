from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from aiconsole.core.database.models import User, UserProfile

# Create database engine
DATABASE_URL = "postgresql://postgres:123321@localhost:5432/aiconsole"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_user_profiles():
    """Create user profiles for existing users"""
    session = SessionLocal()
    try:
        # Get all users
        users = session.execute(select(User)).scalars().all()

        for user in users:
            # Check if profile already exists
            existing_profile = session.query(UserProfile).filter(UserProfile.user_id == user.id).first()
            if not existing_profile:
                # Create profile
                profile = UserProfile(
                    id=user.id,
                    user_id=user.id,
                    username=user.username,
                    email=user.email,
                    avatar_url=user.avatar_url,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(profile)
                print(f"Created profile for user: {user.username}")

        session.commit()
        print("Profile creation completed successfully!")

    except Exception as e:
        print(f"Error creating profiles: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    create_user_profiles()
