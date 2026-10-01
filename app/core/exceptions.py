"""
Custom exception classes.

Domain-specific exceptions make endpoint code read like English
and centralize the mapping of error codes to HTTP status codes.

Why not just use HTTPException everywhere?
- It keeps endpoint code clean and readable.
- It prevents accidentally sending the wrong status code.
- It makes refactoring (e.g., adding error logging) a one-line change.
"""
from fastapi import HTTPException, status


class TodoNotFoundException(HTTPException):
    """
    Raised when a Todo with a given ID does not exist in the database.

    Maps to HTTP 404 Not Found.

    Usage:
        raise TodoNotFoundException(todo_id=5)
    """
    def __init__(self, todo_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} was not found."
        )


class DuplicateTodoException(HTTPException):
    """
    Raised when attempting to create a Todo that already exists.

    Maps to HTTP 409 Conflict.

    Usage:
        raise DuplicateTodoException(title="Buy milk")
    """
    def __init__(self, title: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A todo with the title '{title}' already exists."
        )