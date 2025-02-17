# src/generators/base.py
from abc import ABC, abstractmethod
import logging
import os
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path


class BaseGenerator(ABC):
    def __init__(self, formatter, log_dir=None):
        """
        Initialize the generator with a formatter and log directory.

        Args:
            formatter: The formatter to use for log output
            log_dir: Directory for log files. If None, will use:
                    - In container: /var/log/newrelic
                    - Local dev: ./logs in current directory
        """
        self.formatter = formatter
        self.log_dir = self._determine_log_dir(log_dir)
        self.logger = self._setup_logger()

    def _determine_log_dir(self, log_dir):
        """
        Determine the appropriate log directory based on environment.

        Priority:
        1. Explicitly provided log_dir
        2. Environment variable LOG_DIR
        3. Default locations based on environment
        """
        if log_dir:
            return log_dir

        # Check for environment variable
        env_log_dir = os.getenv('LOG_DIR')
        if env_log_dir:
            return env_log_dir

        # Check if we're in a container
        if os.path.exists('/.dockerenv'):
            container_dir = '/var/log/newrelic'
            # Verify we have write permissions
            if os.access(os.path.dirname(container_dir), os.W_OK):
                return container_dir

        # Default to local development directory
        local_dir = os.path.join(os.getcwd(), 'logs')
        return local_dir

    def _setup_logger(self):
        """
        Set up the logger with appropriate handlers and permissions.
        """
        logger = logging.getLogger(f'LogGenerator.{self.__class__.__name__}')
        logger.setLevel(logging.INFO)
        logger.handlers = []  # Clear existing handlers

        try:
            # Ensure log directory exists with appropriate permissions
            Path(self.log_dir).mkdir(parents=True, exist_ok=True)

            # File handler with rotation
            log_file = os.path.join(self.log_dir, f'{self.get_log_type()}.log')
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(self.formatter)
            logger.addHandler(file_handler)

        except PermissionError as e:
            print(f"Warning: Could not create/access log directory {self.log_dir}")
            print(f"Error: {e}")
            print("Falling back to console-only logging")
        except Exception as e:
            print(f"Unexpected error setting up file logging: {e}")
            print("Falling back to console-only logging")

        # Always add console handler for debugging
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        logger.addHandler(console_handler)

        return logger

    @abstractmethod
    def generate_log(self):
        """Generate a single log entry"""
        pass

    @abstractmethod
    def get_log_type(self) -> str:
        """Return the type of log this generator produces"""
        pass

    def get_log_path(self):
        """
        Get the full path to the current log file.

        Returns:
            str: Full path to the log file
        """
        return os.path.join(self.log_dir, f'{self.get_log_type()}.log')
