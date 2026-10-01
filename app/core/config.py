"""
Application configuration.

This module loads environment variables and provides a single 'settings'
object that the rest of the application imports. Never hardcode secrets or
environment-specific values in your code. Always use this settings object.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic validates these values at startup. If a required variable is
    missing or invalid, the application will crash immediately (fail-fast).
    This is intentional: it is better to crash at startup than to fail
    silently in production.
    """
    PROJECT_NAME: str = "Todo App"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # CORS: Origins allowed to access this API from a browser.
    # In production, replace "*" with your specific frontend URL.
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Singleton instance. Import this everywhere.
settings = Settings()