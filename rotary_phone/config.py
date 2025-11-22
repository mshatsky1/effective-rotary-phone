"""Configuration handling for rotary phone."""

import os
from pathlib import Path


def get_config_dir():
    """Get the configuration directory path."""
    return Path.home() / ".rotary_phone"


def ensure_config_dir():
    """Ensure configuration directory exists."""
    config_dir = get_config_dir()
    config_dir.mkdir(exist_ok=True)
    return config_dir

