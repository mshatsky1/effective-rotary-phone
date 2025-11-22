"""Dialer functionality for rotary phone."""

import time

from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.logger import setup_logger
from rotary_phone.utils import validate_number, format_number

logger = setup_logger()


def dial(number: str, delay: float = 0.1) -> None:
    """Simulate dialing a phone number."""
    if not validate_number(number):
        logger.error(f"Invalid phone number: {number}")
        raise InvalidNumberError(f"Invalid phone number: {number}")
    
    if delay < 0:
        logger.error("Delay must be non-negative")
        raise ValueError("Delay must be non-negative")
    
    cleaned = number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    logger.info(f"Dialing {format_number(cleaned)}...")
    print(f"Dialing {format_number(cleaned)}...")
    
    for digit in cleaned:
        print(f"  {digit}", end="", flush=True)
        time.sleep(delay)
    
    logger.info("Connection established")
    print("\nConnection established!")

