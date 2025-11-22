"""Utility functions for rotary phone."""

import time


def validate_number(number: str) -> bool:
    """Validate a phone number format."""
    if not number:
        return False
    return number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit()


def format_number(number: str) -> str:
    """Format a phone number for display."""
    cleaned = number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if len(cleaned) == 10:
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    return cleaned

