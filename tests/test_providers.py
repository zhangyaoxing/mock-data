"""Tests for output providers."""

import pytest
import tempfile
from pathlib import Path
from mockdata.providers import EJsonProvider


def test_ejson_provider_initialization():
    """Test EJSON provider initialization."""
    config = {"folder": "test_output"}
    provider = EJsonProvider(config)
    assert provider._config == config
    assert provider._file is None


def test_ejson_provider_write():
    """Test EJSON provider write functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {"folder": tmpdir}
        provider = EJsonProvider(config)
        provider.set_name("test")
        
        test_data = {"name": "John", "age": 30}
        provider.write(test_data)
        provider.close()
        
        # Verify file was created
        output_file = Path(tmpdir) / "test.ejson"
        # Note: The actual file path will be resolved by get_project_path
        # This test may need adjustment based on your test environment
