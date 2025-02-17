# src/main.py
import argparse
import os
import time

from formatters.json_formatter import JSONFormatter
from formatters.text_formatter import TextFormatter
from formatters.multi_line import MultilineFormatter
from generators.application import ApplicationGenerator
from generators.error import ErrorGenerator
from generators.metrics import MetricsGenerator
from generators.graphql import GraphQLGenerator


def get_formatter(format_type, **kwargs):
    formatters = {
        'json': JSONFormatter,
        'text': TextFormatter,
        'multiline': MultilineFormatter
    }
    return formatters[format_type](**kwargs)


def get_generator(generator_type, formatter, log_dir):
    generators = {
        'application': ApplicationGenerator,
        'error': ErrorGenerator,
        'metrics': MetricsGenerator,
        'graphql': GraphQLGenerator
    }
    return generators[generator_type](formatter, log_dir)


def main():
    parser = argparse.ArgumentParser(description='Generate test logs for New Relic Fluent Bit testing')
    parser.add_argument('--format', choices=['json', 'text', 'multiline'],
                        default='json', help='Log format (default: json)')
    parser.add_argument('--type', choices=['application', 'error', 'metrics', 'graphql'],
                        default='application', help='Type of logs to generate (default: application)')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Interval between logs in seconds (default: 1.0)')
    parser.add_argument('--count', type=int, default=0,
                        help='Number of logs to generate (0 for infinite, default: 0)')
    parser.add_argument('--log-dir',
                        help='Directory to write log files (default: ./logs in dev, /var/log/newrelic in container)')
    args = parser.parse_args()

    # Create formatter and generator
    formatter = get_formatter(args.format)
    generator = get_generator(args.type, formatter, args.log_dir)

    print(f"Generating {args.type} logs in {args.format} format")
    print(f"Log directory: {generator.get_log_path()}")

    count = 0
    try:
        while True:
            generator.generate_log()
            count += 1

            if args.count > 0 and count >= args.count:
                break

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nLog generation stopped by user")


if __name__ == "__main__":
    main()