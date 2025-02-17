# src/generators/metrics.py
from datetime import datetime
import random
import math
from .base_generator import BaseGenerator


class MetricsGenerator(BaseGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.baseline_values = {
            'cpu_usage': 30,
            'memory_usage': 45,
            'disk_usage': 60,
            'network_in': 1000,
            'network_out': 800,
            'response_time': 100
        }

    def get_log_type(self) -> str:
        return "metrics"

    def _generate_metric_value(self, metric_name, baseline):
        """Generate semi-realistic metric values with some variation"""
        self.counter += 1

        # Add some sine wave variation to make it look more realistic
        wave = math.sin(self.counter / 10) * 10

        # Add random noise
        noise = random.uniform(-5, 5)

        # Combine baseline, wave, and noise
        value = baseline + wave + noise

        # Ensure we don't go below 0
        return max(0, round(value, 2))

    def generate_log(self):
        # Define hosts and services
        hosts = [f'host-{i}' for i in range(1, 4)]
        services = ['web-api', 'auth-service', 'database', 'cache']

        # Select random host and service
        host = random.choice(hosts)
        service = random.choice(services)

        # Generate metrics
        metrics = {}
        for metric_name, baseline in self.baseline_values.items():
            metrics[metric_name] = self._generate_metric_value(metric_name, baseline)

        # Add appropriate units
        units = {
            'cpu_usage': '%',
            'memory_usage': '%',
            'disk_usage': '%',
            'network_in': 'Mbps',
            'network_out': 'Mbps',
            'response_time': 'ms'
        }

        # Build the log entry
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'metric',
            'host': host,
            'service': service,
            'metrics': {}
        }

        # Add metrics with their units and thresholds
        for metric_name, value in metrics.items():
            log_entry['metrics'][metric_name] = {
                'value': value,
                'unit': units[metric_name]
            }

            # Add threshold warnings if metrics are high
            thresholds = {
                'cpu_usage': 80,
                'memory_usage': 90,
                'disk_usage': 85,
                'response_time': 200
            }

            if metric_name in thresholds and value > thresholds[metric_name]:
                log_entry['metrics'][metric_name]['threshold_exceeded'] = True
                log_entry['metrics'][metric_name]['threshold'] = thresholds[metric_name]

        # Add some aggregated metrics
        log_entry['summary'] = {
            'health_score': round(100 - (metrics['cpu_usage'] * 0.3 +
                                         metrics['memory_usage'] * 0.3 +
                                         metrics['disk_usage'] * 0.4), 2),
            'total_network_throughput': metrics['network_in'] + metrics['network_out']
        }

        self.logger.info(self.formatter.format(log_entry))
