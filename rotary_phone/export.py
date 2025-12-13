"""Export and import functionality for rotary phone data."""

import json
from pathlib import Path
from typing import Dict, List

from rotary_phone.contacts import load_contacts, save_contacts
from rotary_phone.history import load_history, save_history


def export_data(output_file: Path, include_history: bool = True) -> None:
    """Export contacts and optionally history to a JSON file.
    
    Args:
        output_file: Path to the output JSON file.
        include_history: Whether to include call history in export.
    """
    data = {
        'contacts': load_contacts(),
    }
    
    if include_history:
        data['history'] = load_history()
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)


def import_data(input_file: Path, merge: bool = True) -> Dict[str, int]:
    """Import contacts and history from a JSON file.
    
    Args:
        input_file: Path to the input JSON file.
        merge: If True, merge with existing data. If False, replace.
    
    Returns:
        Dictionary with import statistics:
        - contacts_added: Number of contacts added
        - contacts_skipped: Number of contacts skipped (if merge and already exists)
        - history_entries_added: Number of history entries added
    """
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    stats = {
        'contacts_added': 0,
        'contacts_skipped': 0,
        'history_entries_added': 0
    }
    
    # Import contacts
    if 'contacts' in data:
        existing_contacts = load_contacts() if merge else {}
        new_contacts = data['contacts']
        
        for name, number in new_contacts.items():
            if merge and name in existing_contacts:
                stats['contacts_skipped'] += 1
            else:
                existing_contacts[name] = number
                stats['contacts_added'] += 1
        
        save_contacts(existing_contacts)
    
    # Import history
    if 'history' in data:
        existing_history = load_history() if merge else []
        new_history = data['history']
        
        # Merge histories and keep unique entries
        if merge:
            existing_numbers = {entry['number'] + entry['timestamp'] for entry in existing_history}
            for entry in new_history:
                key = entry['number'] + entry.get('timestamp', '')
                if key not in existing_numbers:
                    existing_history.append(entry)
                    stats['history_entries_added'] += 1
                    existing_numbers.add(key)
        else:
            existing_history = new_history
            stats['history_entries_added'] = len(new_history)
        
        save_history(existing_history)
    
    return stats





