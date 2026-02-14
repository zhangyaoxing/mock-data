"""Logging utilities."""

import logging
import os

levels = logging._nameToLevel
level = os.getenv("LOG_LEVEL", "INFO")
if level not in levels:
    level = "INFO"

log_level = levels[level]
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

_logger = logging.getLogger(__name__)
_logger.info(f"Using log level: {level}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Name for the logger instance.

    Returns:
        Logger instance configured with project settings.
    """
    return logging.getLogger(name)
