"""Logging module."""

import logging
from gitlab_grabber.logger import JSONFormatter


class Logging:
    """Make logger."""

    def __init__(self, logger_name: str):
        """Init with stdout handler."""
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)
        formatter = JSONFormatter()
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, level: int, message: str, *args) -> None:
        """Log method."""
        self.logger.log(level, message, *args)

    def info(self, message: str, *args) -> None:
        """INFO."""
        self.log(logging.INFO, message, *args)

    def debug(self, message: str, *args) -> None:
        """DEBUG."""
        self.log(logging.DEBUG, message, *args)

    def warning(self, message: str, *args) -> None:
        """WARNING."""
        self.log(logging.WARNING, message, *args)

    def error(self, message: str, *args) -> None:
        """ERROR."""
        self.log(logging.ERROR, message, *args)

    def critical(self, message: str, *args) -> None:
        """CRITICAL."""
        self.log(logging.CRITICAL, message, *args)
