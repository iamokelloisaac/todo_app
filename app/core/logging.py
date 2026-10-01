"""
Structured JSON logging.

Corporate tools (Datadog, Splunk, ELK) require machine-readable logs.
Plain text logs are for hobby projects.

This module configures the root logger to output JSON to stdout.
In a containerized environment (Docker/K8s), stdout is captured
automatically by the orchestrator.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger

from app.core.config import settings


def setup_logging() -> None:
    """
    Configures the root logger to output JSON to stdout.

    Call this function once at application startup (in main.py).
    Calling it twice is safe: it clears existing handlers first
    to avoid duplicate log lines.
    """
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Remove existing handlers to avoid duplicate log lines.
    # This matters when running tests or reloading with uvicorn --reload.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Output to stdout. Never log to a file in a container; let the
    # orchestrator collect stdout and forward it to your log aggregator.
    log_handler = logging.StreamHandler(sys.stdout)

    # Format each log record as a JSON object with standard fields:
    # timestamp, level, logger name, and the message.
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)