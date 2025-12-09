"""Tests for utility functions."""

import pytest

from rotary_phone.utils import validate_number, format_number


def test_validate_number_valid():
    """Test validation with valid numbers."""
    assert validate_number("555-1234") is True
    assert validate_number("5551234") is True
    assert validate_number("(555) 123-4567") is True


def test_validate_number_invalid():
    """Test validation with invalid numbers."""
    assert validate_number("") is False
    assert validate_number("abc") is False
    assert validate_number("555-abc") is False


def test_format_number():
    """Test number formatting."""
    assert format_number("5551234567") == "(555) 123-4567"
    assert format_number("555-123-4567") == "(555) 123-4567"




