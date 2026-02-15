"""Path utilities for locating project files."""

from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path object pointing to the project root.
    """
    # Try to find project root by looking for marker files
    current = Path.cwd()

    # Look for common project markers
    markers = ["pyproject.toml", "setup.py", "config.json", "schemas"]

    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent

    # Fallback to current directory
    return current


def get_project_path(*paths: str) -> Path:
    """Get a path relative to the project root.

    Args:
        *paths: Path components to join with project root.

    Returns:
        Path object for the requested location.
    """
    return get_project_root().joinpath(*paths)
