"""
Pydantic models for the Todo resource.

These models define the contract between the client and the API.
- TodoCreate: What the client sends when creating a todo.
- TodoUpdate: What the client sends when updating a todo.
- TodoResponse: What the API returns to the client.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class Priority(str, Enum):
    """
    Allowed priority levels for a todo.
    Using an Enum restricts the client to these exact values.
    If the client sends "Urgent", FastAPI rejects it with a 422.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoBase(BaseModel):
    """
    Shared fields between create and update models.
    Do not use this model directly in endpoints.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The title of the todo. Required."
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional detailed description of the todo."
    )
    completed: bool = Field(
        default=False,
        description="Whether the todo has been completed."
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="The priority level of the todo."
    )


class TodoCreate(TodoBase):
    """
    Model for POST /todos requests.
    Inherits all fields from TodoBase.
    'extra="forbid"' rejects any unknown fields (security best practice).
    """
    model_config = ConfigDict(extra="forbid")


class TodoUpdate(TodoBase):
    """
    Model for PUT /todos/{id} requests.
    Requires ALL fields to be present (full replacement).
    """
    model_config = ConfigDict(extra="forbid")


class TodoResponse(TodoBase):
    """
    Model for outgoing responses.
    Adds server-generated fields (id, created_at, updated_at).
    """
    id: int = Field(..., description="Unique identifier for the todo.")
    created_at: datetime = Field(..., description="When the todo was created.")
    updated_at: datetime = Field(..., description="When the todo was last updated.")

    model_config = ConfigDict(from_attributes=True)