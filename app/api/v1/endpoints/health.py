"""
Health check endpoint.

Used by Kubernetes, Docker, and load balancers to verify the service is alive.
"""
from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get(
    "/health",
    tags=["System"],
    summary="Service health check",
    status_code=200,
)
async def health_check() -> Dict[str, str]:
    """
    Returns a 200 OK if the service is running.
    This endpoint should be lightweight and never touch the database.
    """
    return {"status": "healthy"}