"""Custom exceptions for rotary phone."""


class RotaryPhoneError(Exception):
    """Base exception for rotary phone errors."""
    pass


class InvalidNumberError(RotaryPhoneError):
    """Raised when a phone number is invalid."""
    pass


class DialError(RotaryPhoneError):
    """Raised when dialing fails."""
    pass



