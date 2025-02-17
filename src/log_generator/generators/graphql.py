# src/generators/graphql.py
from datetime import datetime
import random
from .base import BaseGenerator


class GraphQLGenerator(BaseGenerator):
    def get_log_type(self) -> str:
        return "graphql"

    def generate_log(self):
        # Sample GraphQL queries with different complexity
        queries = [
            {
                'operation': 'query',
                'name': 'GetUserProfile',
                'query': '''
                    query GetUserProfile {
                        user(id: "123") {
                            id
                            name
                            email
                            posts {
                                id
                                title
                            }
                        }
                    }
                '''.strip()
            },
            {
                'operation': 'mutation',
                'name': 'CreatePost',
                'query': '''
                    mutation CreatePost($input: PostInput!) {
                        createPost(input: $input) {
                            id
                            title
                            content
                            author {
                                id
                                name
                            }
                        }
                    }
                '''.strip(),
                'variables': {
                    'input': {
                        'title': 'New Post',
                        'content': 'Post content'
                    }
                }
            }
        ]

        # Randomly select a query
        query_template = random.choice(queries)

        # Generate execution metrics
        execution_time = random.uniform(0.05, 2.0)
        status = random.choice(['SUCCESS', 'VALIDATION_ERROR', 'EXECUTION_ERROR'])

        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'graphql-api',
            'operation_type': query_template['operation'],
            'operation_name': query_template['name'],
            'query': query_template['query'],
            'execution_time_ms': round(execution_time * 1000, 2),
            'status': status
        }

        if 'variables' in query_template:
            log_entry['variables'] = query_template['variables']

        if status != 'SUCCESS':
            log_entry['error'] = {
                'message': f'Error during {query_template["operation"]}',
                'code': random.choice(['VALIDATION', 'AUTHORIZATION', 'INTERNAL'])
            }

        self.logger.info(self.formatter.format(log_entry))