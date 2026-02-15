"""Logging utilities."""

import logging
import os

levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
level = os.getenv("LOG_LEVEL", "INFO")
if level not in levels:
    level = "INFO"

log_level = getattr(logging, level)
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

_logger = logging.getLogger(__name__)
_logger.info("Using log level: %s", level)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Name for the logger instance.

    Returns:
        Logger instance configured with project settings.
    """
    return logging.getLogger(name)
