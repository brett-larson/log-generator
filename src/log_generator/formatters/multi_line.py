# src/formatters/multiline_formatter.py
import json
from .base_formatter import BaseFormatter


class MultilineFormatter(BaseFormatter):
    def __init__(self, indent=2):
        self.indent = indent

    def format(self, record):
        """
        Formats the record with special handling for multiline content.
        For GraphQL logs, this ensures the query is properly indented and
        creates a format that Fluent Bit can parse correctly.
        """
        if isinstance(record, dict):
            # Handle query indentation if present
            if 'query' in record:
                record['query'] = self._format_query(record['query'])

            # Format the entire record with proper multiline handling
            formatted = json.dumps(record, indent=self.indent)

            # Add special start/end markers for Fluent Bit multiline parsing
            return f"BEGIN_LOG\n{formatted}\nEND_LOG"
        return str(record)

    def _format_query(self, query):
        """
        Formats a GraphQL query string with consistent indentation.
        Strips empty lines and normalizes whitespace.
        """
        lines = query.split('\n')
        # Remove empty lines and normalize indentation
        lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(lines)