"""
Logging configuration for HordeRL engine.

This module provides a standard logging configuration for the HordeRL engine,
with support for both file and console logging, different environments, and
consistent log formatting.
"""

import logging
import logging.config
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
    console_enabled: bool = False,
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
        console_enabled: Whether to enable console logging

    Returns:
        None
    """
    if environment not in ("development", "test", "production"):
        raise ValueError(f"Unknown environment: {environment}")

    # Create log directory if it doesn't exist
    if log_file is not None and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set default levels based on environment if not explicitly provided
    if console_level is None:
        console_level = DEFAULT_CONSOLE_LEVEL[environment]
    if file_level is None:
        file_level = DEFAULT_FILE_LEVEL[environment]

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    for logger in logging.root.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            logger.handlers.clear()
            logger.propagate = True

    # Create formatters
    if environment == "development":
        console_formatter = {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%H:%M:%S",
        }
        file_formatter = {
            "format": (
                "%(asctime)s [%(levelname)s] %(name)s "
                "(%(filename)s:%(lineno)d): %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    else:  # production or test
        console_formatter = {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
        file_formatter = {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }

    log_file_path = None
    handlers: Dict[str, Dict[str, Any]] = {}
    handler_names = []
    if console_enabled:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "level": console_level,
            "formatter": "console",
            "stream": sys.stdout,
        }
        handler_names.append("console")
    if log_file is not None:
        log_file_path = os.path.join(log_dir, log_file)
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": file_level,
            "formatter": "file",
            "filename": log_file_path,
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
        }
        handler_names.append("file")

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": console_formatter,
                "file": file_formatter,
            },
            "handlers": handlers,
            "root": {
                "level": "DEBUG",
                "handlers": handler_names,
            },
        }
    )

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
