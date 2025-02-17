# src/formatters/json_formatter.py
import json
from datetime import datetime
import logging
from .base_formatter import BaseFormatter


class JSONFormatter(BaseFormatter):
    """
    Formatter that outputs JSON strings.

    Usage:
        formatter = JSONFormatter(indent=2)
        logger.setFormatter(formatter)
    """

    def __init__(self, indent=None, ensure_ascii=False, **json_kwargs):
        """
        Initialize the formatter with JSON-specific options.

        Args:
            indent: Number of spaces for indentation (None for single line)
            ensure_ascii: If False, allow non-ASCII characters in output
            **json_kwargs: Additional keyword arguments for json.dumps
        """
        super().__init__()
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        self.json_kwargs = json_kwargs

    def format(self, record):
        """
        Format the record as JSON.

        Args:
            record: LogRecord instance or dict

        Returns:
            str: JSON-formatted log entry
        """
        self.validate_record(record)

        if isinstance(record, logging.LogRecord):
            log_entry = self._format_log_record(record)
        else:
            log_entry = self._ensure_minimal_fields(record)

        return json.dumps(
            log_entry,
            indent=self.indent,
            ensure_ascii=self.ensure_ascii,
            default=self._json_default,
            **self.json_kwargs
        )

    def _format_log_record(self, record):
        """
        Convert a LogRecord instance to a dictionary.

        Args:
            record: logging.LogRecord instance

        Returns:
            dict: Record data ready for JSON serialization
        """
        output = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage()
        }

        # Add exception info if present
        if record.exc_info:
            output['exception'] = self.format_exception(record.exc_info)

        # Add stack info if present
        if record.stack_info:
            output['stack_info'] = self.format_stack(record.stack_info)

        # Add any extra attributes
        if hasattr(record, 'extras'):
            output.update(record.extras)

        return output

    def _json_default(self, obj):
        """
        Handle non-JSON-serializable objects.

        Args:
            obj: Object to serialize

        Returns:
            str: String representation of the object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Exception):
            return str(obj)
        return str(obj)