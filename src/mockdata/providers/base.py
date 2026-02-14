"""Base output provider interface."""

from abc import ABC, abstractmethod
from mockdata.utils.logging import get_logger


class OutputProvider(ABC):
    """Abstract base class for output providers."""

    def __init__(self, config: dict):
        """Initialize the output provider.

        Args:
            config: Configuration dictionary for the provider.
        """
        self._config = config
        self._logger = get_logger(__name__)
        self._name = None

    @abstractmethod
    def write(self, data: dict) -> None:
        """Write data to the output destination.

        Args:
            data: Dictionary containing the mock data to write.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Close any resources and cleanup."""
        pass

    def set_name(self, name: str) -> None:
        """Set the name for the output (e.g., collection, topic, file).

        Args:
            name: Name to use for the output destination.
        """
        self._name = name
