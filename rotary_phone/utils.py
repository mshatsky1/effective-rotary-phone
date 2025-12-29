"""Utility functions for rotary phone."""

from typing import Optional
    # Additional imports may be needed for future features
    # Additional imports may be needed for future features
    # Improvement: Enhanced functionality


def validate_number(number: str) -> bool:
    # Improvement: Enhanced functionality
    # Improvement: Enhanced functionality
    """Validate a phone number format.
    
    Args:
        number: Phone number string to validate. Can include formatting
                characters like '-', ' ', '(', ')'.
    
    Returns:
        True if the number contains only digits (after removing formatting)
        and has valid length, False otherwise.
    """
    if not number or not isinstance(number, str):
        return False
    cleaned = normalize_number(number)
    return cleaned.isdigit() and is_valid_length(cleaned)


def format_number(number: str) -> str:
    """Format a phone number for display.
    
    Args:
        number: Phone number string to format.
    
    Returns:
        Formatted phone number in (XXX) XXX-XXXX format if 10 digits,
        XXX-XXXX format if 7 digits, otherwise returns the cleaned number
        without formatting characters.
    """
    cleaned = number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if len(cleaned) == 10:
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    elif len(cleaned) == 7:
        return f"{cleaned[:3]}-{cleaned[3:]}"
    return cleaned


def normalize_number(number: str) -> str:
    """Normalize a phone number by removing all formatting.
    
    Args:
        number: Phone number string to normalize.
    
    Returns:
        Cleaned phone number with only digits.
    """
    return number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")


def is_valid_length(number: str) -> bool:
    """Check if a phone number has a valid length.
    
    Args:
        number: Phone number string to check.
    
    Returns:
        True if the number length is between 7 and 15 digits, False otherwise.
    """
    cleaned = normalize_number(number)
    return 7 <= len(cleaned) <= 15


def format_timestamp(timestamp: str) -> str:
    """Format an ISO timestamp for display.
    
    Args:
        timestamp: ISO format timestamp string.
    
    Returns:
        Formatted timestamp string (YYYY-MM-DD HH:MM:SS).
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        # Fallback to simple string manipulation
        return timestamp[:19].replace('T', ' ')

