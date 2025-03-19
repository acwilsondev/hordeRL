"""
Logging configuration for HordeRL engine.

This module provides a standard logging configuration for the HordeRL engine,
with support for both file and console logging, different environments, and
consistent log formatting.
"""

import logging
import logging.handlers
import os
import sys
from typing import Any, Dict, Optional

# Default log levels for different environments
DEFAULT_CONSOLE_LEVEL = {
    "development": logging.DEBUG,
    "test": logging.INFO,
    "production": logging.WARNING,
}

DEFAULT_FILE_LEVEL = {
    "development": logging.DEBUG,
    "test": logging.DEBUG,
    "production": logging.INFO,
}


def configure_logging(
    environment: str = "development",
    log_dir: str = "logs",
    log_file: str = "horderl.log",
    console_level: Optional[int] = None,
    file_level: Optional[int] = None,
    capture_warnings: bool = True,
) -> None:
    """
    Configure the logging system for the application.

    Args:
        environment: The environment ('development', 'test', or 'production')
        log_dir: Directory to store log files
        log_file: Name of the log file
        console_level: Override the default console logging level for the environment
        file_level: Override the default file logging level for the environment
        capture_warnings: Whether to capture warnings via logging

    Returns:
        None
    """
    if environment not in ("development", "test", "production"):
        raise ValueError(f"Unknown environment: {environment}")

    # Create log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set default levels based on environment if not explicitly provided
    if console_level is None:
        console_level = DEFAULT_CONSOLE_LEVEL[environment]
    if file_level is None:
        file_level = DEFAULT_FILE_LEVEL[environment]

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all logs
    root_logger.handlers = []  # Remove any existing handlers

    # Create formatters
    if environment == "development":
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d):"
            " %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:  # production or test
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

    # Console handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (rotating) - only if log_file is provided
    log_file_path = None
    if log_file is not None:
        log_file_path = os.path.join(log_dir, log_file)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Capture warnings from the warnings module
    logging.captureWarnings(capture_warnings)

    # Log the configuration
    logger = logging.getLogger(__name__)
    log_message = (
        f"Logging configured: environment={environment}, "
        f"console_level={logging.getLevelName(console_level)}"
    )

    # Add file logging info only if file logging is enabled
    if log_file is not None:
        log_message += (
            f", file_level={logging.getLevelName(file_level)}, "
            f"log_file={log_file_path}"
        )

    logger.info(log_message)


def get_logger(
    name: str, extra: Optional[Dict[str, Any]] = None
) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: The logger name, typically the module name (__name__)
        extra: Optional dict of extra contextual information to include in logs

    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)

    if extra:
        # Return a logger adapter if extra context is provided
        return logging.LoggerAdapter(logger, extra)

    return logger
