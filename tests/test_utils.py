"""Tests for utility functions."""

import pytest
from pathlib import Path
from mockdata.utils.colors import green, red, cyan, bold
from mockdata.utils.path import get_project_root


def test_color_functions():
    """Test color utility functions."""
    text = "test"
    
    # Test that color functions return strings with ANSI codes
    assert green(text) != text
    assert red(text) != text
    assert cyan(text) != text
    assert bold(text) != text
    
    # Test that colors contain the original text
    assert text in green(text) or "test" in green(text).replace("\x1b", "")


def test_get_project_root():
    """Test project root detection."""
    root = get_project_root()
    assert isinstance(root, Path)
    assert root.exists()
