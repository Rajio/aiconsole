from typing import Any, Optional, Type, Union

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class DatabaseError(Exception):
    """Base class for database errors"""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ConnectionError(DatabaseError):
    """Raised when there is an error connecting to the database"""

    pass


class ValidationError(DatabaseError):
    """Raised when there is a validation error"""

    pass


class DuplicateError(DatabaseError):
    """Raised when trying to create a duplicate record"""

    pass


class NotFoundError(DatabaseError):
    """Raised when a record is not found"""

    pass


def handle_db_error(error: Exception, context: str = "") -> None:
    """
    Handle database errors and raise appropriate custom exceptions

    Args:
        error: The original exception
        context: Additional context about where the error occurred

    Raises:
        ConnectionError: If there is a connection issue
        ValidationError: If there is a validation error
        DuplicateError: If there is a duplicate record
        DatabaseError: For other database errors
    """
    if isinstance(error, IntegrityError):
        if "duplicate key" in str(error).lower():
            raise DuplicateError(f"Duplicate record found: {context}", error)
        raise ValidationError(f"Validation error: {context}", error)
    elif isinstance(error, SQLAlchemyError):
        if "connection" in str(error).lower():
            raise ConnectionError(f"Database connection error: {context}", error)
        raise DatabaseError(f"Database error: {context}", error)
    raise error


def safe_commit(session: Session, context: str = "") -> None:
    """
    Safely commit a database session with error handling

    Args:
        session: The database session to commit
        context: Additional context about the operation

    Raises:
        DatabaseError: If there is an error during commit
    """
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        handle_db_error(e, context)


def get_or_404(session: Session, model: Type, id: Union[str, int], context: str = "") -> Any:
    """
    Get a record by ID or raise NotFoundError

    Args:
        session: The database session
        model: The model class to query
        id: The ID of the record to find
        context: Additional context about the operation

    Returns:
        The found record

    Raises:
        NotFoundError: If the record is not found
    """
    try:
        record = session.query(model).get(id)
        if record is None:
            raise NotFoundError(f"{model.__name__} with id {id} not found: {context}")
        return record
    except Exception as e:
        handle_db_error(e, context)
