# Database Management Scripts

This directory contains scripts for managing PostgreSQL database.

## Directory Structure

- `init.sql` - file with initial database dump
- `dump_db.py` - script for creating database dump
- `restore_db.py` - script for restoring database from dump

## Requirements

- Python 3.8 or higher
- PostgreSQL
- `pg_dump` and `psql` utilities from PostgreSQL package
- `python-dotenv` package for working with environment variables

## Setup

1. Make sure you have PostgreSQL and `pg_dump` and `psql` utilities installed
2. Create a `.env` file in the project root with the following parameter:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```
   Example:
   ```
   DATABASE_URL=postgresql://postgres:123321@localhost:5432/aiconsole
   ```

## Usage

### Creating Database Dump

```bash
python dump_db.py
```

The script will create a dump file with current date and time in the format `dump_YYYYMMDD_HHMMSS.sql`

### Restoring Database

```bash
python restore_db.py
```

The script will restore the database from the `init.sql` file

## Notes

- Before restoring the database, make sure the `init.sql` file exists
- Scripts use connection parameters from the `DATABASE_URL` environment variable
- Scripts will throw an error if required connection parameters are missing
