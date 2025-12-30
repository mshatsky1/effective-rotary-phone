"""Dialer functionality for rotary phone."""

import time

from rotary_phone.exceptions import InvalidDelayError, InvalidNumberError
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
        raise InvalidDelayError("Delay must be non-negative")
    
    if delay > 10.0:
        logger.warning(f"Delay value {delay} is very high, dialing may take a long time")
    
    from rotary_phone.utils import normalize_number
    cleaned = normalize_number(number)
    formatted = format_number(cleaned)
    logger.info(f"Dialing {formatted}...")
    print(f"Dialing {formatted}...")
    
    for i, digit in enumerate(cleaned):
        print(f"  {digit}", end="", flush=True)
        time.sleep(delay)
        # Add visual feedback every 3 digits
        if (i + 1) % 3 == 0 and i + 1 < len(cleaned):
            print(".", end="", flush=True)
    
    print()  # New line after dialing
    
    # Add to history
    add_to_history(cleaned, formatted)
    
    logger.info(f"Connection established to {formatted}")
    print("Connection established!")
    
    # Calculate and log dialing duration
    from rotary_phone.utils import format_duration
    duration = len(cleaned) * delay
    logger.debug(f"Dialing took {format_duration(duration)}")

