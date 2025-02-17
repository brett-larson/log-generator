# src/generators/application.py
from datetime import datetime
import random
import uuid
from .base_generator import BaseGenerator

class ApplicationGenerator(BaseGenerator):
    def get_log_type(self) -> str:
        return "application"

    def generate_log(self):
        # Common application endpoints
        endpoints = [
            '/api/users',
            '/api/products',
            '/api/orders',
            '/api/cart',
            '/api/auth/login',
            '/api/auth/logout',
            '/healthcheck'
        ]

        # HTTP methods with weighted distribution
        methods = ['GET'] * 6 + ['POST'] * 3 + ['PUT'] * 2 + ['DELETE']

        # Status codes with realistic distribution
        status_codes = [200] * 85 + [201] * 5 + [400] * 3 + [401] * 2 + \
                      [403] * 2 + [404] * 2 + [500]

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36'
        ]

        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'web-api',
            'level': 'INFO',
            'trace_id': str(uuid.uuid4()),
            'request': {
                'method': random.choice(methods),
                'path': random.choice(endpoints),
                'remote_addr': f'192.168.{random.randint(1,255)}.{random.randint(1,255)}',
                'user_agent': random.choice(user_agents)
            },
            'response': {
                'status_code': random.choice(status_codes),
                'response_time_ms': round(random.uniform(10, 500), 2)
            }
        }

        # Add error details for non-200 status codes
        if log_entry['response']['status_code'] >= 400:
            error_messages = {
                400: 'Bad Request - Invalid parameters',
                401: 'Unauthorized - Missing or invalid authentication',
                403: 'Forbidden - Insufficient permissions',
                404: 'Not Found - Resource does not exist',
                500: 'Internal Server Error - An unexpected error occurred'
            }
            log_entry['level'] = 'ERROR'
            log_entry['error'] = {
                'code': str(log_entry['response']['status_code']),
                'message': error_messages.get(
                    log_entry['response']['status_code'],
                    'Unknown error'
                )
            }

        # Add response size for GET requests
        if log_entry['request']['method'] == 'GET':
            log_entry['response']['size_bytes'] = random.randint(100, 10000)

        # Add request body size for POST/PUT requests
        if log_entry['request']['method'] in ['POST', 'PUT']:
            log_entry['request']['body_size_bytes'] = random.randint(50, 1000)

        self.logger.info(self.formatter.format(log_entry))
