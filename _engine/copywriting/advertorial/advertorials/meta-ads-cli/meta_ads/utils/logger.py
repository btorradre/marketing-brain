"""Logging setup — structured output for API operations."""

import logging
import sys


def setup_logger(level: str = "INFO") -> logging.Logger:
    """Create a logger with consistent formatting for CLI output."""
    logger = logging.getLogger("meta_ads")

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
