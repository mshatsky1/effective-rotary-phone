"""Logging configuration for rotary phone."""

import logging
import sys


def setup_logger(name: str = "rotary_phone", level: int = logging.INFO) -> logging.Logger:
    """Set up and configure the logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger

