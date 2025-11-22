"""Configuration handling for rotary phone."""

import json
from pathlib import Path
from typing import Dict, Any, Optional


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


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    config_dir = ensure_config_dir()
    return config_dir / "config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from the config file.
    
    Returns:
        Dictionary with configuration settings.
    """
    config_file = get_config_file()
    if not config_file.exists():
        return _get_default_config()
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            default = _get_default_config()
            default.update(config)
            return default
    except (json.JSONDecodeError, IOError):
        return _get_default_config()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to the config file.
    
    Args:
        config: Dictionary with configuration settings.
    """
    config_file = get_config_file()
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value by key.
    
    Args:
        key: Configuration key.
        default: Default value if key not found.
    
    Returns:
        Configuration value or default.
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """Set a configuration value.
    
    Args:
        key: Configuration key.
        value: Value to set.
    """
    config = load_config()
    config[key] = value
    save_config(config)


def _get_default_config() -> Dict[str, Any]:
    """Get default configuration.
    
    Returns:
        Dictionary with default configuration settings.
    """
    return {
        'default_delay': 0.1,
        'history_limit': 100,
        'auto_save_history': True,
    }

