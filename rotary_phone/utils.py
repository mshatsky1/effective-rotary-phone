"""Utility functions for rotary phone."""


def validate_number(number: str) -> bool:
    """Validate a phone number format.
    
    Args:
        number: Phone number string to validate. Can include formatting
                characters like '-', ' ', '(', ')'.
    
    Returns:
        True if the number contains only digits (after removing formatting),
        False otherwise.
    """
    if not number:
        return False
    return number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit()


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

