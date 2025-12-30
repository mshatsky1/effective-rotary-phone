"""Tests for contact management."""

import pytest
from pathlib import Path
import json
import tempfile
import shutil

from rotary_phone.contacts import (
    add_contact, delete_contact, get_contact,
    list_contacts, load_contacts, save_contacts
)


@pytest.fixture
def temp_config(tmp_path, monkeypatch):
    """Create a temporary config directory for testing."""
    config_dir = tmp_path / ".rotary_phone"
    config_dir.mkdir()
    
    # Monkey patch get_config_dir to return temp directory
    from rotary_phone import config
    original_get_config_dir = config.get_config_dir
    
    def mock_get_config_dir():
        return config_dir
    
    monkeypatch.setattr(config, "get_config_dir", mock_get_config_dir)
    monkeypatch.setattr(config, "ensure_config_dir", lambda: config_dir)
    
    return config_dir


def test_add_and_get_contact(temp_config):
    """Test adding and retrieving a contact."""
    add_contact("John Doe", "555-1234")
    number = get_contact("John Doe")
    assert number == "555-1234"


def test_list_contacts(temp_config):
    """Test listing all contacts."""
    add_contact("John", "555-1111")
    add_contact("Jane", "555-2222")
    contacts = list_contacts()
    assert len(contacts) == 2
    assert contacts["John"] == "555-1111"
    assert contacts["Jane"] == "555-2222"


def test_delete_contact(temp_config):
    """Test deleting a contact."""
    add_contact("John", "555-1111")
    assert delete_contact("John") is True
    assert get_contact("John") is None
    assert delete_contact("Nonexistent") is False


def test_get_nonexistent_contact(temp_config):
    """Test getting a contact that doesn't exist."""
    assert get_contact("Nonexistent") is None







