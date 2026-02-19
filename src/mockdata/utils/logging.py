"""Logging utilities."""

import logging
import os


def init_logging():
    """Initialize logging configuration based on environment variables."""
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    level = os.getenv("LOG_LEVEL", "INFO")
    if level not in levels:
        level = "INFO"

    log_level = getattr(logging, level)
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    _logger = logging.getLogger(__name__)
    _logger.info("Using log level: %s", level)


def get_logger(name: str = __name__) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: The name of the logger. Defaults to the current module name.

    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)
