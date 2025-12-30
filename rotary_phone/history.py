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
    
    Raises:
        IOError: If the history file cannot be written.
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
    from rotary_phone.config import get_config_value
    
    # Check if auto_save_history is enabled
    if not get_config_value('auto_save_history', True):
        return
    
    history = load_history()
    entry = {
        'number': number,
        'formatted': formatted,
        'timestamp': datetime.now().isoformat()
    }
    history.append(entry)
    # Keep only last N entries based on config
    history_limit = get_config_value('history_limit', 100)
    history = history[-history_limit:]
    save_history(history)


def get_history(limit: int = 10) -> List[Dict[str, str]]:
    """Get recent call history.
    
    Args:
        limit: Maximum number of entries to return.
    
    Returns:
        List of recent call history entries, sorted by timestamp (newest first).
    """
    history = load_history()
    # Return most recent entries, sorted by timestamp
    sorted_history = sorted(history, key=lambda x: x.get('timestamp', ''), reverse=True)
    return sorted_history[:limit]


def clear_history() -> None:
    """Clear all call history."""
    save_history([])


def get_history_count() -> int:
    """Get the total number of history entries.
    
    Returns:
        Number of entries in call history.
    """
    return len(load_history())


def get_recent_calls(days: int = 7) -> List[Dict[str, str]]:
    """Get recent calls within the specified number of days.
    
    Args:
        days: Number of days to look back.
    
    Returns:
        List of call history entries within the specified period.
    """
    from datetime import datetime, timedelta
    history = load_history()
    cutoff_date = datetime.now() - timedelta(days=days)
    
    recent = []
    for entry in history:
        try:
            timestamp = datetime.fromisoformat(entry.get('timestamp', ''))
            if timestamp >= cutoff_date:
                recent.append(entry)
        except (ValueError, AttributeError):
            continue
    
    return sorted(recent, key=lambda x: x.get('timestamp', ''), reverse=True)





