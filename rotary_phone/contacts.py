"""Contact management for rotary phone."""

import json
from pathlib import Path
from typing import Dict, Optional

from rotary_phone.config import ensure_config_dir


def get_contacts_file() -> Path:
    """Get the path to the contacts file."""
    config_dir = ensure_config_dir()
    return config_dir / "contacts.json"


def load_contacts() -> Dict[str, str]:
    """Load contacts from the contacts file.
    
    Returns:
        Dictionary mapping contact names to phone numbers.
    """
    contacts_file = get_contacts_file()
    if not contacts_file.exists():
        return {}
    
    try:
        with open(contacts_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_contacts(contacts: Dict[str, str]) -> None:
    """Save contacts to the contacts file.
    
    Args:
        contacts: Dictionary mapping contact names to phone numbers.
    """
    contacts_file = get_contacts_file()
    with open(contacts_file, 'w') as f:
        json.dump(contacts, f, indent=2)


def add_contact(name: str, number: str) -> None:
    """Add a contact.
    
    Args:
        name: Contact name.
        number: Phone number.
    """
    contacts = load_contacts()
    contacts[name] = number
    save_contacts(contacts)


def get_contact(name: str) -> Optional[str]:
    """Get a contact's phone number by name.
    
    Args:
        name: Contact name.
    
    Returns:
        Phone number if contact exists, None otherwise.
    """
    contacts = load_contacts()
    return contacts.get(name)


def list_contacts() -> Dict[str, str]:
    """List all contacts.
    
    Returns:
        Dictionary of all contacts.
    """
    return load_contacts()


def delete_contact(name: str) -> bool:
    """Delete a contact.
    
    Args:
        name: Contact name to delete.
    
    Returns:
        True if contact was deleted, False if not found.
    """
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        return True
    return False





