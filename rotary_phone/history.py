"""Call history tracking for rotary phone."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from rotary_phone.config import ensure_config_dir


def get_history_file() -> Path:
    """Get the path to the history file."""
    config_dir = ensure_config_dir()
    return config_dir / "history.json"


def load_history() -> List[Dict[str, str]]:
    """Load call history from the history file.
    
    Returns:
        List of call history entries, each with 'number', 'formatted', and 'timestamp'.
    """
    history_file = get_history_file()
    if not history_file.exists():
        return []
    
    try:
        with open(history_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history: List[Dict[str, str]]) -> None:
    """Save call history to the history file.
    
    Args:
        history: List of call history entries.
    """
    history_file = get_history_file()
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)


def add_to_history(number: str, formatted: str) -> None:
    """Add a dialed number to history.
    
    Args:
        number: The dialed number.
        formatted: Formatted version of the number.
    """
    history = load_history()
    entry = {
        'number': number,
        'formatted': formatted,
        'timestamp': datetime.now().isoformat()
    }
    history.append(entry)
    # Keep only last 100 entries
    history = history[-100:]
    save_history(history)


def get_history(limit: int = 10) -> List[Dict[str, str]]:
    """Get recent call history.
    
    Args:
        limit: Maximum number of entries to return.
    
    Returns:
        List of recent call history entries.
    """
    history = load_history()
    return history[-limit:]


def clear_history() -> None:
    """Clear all call history."""
    save_history([])




