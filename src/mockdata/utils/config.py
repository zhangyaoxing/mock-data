"""Configuration loading utilities."""

import json
from pathlib import Path
from typing import Optional

from mockdata.utils.path import get_project_path


_config: Optional[dict] = None


def load_config(config_path: Optional[Path] = None) -> dict:
    """Load configuration from JSON file.

    Args:
        config_path: Optional path to config file. Defaults to config/config.json
                    or config.json in project root.

    Returns:
        Dictionary containing configuration.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        json.JSONDecodeError: If config file is invalid JSON.
    """
    global _config

    if _config is not None:
        return _config

    if config_path is None:
        # Try config/config.json first, then config.json
        config_path = get_project_path("config", "config.json")
        if not config_path.exists():
            config_path = get_project_path("config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        _config = json.load(f)

    return _config


def clear_config() -> None:
    """Clear the cached configuration."""
    global _config
    _config = None
