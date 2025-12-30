"""Statistics and analytics for rotary phone."""

from collections import Counter
from typing import Dict, List

from rotary_phone.history import load_history
from rotary_phone.contacts import load_contacts


def get_dial_stats() -> Dict[str, int]:
    """Get statistics about dialed numbers.
    
    Returns:
        Dictionary with statistics including:
        - total_calls: Total number of calls made
        - unique_numbers: Number of unique numbers dialed
        - most_dialed: Most frequently dialed number (or None)
        - most_dialed_count: Count of most dialed number
        - total_contacts: Number of saved contacts
    """
    history = load_history()
    contacts = load_contacts()
    
    if not history:
        return {
            'total_calls': 0,
            'unique_numbers': 0,
            'most_dialed': None,
            'most_dialed_count': 0,
            'total_contacts': len(contacts)
        }
    
    number_counts = Counter(entry['number'] for entry in history)
    most_common = number_counts.most_common(1)
    
    stats = {
        'total_calls': len(history),
        'unique_numbers': len(number_counts),
        'total_contacts': len(contacts),
    }
    
    if most_common:
        stats['most_dialed'] = most_common[0][0]
        stats['most_dialed_count'] = most_common[0][1]
    else:
        stats['most_dialed'] = None
        stats['most_dialed_count'] = 0
    
    return stats


def get_top_dialed(limit: int = 5) -> List[tuple]:
    """Get the most frequently dialed numbers.
    
    Args:
        limit: Maximum number of results to return.
    
    Returns:
        List of tuples (number, count) sorted by frequency (descending).
    """
    history = load_history()
    if not history:
        return []
    
    number_counts = Counter(entry['number'] for entry in history)
    return number_counts.most_common(limit)


def get_average_calls_per_day() -> float:
    """Calculate average number of calls per day.
    
    Returns:
        Average calls per day, or 0.0 if no history exists.
    """
    history = load_history()
    if not history:
        return 0.0
    
    from datetime import datetime, timedelta
    
    if len(history) < 2:
        return float(len(history))
    
    # Get first and last timestamps
    timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in history]
    first_date = min(timestamps)
    last_date = max(timestamps)
    
    days = (last_date - first_date).days + 1
    return len(history) / days if days > 0 else float(len(history))


def get_calls_by_day() -> Dict[str, int]:
    """Get call count grouped by day.
    
    Returns:
        Dictionary mapping date strings (YYYY-MM-DD) to call counts.
    """
    history = load_history()
    if not history:
        return {}
    
    from collections import Counter
    from datetime import datetime
    
    dates = []
    for entry in history:
        timestamp = entry.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                dates.append(dt.strftime('%Y-%m-%d'))
            except (ValueError, AttributeError):
                continue
    
    return dict(Counter(dates))


def get_calls_by_hour() -> Dict[int, int]:
    """Get call count grouped by hour of day.
    
    Returns:
        Dictionary mapping hour (0-23) to call counts.
    """
    history = load_history()
    if not history:
        return {}
    
    from collections import Counter
    from datetime import datetime
    
    hours = []
    for entry in history:
        timestamp = entry.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                hours.append(dt.hour)
            except (ValueError, AttributeError):
                continue
    
    return dict(Counter(hours))





