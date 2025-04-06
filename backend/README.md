# AIConsole Backend

## Database Setup

The AIConsole backend uses PostgreSQL as its database. Here's how to set it up:

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Poetry for dependency management

### Installation

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Create a `.env` file in the backend directory with the following content:

   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=aiconsole
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

3. Initialize the database:
   ```bash
   poetry run alembic upgrade head
   ```

### Database Migrations

To create a new migration:

```bash
poetry run alembic revision --autogenerate -m "description of changes"
```

To apply migrations:

```bash
poetry run alembic upgrade head
```

To rollback migrations:

```bash
poetry run alembic downgrade -1
```

### Testing

To run tests:

```bash
poetry run pytest
```

The tests use a separate test database. Make sure to set up the test database configuration in `pytest.ini`.

### Development

1. Start the development server:

   ```bash
   poetry run dev
   ```

2. The server will be available at `http://localhost:8000`

### Project Structure

- `aiconsole/database/` - Database models and configuration
- `migrations/` - Alembic migration scripts
- `tests/` - Test files

### Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Submit a pull request

### License

Apache License 2.0
