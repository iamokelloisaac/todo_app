"""
Todo CRUD endpoints.

This module contains all HTTP routes for the Todo resource.
It delegates data operations to the database layer and uses custom
exceptions for error handling.
"""
from typing import List, Optional

from fastapi import APIRouter, Path, Query, status

from app.core.exceptions import TodoNotFoundException, DuplicateTodoException
from app.models.database import (
    create_todo,
    delete_todo,
    get_todo,
    list_todos,
    update_todo,
)
from app.models.todo import (
    Priority,
    TodoCreate,
    TodoResponse,
    TodoUpdate,
)

router = APIRouter()


@router.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Todos"],
    summary="Create a new todo",
)
async def create_new_todo(payload: TodoCreate) -> TodoResponse:
    """
    Creates a new todo item.

    - **title**: Required, 1-100 characters.
    - **description**: Optional, max 500 characters.
    - **priority**: One of 'low', 'medium', 'high'. Defaults to 'medium'.

    Returns the created todo with a 201 Created status.
    """
    try:
        return create_todo(payload)
    except ValueError:
        raise DuplicateTodoException(title=payload.title)


@router.get(
    "/todos",
    response_model=List[TodoResponse],
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    summary="List all todos",
)
async def get_all_todos(
    completed: Optional[bool] = Query(
        None, description="Filter by completion status."
    ),
    priority: Optional[Priority] = Query(
        None, description="Filter by priority level."
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip."),
    limit: int = Query(10, ge=1, le=100, description="Max records to return."),
) -> List[TodoResponse]:
    """
    Returns a list of todos with optional filtering and pagination.

    Examples:
    - `GET /todos` - Returns the first 10 todos.
    - `GET /todos?completed=true` - Returns only completed todos.
    - `GET /todos?priority=high&limit=5` - Returns the 5 highest priority todos.
    """
    return list_todos(completed=completed, priority=priority, skip=skip, limit=limit)


@router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    summary="Get a single todo by ID",
)
async def get_single_todo(
    todo_id: int = Path(..., ge=1, description="The ID of the todo to retrieve."),
) -> TodoResponse:
    """
    Retrieves a single todo by its ID.

    Returns a 404 Not Found if the todo does not exist.
    """
    todo = get_todo(todo_id)
    if todo is None:
        raise TodoNotFoundException(todo_id=todo_id)
    return todo


@router.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
    summary="Replace a todo entirely",
)
async def replace_todo(
    payload: TodoUpdate,
    todo_id: int = Path(..., ge=1, description="The ID of the todo to update."),
) -> TodoResponse:
    """
    Replaces an entire todo. All fields are required.

    Returns a 404 Not Found if the todo does not exist.
    """
    updated = update_todo(todo_id, payload)
    if updated is None:
        raise TodoNotFoundException(todo_id=todo_id)
    return updated


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Todos"],
    summary="Delete a todo",
)
async def remove_todo(
    todo_id: int = Path(..., ge=1, description="The ID of the todo to delete."),
) -> None:
    """
    Deletes a todo by its ID.

    Returns a 204 No Content on success.
    Returns a 404 Not Found if the todo does not exist.
    """
    deleted = delete_todo(todo_id)
    if not deleted:
        raise TodoNotFoundException(todo_id=todo_id)
    return None