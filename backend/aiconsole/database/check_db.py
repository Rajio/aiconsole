"""
Script to check the database connection and table structure.
"""

import sys
from typing import List, Optional, Tuple

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from aiconsole.database import db_manager
from aiconsole.database.models import Material


async def check_connection() -> bool:
    """Check if the database connection is working."""
    try:
        async with db_manager.session() as session:
            await session.execute(text("SELECT 1"))
            await session.execute(text("SELECT version()"))  # Check PostgreSQL version
        print("✅ PostgreSQL connection successful")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def check_table_exists() -> bool:
    """Check if the materials table exists."""
    try:
        async with db_manager.session() as session:
            # Check if table exists
            result = await session.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'materials')"
            ))
            exists = result.scalar()
            
            if exists:
                print("✅ Materials table exists")
                return True
            else:
                print("❌ Materials table does not exist")
                return False
    except SQLAlchemyError as e:
        print(f"❌ Error checking table existence: {e}")
        return False


async def check_table_structure() -> Tuple[bool, List[str]]:
    """Check if the materials table has the correct structure."""
    expected_columns = {
        "id": "integer",
        "name": "character varying",
        "version": "character varying",
        "usage": "text",
        "usage_examples": "text",
        "type": "character varying",
        "location": "character varying",
        "default_status": "character varying",
        "current_status": "character varying",
        "override": "boolean",
        "content": "text",
        "content_type": "character varying",
        "path": "character varying",
        "created_at": "timestamp without time zone",
        "updated_at": "timestamp without time zone",
        "material_metadata": "jsonb",
        "agents": "jsonb"
    }

    try:
        async with db_manager.session() as session:
            # Get column information from PostgreSQL
            result = await session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'materials'
            """))
            columns = {row[0]: row[1] for row in result}

            # Check for missing columns
            missing_columns = []
            for col_name, col_type in expected_columns.items():
                if col_name not in columns:
                    missing_columns.append(col_name)
                elif columns[col_name] != col_type:
                    missing_columns.append(f"{col_name} (expected {col_type}, got {columns[col_name]})")

            if not missing_columns:
                print("✅ Materials table structure is correct")
                return True, []
            else:
                print("❌ Materials table structure is incorrect")
                print(f"Missing or incorrect columns: {', '.join(missing_columns)}")
                return False, missing_columns

    except SQLAlchemyError as e:
        print(f"❌ Error checking table structure: {e}")
        return False, ["Error checking table structure"]


async def check_database_indexes() -> bool:
    """Check if the necessary indexes exist."""
    try:
        async with db_manager.session() as session:
            # Check for primary key
            result = await session.execute(text("""
                SELECT COUNT(*) 
                FROM pg_constraint 
                WHERE conrelid = 'materials'::regclass 
                AND contype = 'p'
            """))
            has_primary_key = result.scalar() > 0

            # Check for name index
            result = await session.execute(text("""
                SELECT COUNT(*) 
                FROM pg_indexes 
                WHERE tablename = 'materials' 
                AND indexdef LIKE '%materials_name%'
            """))
            has_name_index = result.scalar() > 0

            if has_primary_key and has_name_index:
                print("✅ All required indexes exist")
                return True
            else:
                missing = []
                if not has_primary_key:
                    missing.append("primary key")
                if not has_name_index:
                    missing.append("name index")
                print(f"❌ Missing indexes: {', '.join(missing)}")
                return False

    except SQLAlchemyError as e:
        print(f"❌ Error checking indexes: {e}")
        return False


async def verify_database() -> bool:
    """Run all database verification checks."""
    print("\n🔍 Starting database verification...")
    
    # Check connection
    if not await check_connection():
        return False

    # Check table
    if not await check_table_exists():
        return False

    # Check structure
    structure_ok, _ = await check_table_structure()
    if not structure_ok:
        return False

    # Check indexes
    if not await check_database_indexes():
        return False

    print("\n✅ All database checks passed successfully!")
    return True


if __name__ == "__main__":
    import asyncio
    
    success = asyncio.run(verify_database())
    sys.exit(0 if success else 1)
