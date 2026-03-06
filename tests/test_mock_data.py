"""Tests for core MockData functionality."""

import json

from bson import ObjectId

from mockdata.core.mock_data import MockData


def load_sample_schema() -> dict:
    """Load a sample JSON schema for testing."""
    with open("schemas/BookStore.json") as f:
        schema_str = f.read()
        return json.loads(schema_str)


def test_mock_data_initialization():
    """Test MockData initialization with a schema."""
    sample_schema = load_sample_schema()
    mock_data = MockData(sample_schema)
    assert mock_data._count == 100


def test_mock_data_generation():
    """Test basic mock data generation."""
    sample_schema = load_sample_schema()
    schema = sample_schema["collections"]["Foo.Author"]
    mock_data = MockData(schema)
    results = mock_data.run()

    for result in results:
        assert "_id" in result
        assert "firstName" in result
        assert "lastName" in result
        assert "email" in result
        assert isinstance(result["_id"], ObjectId)
        assert isinstance(result["firstName"], str)
        assert isinstance(result["lastName"], str)
        assert isinstance(result["email"], str)
