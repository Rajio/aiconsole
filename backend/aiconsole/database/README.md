# Database Integration for Materials

This module provides database integration for managing materials using PostgreSQL.

## Setup

1. Install required dependencies:

   ```bash
   pip install sqlalchemy psycopg2-binary python-dotenv
   ```

2. Create a `.env` file in the project root with the following configuration:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=aiconsole
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

## Basic Operations

### Creating a Material

```python
from aiconsole.database import db_manager

material_data = {
    "name": "example_material",
    "version": "1.0.0",
    "usage": "example",
    "type": "material",
    "location": "local",
    "default_status": "active",
    "current_status": "active",
    "content": "Example content",
    "material_metadata": {"key": "value"}
}

material = db_manager.create_material(material_data)
```

### Retrieving a Material

```python
# Get by ID
material = db_manager.get_material(1)

# Get all materials
materials = db_manager.get_all_materials()
```

### Updating a Material

```python
update_data = {
    "current_status": "inactive"
}
db_manager.update_material(1, update_data)
```

### Deleting a Material

```python
db_manager.delete_material(1)
```

## Database Schema

The `materials` table has the following structure:

| Field             | Type      | Description           |
| ----------------- | --------- | --------------------- |
| id                | Integer   | Primary key           |
| name              | String    | Material name         |
| version           | String    | Material version      |
| usage             | String    | Usage description     |
| type              | String    | Material type         |
| location          | String    | Storage location      |
| default_status    | String    | Default status        |
| current_status    | String    | Current status        |
| content           | Text      | Material content      |
| material_metadata | JSON      | Additional metadata   |
| created_at        | Timestamp | Creation timestamp    |
| updated_at        | Timestamp | Last update timestamp |

## Command-line Tools

### Database Synchronization

```bash
# Run database synchronization
python -m aiconsole.database sync

# Run usage example
python -m aiconsole.database example

# Run custom queries example
python -m aiconsole.database queries
```

## Migration Process

The migration process scans the following directories for material files:

- `backend/aiconsole/materials/`
- `backend/aiconsole/materials/agents/`
- `backend/aiconsole/materials/tools/`
- `backend/aiconsole/materials/workspaces/`

Supported file types:

- JSON (`.json`)
- YAML (`.yaml`, `.yml`)
- TOML (`.toml`)
- Text (`.txt`)
- Markdown (`.md`)

## Custom Queries

The module supports custom SQL queries using SQLAlchemy's `text` function. Here are some examples:

### Get Materials by Type

```python
from sqlalchemy import text
from aiconsole.database import db_manager

with db_manager.get_session() as session:
    result = session.execute(text("SELECT * FROM materials WHERE type = 'material'"))
    materials = result.fetchall()
```

### Get Recent Materials

```python
with db_manager.get_session() as session:
    result = session.execute(
        text("SELECT * FROM materials WHERE created_at > NOW() - INTERVAL '24 hours'")
    )
    recent_materials = result.fetchall()
```

### Count Materials by Location

```python
with db_manager.get_session() as session:
    result = session.execute(
        text("SELECT location, COUNT(*) FROM materials GROUP BY location")
    )
    location_counts = result.fetchall()
```

## Troubleshooting

### Common Issues

1. Database Connection

   - Ensure PostgreSQL is running
   - Verify database credentials in `.env`
   - Check network connectivity

2. Table Structure

   - Run synchronization to create/update tables
   - Check for migration errors

3. Migration Errors
   - Verify file permissions
   - Check file format compatibility
   - Ensure proper JSON/YAML/TOML syntax

## Debugging

To debug database operations:

1. Enable SQLAlchemy logging:

   ```python
   import logging
   logging.basicConfig()
   logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
   ```

2. Use the session context manager:
   ```python
   with db_manager.get_session() as session:
       # Your database operations here
   ```

## Advanced Usage

### Transaction Management

```python
with db_manager.get_session() as session:
    try:
        # Your database operations here
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
```

### Custom Queries

For complex queries, use SQLAlchemy's `text` function:

```python
from sqlalchemy import text

with db_manager.get_session() as session:
    result = session.execute(text("YOUR SQL QUERY HERE"))
    data = result.fetchall()
```
