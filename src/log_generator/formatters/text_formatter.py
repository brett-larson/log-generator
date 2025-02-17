# src/formatters/text_formatter.py
import json
from datetime import datetime
import logging
from .base_formatter import BaseFormatter


class TextFormatter(BaseFormatter):
    """
    Formatter that outputs human-readable text logs.
    Handles both structured data and LogRecord objects.
    """

    def __init__(self):
        super().__init__()

    def format(self, record):
        """
        Format the record as human-readable text.

        Args:
            record: LogRecord instance or dict

        Returns:
            str: Formatted log entry
        """
        self.validate_record(record)

        if isinstance(record, logging.LogRecord):
            return self._format_log_record(record)
        else:
            return self._format_dict_record(record)

    def _format_log_record(self, record):
        """Format a LogRecord instance"""
        timestamp = self.formatTime(record)
        level = record.levelname
        message = record.getMessage()

        # Basic format
        output = f"[{timestamp}] {level}: {message}"

        # Add exception info if present
        if record.exc_info:
            output += f"\nException: {self.format_exception(record.exc_info)}"

        # Add stack info if present
        if record.stack_info:
            output += f"\nStack trace: {self.format_stack(record.stack_info)}"

        return output

    def _format_dict_record(self, record):
        """Format a dictionary record"""
        # Ensure we have minimal fields
        record = self._ensure_minimal_fields(record)

        # Start with timestamp and basic info
        output_parts = []

        # Add timestamp if present
        if 'timestamp' in record:
            output_parts.append(f"[{record['timestamp']}]")

        # Add level if present
        if 'level' in record:
            output_parts.append(record['level'])

        # Handle different log types
        if 'service' in record:
            output_parts.append(f"Service: {record['service']}")

        # Handle HTTP request logs
        if 'request' in record:
            req = record['request']
            output_parts.append(
                f"Request: {req.get('method', 'UNKNOWN')} {req.get('path', '')}"
            )
            if 'response' in record:
                resp = record['response']
                output_parts.append(
                    f"Status: {resp.get('status_code', '?')} "
                    f"Time: {resp.get('response_time_ms', '?')}ms"
                )

        # Handle error logs
        if 'error' in record:
            err = record['error']
            output_parts.append(
                f"Error: {err.get('type', 'Unknown')} - {err.get('message', '')}"
            )
            if 'stack_trace' in record:
                output_parts.append(f"\nStack trace:\n{record['stack_trace']}")

        # Handle metric logs
        if 'metrics' in record:
            metrics = record['metrics']
            output_parts.append(f"Host: {record.get('host', 'unknown')}")

            # Format each metric with its value and unit
            metric_parts = []
            for metric_name, metric_data in metrics.items():
                if isinstance(metric_data, dict):
                    value = metric_data.get('value', '?')
                    unit = metric_data.get('unit', '')
                    metric_str = f"{metric_name}: {value}{unit}"

                    # Add threshold warning if present
                    if metric_data.get('threshold_exceeded'):
                        metric_str += f" (Exceeded threshold: {metric_data['threshold']})"

                    metric_parts.append(metric_str)
                else:
                    # Handle simple metric values
                    metric_parts.append(f"{metric_name}: {metric_data}")

            output_parts.append("Metrics: " + ", ".join(metric_parts))

            # Add summary if present
            if 'summary' in record:
                summary = record['summary']
                summary_parts = [f"{k}: {v}" for k, v in summary.items()]
                output_parts.append("Summary: " + ", ".join(summary_parts))

        # Handle GraphQL logs
        if 'operation_type' in record:
            output_parts.append(
                f"GraphQL {record['operation_type']}: {record.get('operation_name', 'unnamed')}"
            )
            if 'execution_time_ms' in record:
                output_parts.append(f"Execution time: {record['execution_time_ms']}ms")
            if 'status' in record:
                output_parts.append(f"Status: {record['status']}")
            if 'error' in record:
                output_parts.append(f"Error: {record['error'].get('message', 'Unknown error')}")

            # Add query as a separate line
            if 'query' in record:
                output_parts.append(f"\nQuery:\n{record['query']}")

        # Join all parts with appropriate spacing
        base_output = " | ".join(part for part in output_parts if not '\n' in part)

        # Add any multi-line content (like stack traces or queries) at the end
        multi_line_parts = [part for part in output_parts if '\n' in part]
        if multi_line_parts:
            return base_output + '\n' + '\n'.join(multi_line_parts)

        return base_output

    def _format_value(self, value):
        """Helper method to format values consistently"""
        if isinstance(value, (int, float)):
            return f"{value:,}"
        elif isinstance(value, dict):
            return json.dumps(value)
        return str(value)
