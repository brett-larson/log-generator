# Imports
from abc import ABC, abstractmethod
import logging
import os
from logging.handlers import RotatingFileHandler
import sys


class BaseGenerator(ABC):
    def __init__(self, formatter, log_dir='/var/log/newrelic'):
        self.formatter = formatter
        self.log_dir = log_dir
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(f'LogGenerator.{self.__class__.__name__}')
        logger.setLevel(logging.INFO)
        logger.handlers = []  # Clear existing handlers

        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # File handler with rotation
        log_file = os.path.join(self.log_dir, f'{self.get_log_type()}.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(self.formatter)
        logger.addHandler(file_handler)

        # Console handler for debugging
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