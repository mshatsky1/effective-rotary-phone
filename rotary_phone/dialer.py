"""Dialer functionality for rotary phone."""

import time

from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.history import add_to_history
from rotary_phone.logger import setup_logger
from rotary_phone.utils import validate_number, format_number

logger = setup_logger()


def dial(number: str, delay: float = 0.1) -> None:
    """Simulate dialing a phone number.
    
    Args:
        number: Phone number to dial. Must be a valid number format.
        delay: Delay in seconds between each digit (default: 0.1).
    
    Raises:
        InvalidNumberError: If the phone number is invalid.
        ValueError: If delay is negative.
    """
    if not validate_number(number):
        logger.error(f"Invalid phone number: {number}")
        raise InvalidNumberError(f"Invalid phone number: {number}")
    
    if delay < 0:
        logger.error("Delay must be non-negative")
        raise ValueError("Delay must be non-negative")
    
    cleaned = number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    formatted = format_number(cleaned)
    logger.info(f"Dialing {formatted}...")
    print(f"Dialing {formatted}...")
    
    for digit in cleaned:
        print(f"  {digit}", end="", flush=True)
        time.sleep(delay)
    
    # Add to history
    add_to_history(cleaned, formatted)
    
    logger.info("Connection established")
    print("\nConnection established!")

