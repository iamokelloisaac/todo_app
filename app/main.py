"""
Application entry point.

Creates the FastAPI app, configures middleware (CORS, logging),
and mounts the API routers.

How to run:
    - PyCharm:  Click the green Play button (runs this file directly).
    - Terminal: uvicorn app.main:app --reload
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_offline import FastAPIOffline

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging


def create_application() -> FastAPI:
    """
    Builds and returns a configured FastAPI application instance.
    """
    # 1. Setup logging first, so we capture everything from the start.
    setup_logging()

    # 2. Create the app instance.
    application = FastAPIOffline(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # 3. Configure CORS (required for frontend access).
    #
    # CORPORATE RULE (FastAPI 0.100.0+):
    #   You CANNOT combine allow_origins=["*"] with allow_credentials=True.
    #   FastAPI will raise a ValueError at startup. This is a security feature.
    #
    #   - If you need credentials (cookies, auth headers):
    #       allow_origins must be an EXPLICIT list (e.g., ["http://localhost:3000"]).
    #   - If you use wildcard ["*"]:
    #       allow_credentials MUST be False.
    #
    #   In dev, we default to a safe wildcard config (no credentials).
    #   In production, BACKEND_CORS_ORIGINS should be an explicit list.
    cors_origins = settings.BACKEND_CORS_ORIGINS
    cors_credentials = True

    # Safety check: if wildcard is used, force credentials off.
    if "*" in cors_origins:
        cors_credentials = False
        # Log a warning so the dev knows this is a dev-only config.
        import logging
        logging.getLogger(__name__).warning(
            "CORS is using wildcard '*'. Credentials have been disabled. "
            "For production, set explicit origins in BACKEND_CORS_ORIGINS."
        )

    application.add_middleware( # type: ignore[arg-type]
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=cors_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        expose_headers=["X-Request-ID"],
        max_age=600,
    )

    # 4. Mount the API v1 router.
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


# The application instance. Uvicorn looks for this variable.
app = create_application()


# ---------------------------------------------------------------------------
# Development entry point.
#
# This block ONLY runs when you execute this file directly
# (e.g., clicking the Play button in PyCharm, or `python app/main.py`).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )