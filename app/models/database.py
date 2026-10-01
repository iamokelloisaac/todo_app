"""
In-memory database for the Todo App.

This module simulates a database. It will be replaced with SQLAlchemy
in a future chapter. The rest of the application interacts with this
module via the functions below, so the swap will be seamless.
"""
from datetime import datetime, timezone
from typing import Optional

from app.models.todo import TodoCreate, TodoResponse, TodoUpdate, Priority


# The "table". In a real DB, this would be a SQL table.
_TODOS: dict[int, TodoResponse] = {}
_CURRENT_ID: int = 0


def _get_next_id() -> int:
    """Simulates an auto-incrementing primary key."""
    global _CURRENT_ID
    _CURRENT_ID += 1
    return _CURRENT_ID


def _utc_now() -> datetime:
    """Returns the current UTC time. Always use UTC in the backend."""
    return datetime.now(timezone.utc)


def create_todo(payload: TodoCreate) -> TodoResponse:
    """
    Inserts a new todo into the database.

    Args:
        payload: The validated TodoCreate data from the client.

    Returns:
        The full TodoResponse object with generated fields.
    """
    # Check for duplicates (simulating a UNIQUE constraint on title)
    for existing in _TODOS.values():
        if existing.title.lower() == payload.title.lower():
            raise ValueError(f"Todo with title '{payload.title}' already exists.")

    todo_id = _get_next_id()
    now = _utc_now()
    new_todo = TodoResponse(
        id=todo_id,
        **payload.model_dump(),
        created_at=now,
        updated_at=now,
    )
    _TODOS[todo_id] = new_todo
    return new_todo


def get_todo(todo_id: int) -> Optional[TodoResponse]:
    """
    Retrieves a single todo by ID.

    Returns None if the todo does not exist.
    """
    return _TODOS.get(todo_id)


def list_todos(
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    skip: int = 0,
    limit: int = 10,
) -> list[TodoResponse]:
    """
    Lists todos with optional filtering and pagination.

    Args:
        completed: If provided, filter by completion status.
        priority: If provided, filter by priority level.
        skip: Number of records to skip (for pagination).
        limit: Maximum number of records to return.

    Returns:
        A list of TodoResponse objects.
    """
    results = list(_TODOS.values())

    if completed is not None:
        results = [t for t in results if t.completed == completed]
    if priority is not None:
        results = [t for t in results if t.priority == priority]

    return results[skip : skip + limit]


def update_todo(todo_id: int, payload: TodoUpdate) -> Optional[TodoResponse]:
    """
    Replaces an existing todo entirely.

    Returns None if the todo does not exist.
    """
    if todo_id not in _TODOS:
        return None

    original = _TODOS[todo_id]
    updated = TodoResponse(
        id=todo_id,
        **payload.model_dump(),
        created_at=original.created_at,  # Preserve original creation date
        updated_at=_utc_now(),
    )
    _TODOS[todo_id] = updated
    return updated


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo by ID.

    Returns True if deleted, False if the todo did not exist.
    """
    if todo_id not in _TODOS:
        return False
    del _TODOS[todo_id]
    return True