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
        - most_dialed: Most frequently dialed number
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
        List of tuples (number, count) sorted by frequency.
    """
    history = load_history()
    if not history:
        return []
    
    number_counts = Counter(entry['number'] for entry in history)
    return number_counts.most_common(limit)





