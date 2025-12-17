"""Logging configuration for rotary phone."""

import logging
import sys


def setup_logger(name: str = "rotary_phone", level: int = logging.INFO) -> logging.Logger:
    """Set up and configure the logger.
    
    Args:
        name: Logger name.
        level: Logging level.
    
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Use more detailed format with milliseconds
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger





