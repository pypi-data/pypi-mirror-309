"""Format log module."""

import logging
import json


class JSONFormatter(logging.Formatter):
    """Log formatter."""

    def format(self, record):
        """Fields of logs."""
        log_record = {
            "module": record.name,
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)
