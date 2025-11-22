"""Configuration handling for rotary phone."""

from pathlib import Path


def get_config_dir() -> Path:
    """Get the configuration directory path.
    
    Returns:
        Path object pointing to ~/.rotary_phone directory.
    """
    return Path.home() / ".rotary_phone"


def ensure_config_dir() -> Path:
    """Ensure configuration directory exists.
    
    Creates the configuration directory if it doesn't exist.
    
    Returns:
        Path object pointing to the configuration directory.
    """
    config_dir = get_config_dir()
    config_dir.mkdir(exist_ok=True)
    return config_dir

