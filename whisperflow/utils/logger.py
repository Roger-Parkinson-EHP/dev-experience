"""Logging configuration for WhisperFlow."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(log_level: str = "DEBUG") -> logging.Logger:
    """Set up logging to both file and console.

    Returns the configured logger.
    """
    # Create log directory
    log_dir = Path.home() / ".whisperflow"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "whisperflow.log"

    # Create logger
    logger = logging.getLogger("whisperflow")
    logger.setLevel(getattr(logging, log_level.upper(), logging.DEBUG))

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # File handler with rotation (max 5MB, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Log startup
    logger.info("=" * 60)
    logger.info(f"WhisperFlow logging initialized at {datetime.now()}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    return logger


def get_logger(name: str = "whisperflow") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


# Initialize default logger
_logger = None


def init_logger() -> logging.Logger:
    """Initialize and return the global logger."""
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger


def log_exception(logger: logging.Logger, msg: str, exc: Exception) -> None:
    """Log an exception with full traceback."""
    import traceback
    logger.error(f"{msg}: {exc}")
    logger.debug(f"Traceback:\n{traceback.format_exc()}")
