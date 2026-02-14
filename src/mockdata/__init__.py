"""Mock Data Generator - A tool for generating mock data based on JSON schemas."""

__version__ = "0.2.0"
__author__ = "Mock Data Team"

from mockdata.core.mock_data import MockData
from mockdata.core.constants import BSON_TYPES

__all__ = ["MockData", "BSON_TYPES"]
