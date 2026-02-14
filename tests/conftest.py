"""Test configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_schema():
    """Sample JSON schema for testing."""
    return {
        "name": "test_schema",
        "count": 5,
        "$jsonSchema": {
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "#name()#"
                },
                "age": {
                    "bsonType": "int",
                    "description": "#random_int(18, 100)#"
                },
                "email": {
                    "bsonType": "string",
                    "description": "#email()#"
                }
            }
        }
    }


@pytest.fixture
def test_config():
    """Sample configuration for testing."""
    return {
        "output": {
            "ejson": {
                "folder": "test_output"
            }
        }
    }
