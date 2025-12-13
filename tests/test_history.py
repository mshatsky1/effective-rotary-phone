"""Tests for call history."""

import pytest
from pathlib import Path
import json
from datetime import datetime

from rotary_phone.history import (
    add_to_history, clear_history, get_history,
    load_history, save_history
)


@pytest.fixture
def temp_config(tmp_path, monkeypatch):
    """Create a temporary config directory for testing."""
    config_dir = tmp_path / ".rotary_phone"
    config_dir.mkdir()
    
    from rotary_phone import config
    original_get_config_dir = config.get_config_dir
    
    def mock_get_config_dir():
        return config_dir
    
    monkeypatch.setattr(config, "get_config_dir", mock_get_config_dir)
    monkeypatch.setattr(config, "ensure_config_dir", lambda: config_dir)
    
    return config_dir


def test_add_and_get_history(temp_config):
    """Test adding to and retrieving from history."""
    add_to_history("5551234", "(555) 123-4567")
    history = get_history()
    assert len(history) == 1
    assert history[0]["number"] == "5551234"
    assert history[0]["formatted"] == "(555) 123-4567"


def test_history_limit(temp_config):
    """Test history limit."""
    for i in range(15):
        add_to_history(f"555{i:04d}", f"(555) {i:04d}")
    
    history = get_history(limit=10)
    assert len(history) == 10


def test_clear_history(temp_config):
    """Test clearing history."""
    add_to_history("555-1111", "(555) 111-1111")
    clear_history()
    history = get_history()
    assert len(history) == 0


def test_history_max_entries(temp_config):
    """Test that history keeps only last 100 entries."""
    for i in range(110):
        add_to_history(f"555{i:04d}", f"(555) {i:04d}")
    
    history = load_history()
    assert len(history) == 100





