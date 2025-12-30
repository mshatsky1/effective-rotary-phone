"""Utility functions for rotary phone."""

from typing import Optional


def validate_number(number: str) -> bool:
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


def format_number(number: str, international: bool = False) -> str:
    """Format a phone number for display.
    
    Args:
        number: Phone number string to format.
        international: If True, format with international prefix (+1).
    
    Returns:
        Formatted phone number in (XXX) XXX-XXXX format if 10 digits,
        XXX-XXXX format if 7 digits, otherwise returns the cleaned number
        without formatting characters.
    """
    cleaned = number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if len(cleaned) == 10:
        formatted = f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
        if international:
            return f"+1 {formatted}"
        return formatted
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


def extract_country_code(number: str) -> tuple[str, str]:
    """Extract country code from phone number if present.
    
    Args:
        number: Phone number string.
    
    Returns:
        Tuple of (country_code, number_without_code).
        If no country code found, returns ("", normalized_number).
    """
    cleaned = normalize_number(number)
    
    # Check for common country codes
    if cleaned.startswith("1") and len(cleaned) == 11:
        return ("1", cleaned[1:])
    elif cleaned.startswith("+1") and len(cleaned) == 12:
        return ("1", cleaned[2:])
    
    return ("", cleaned)


def is_valid_length(number: str) -> bool:
    """Check if a phone number has a valid length.
    
    Args:
        number: Phone number string to check.
    
    Returns:
        True if the number length is between 7 and 15 digits, False otherwise.
    """
    from rotary_phone.config import get_config_value
    cleaned = normalize_number(number)
    min_length = get_config_value('min_number_length', 7)
    max_length = get_config_value('max_number_length', 15)
    return min_length <= len(cleaned) <= max_length


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


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds.
    
    Returns:
        Formatted duration string (e.g., "2h 30m 15s" or "45s").
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s" if secs > 0 else f"{minutes}m"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        parts = [f"{hours}h"]
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0:
            parts.append(f"{secs}s")
        return " ".join(parts)

