"""Tests for core MockData functionality."""

import pytest
from mockdata.core.mock_data import MockData


def test_mock_data_initialization(sample_schema):
    """Test MockData initialization with a schema."""
    mock_data = MockData(sample_schema)
    assert mock_data._name == "test_schema"
    assert mock_data._count == 5


def test_mock_data_generation(sample_schema):
    """Test basic mock data generation."""
    mock_data = MockData(sample_schema)
    results = list(mock_data.run())
    
    assert len(results) == 5
    for result in results:
        assert "name" in result
        assert "age" in result
        assert "email" in result
        assert isinstance(result["name"], str)
        assert isinstance(result["age"], int)
        assert 18 <= result["age"] <= 100


def test_resolve_description(sample_schema):
    """Test description parsing."""
    mock_data = MockData(sample_schema)
    
    result = mock_data._resolve_description("#random_int(1, 100)#")
    assert result["gen_method"] == "random_int"
    assert result["params"] == [1, 100]
    
    result = mock_data._resolve_description("#name()#")
    assert result["gen_method"] == "name"
    assert result["params"] == []


def test_bson_type_conversion(sample_schema):
    """Test BSON type conversion."""
    mock_data = MockData(sample_schema)
    
    # Test string conversion
    result = mock_data._convert_value("string", 123, "test_field", {})
    assert result == "123"
    
    # Test int conversion
    result = mock_data._convert_value("int", "42", "test_field", {})
    assert result == 42
    
    # Test bool conversion
    result = mock_data._convert_value("bool", 1, "test_field", {})
    assert result is True
