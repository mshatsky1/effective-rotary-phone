"""Tests for dialer functionality."""

import pytest

from rotary_phone.dialer import dial
from rotary_phone.utils import validate_number


def test_dial_valid_number():
    """Test dialing a valid number."""
    try:
        dial("555-1234", delay=0.01)
    except Exception as e:
        pytest.fail(f"Dialing valid number should not raise: {e}")


def test_dial_invalid_number():
    """Test dialing an invalid number raises error."""
    with pytest.raises(ValueError):
        dial("invalid")







