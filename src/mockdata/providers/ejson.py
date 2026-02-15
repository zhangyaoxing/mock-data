"""EJSON file output provider."""

from bson import json_util

from mockdata.providers.base import OutputProvider
from mockdata.utils.path import get_project_path


class EJsonProvider(OutputProvider):
    """Provider for writing mock data to EJSON files."""

    def __init__(self, config: dict):
        """Initialize EJSON provider.

        Args:
            config: Configuration with 'folder' key for output directory.
        """
        super().__init__(config)
        self._file = None
        self._logger.debug("Initialized EJsonProvider with config: %s", config)

    def write(self, data: dict) -> None:
        """Write data to EJSON file.

        Args:
            data: Dictionary to write in EJSON format.
        """
        if not self._file:
            folder = self._config.get("folder", "data")
            file_path = get_project_path(folder, f"{self._name}.ejson")

            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            self._file = open(file_path, "w", encoding="utf-8")
            self._logger.debug("Opened EJSON file for writing: %s", file_path)

        # Write data in EJSON format
        ejson_data = json_util.dumps(data)
        self._file.write(ejson_data)
        self._file.write("\n")

    def close(self) -> None:
        """Close the output file."""
        if self._file:
            self._file.close()
            self._logger.debug("Closed EJSON file: %s", self._file.name)
