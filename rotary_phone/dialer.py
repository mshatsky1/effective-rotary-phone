"""Dialer functionality for rotary phone."""

import time

from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.utils import validate_number, format_number


def dial(number: str, delay: float = 0.1) -> None:
    """Simulate dialing a phone number."""
    if not validate_number(number):
        raise InvalidNumberError(f"Invalid phone number: {number}")
    
    if delay < 0:
        raise ValueError("Delay must be non-negative")
    
    cleaned = number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    print(f"Dialing {format_number(cleaned)}...")
    
    for digit in cleaned:
        print(f"  {digit}", end="", flush=True)
        time.sleep(delay)
    
    print("\nConnection established!")

