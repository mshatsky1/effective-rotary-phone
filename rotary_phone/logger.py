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
    from rotary_phone.config import get_config_value
    
    logger = logging.getLogger(name)
    
    # Check if logging is enabled in config
    if not get_config_value('enable_logging', True):
        logger.setLevel(logging.CRITICAL)
        return logger
    
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





