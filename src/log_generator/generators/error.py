# src/generators/error.py
from datetime import datetime
import random
import uuid
import traceback
from .base_generator import BaseGenerator

class ErrorGenerator(BaseGenerator):
    def get_log_type(self) -> str:
        return "error"

    def generate_log(self):
        # Define common error scenarios
        error_types = [
            {
                'name': 'DatabaseConnectionError',
                'message': 'Failed to connect to database',
                'module': 'database.connection',
                'severity': 'CRITICAL',
                'details': {
                    'host': 'db-master-01',
                    'port': 5432,
                    'timeout': 30
                }
            },
            {
                'name': 'ValidationError',
                'message': 'Invalid input parameters',
                'module': 'api.validators',
                'severity': 'WARNING',
                'details': {
                    'field': random.choice(['email', 'phone', 'address', 'user_id']),
                    'reason': 'Invalid format'
                }
            },
            {
                'name': 'AuthenticationError',
                'message': 'Failed to authenticate user',
                'module': 'auth.service',
                'severity': 'ERROR',
                'details': {
                    'mechanism': 'JWT',
                    'reason': 'Token expired'
                }
            },
            {
                'name': 'RateLimitExceeded',
                'message': 'API rate limit exceeded',
                'module': 'api.middleware',
                'severity': 'WARNING',
                'details': {
                    'limit': 100,
                    'period': '1m'
                }
            },
            {
                'name': 'InternalServerError',
                'message': 'Unexpected server error',
                'module': 'api.handlers',
                'severity': 'CRITICAL',
                'details': {
                    'server': f'app-{random.randint(1,5)}',
                    'process_id': random.randint(1000, 9999)
                }
            }
        ]

        # Select random error
        error = random.choice(error_types)

        # Generate stack trace
        stack_frames = [
            f'  File "/{error["module"]}.py", line {random.randint(1,500)}, in handle_request',
            f'    return process_request(input)',
            f'  File "/{error["module"]}.py", line {random.randint(1,500)}, in process_request',
            f'    validate_input(input)',
            f'  File "/{error["module"]}.py", line {random.randint(1,500)}, in validate_input',
            f'    raise {error["name"]}({error["message"]})'
        ]

        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'web-api',
            'level': error['severity'],
            'error_id': str(uuid.uuid4()),
            'error': {
                'type': error['name'],
                'message': error['message'],
                'module': error['module'],
                'details': error['details']
            },
            'stack_trace': '\n'.join(stack_frames),
            'context': {
                'environment': random.choice(['production', 'staging']),
                'version': f'1.{random.randint(0,9)}.{random.randint(0,9)}',
                'server': f'app-server-{random.randint(1,5)}'
            }
        }

        self.logger.info(self.formatter.format(log_entry))
