"""
API v1 router aggregator.

This module collects all endpoint routers for version 1 of the API
and exposes them as a single 'api_router'. The main application
mounts this router with the '/api/v1' prefix.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import health, todos

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(todos.router)