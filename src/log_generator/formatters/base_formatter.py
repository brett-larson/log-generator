# src/formatters/base.py
from abc import ABC, abstractmethod
import logging


class BaseFormatter(ABC, logging.Formatter):
    """
    Base class for all log formatters. Inherits from both ABC for abstract method definition
    and logging.Formatter to maintain compatibility with Python's logging system.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def format(self, record):
        """
        Format the specified record.

        Args:
            record: The log record to format. Can be either:
                   - logging.LogRecord instance (when used with standard logging)
                   - dict (when used directly with log data)

        Returns:
            str: The formatted log entry
        """
        pass

    def format_exception(self, exc_info):
        """
        Format an exception for logging.

        Args:
            exc_info: Exception tuple (type, value, traceback)

        Returns:
            str: Formatted exception information
        """
        if exc_info:
            return super().formatException(exc_info)
        return ""

    def format_stack(self, stack_info):
        """
        Format a stack trace for logging.

        Args:
            stack_info: Stack trace information

        Returns:
            str: Formatted stack trace
        """
        if stack_info:
            return super().formatStack(stack_info)
        return ""

    def formatTime(self, record, datefmt=None):
        """
        Format the record's time field.

        Args:
            record: logging.LogRecord instance
            datefmt: Optional date format string

        Returns:
            str: Formatted time string
        """
        return super().formatTime(record, datefmt)

    def usesTime(self):
        """
        Check if the format uses the creation time of the record.

        Returns:
            bool: True if the format uses time, False otherwise
        """
        return True  # Most log formats will include timestamp

    def validate_record(self, record):
        """
        Validate a record before formatting.

        Args:
            record: The record to validate (LogRecord or dict)

        Returns:
            bool: True if valid, False otherwise

        Raises:
            ValueError: If record is invalid
        """
        if isinstance(record, logging.LogRecord):
            return True
        elif isinstance(record, dict):
            return True
        else:
            raise ValueError(f"Unsupported record type: {type(record)}")

    def _ensure_minimal_fields(self, record):
        """
        Ensure record has minimal required fields.

        Args:
            record: dict or LogRecord to check

        Returns:
            dict: Record with guaranteed minimal fields
        """
        if isinstance(record, dict):
            minimal_fields = {
                'timestamp': None,
                'level': 'INFO',
                'message': ''
            }
            return {**minimal_fields, **record}
        return record