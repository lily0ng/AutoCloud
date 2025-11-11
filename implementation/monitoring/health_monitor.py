"""
Health monitoring service
"""
import requests
import psutil
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HealthMonitor:
    """Monitor service health and dependencies"""
    
    def __init__(self, config: dict):
        self.config = config
        self.dependencies = config.get('dependencies', [])
        self.thresholds = config.get('thresholds', {})
    
    def check_system_health(self) -> dict:
        """Check system health"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status = {
            'healthy': True,
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'cpu': {
                    'status': 'healthy' if cpu_percent < self.thresholds.get('cpu', 80) else 'unhealthy',
                    'value': cpu_percent,
                    'threshold': self.thresholds.get('cpu', 80)
                },
                'memory': {
                    'status': 'healthy' if memory.percent < self.thresholds.get('memory', 85) else 'unhealthy',
                    'value': memory.percent,
                    'threshold': self.thresholds.get('memory', 85)
                },
                'disk': {
                    'status': 'healthy' if disk.percent < self.thresholds.get('disk', 90) else 'unhealthy',
                    'value': disk.percent,
                    'threshold': self.thresholds.get('disk', 90)
                }
            }
        }
        
        # Check if any component is unhealthy
        for check in health_status['checks'].values():
            if check['status'] == 'unhealthy':
                health_status['healthy'] = False
                break
        
        return health_status
    
    def check_dependencies(self) -> dict:
        """Check external dependencies"""
        results = {}
        
        for dep in self.dependencies:
            name = dep.get('name')
            url = dep.get('url')
            timeout = dep.get('timeout', 5)
            
            try:
                response = requests.get(url, timeout=timeout)
                results[name] = {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'response_time': response.elapsed.total_seconds(),
                    'status_code': response.status_code
                }
            except Exception as e:
                results[name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                logger.error(f"Dependency check failed for {name}: {str(e)}")
        
        return results
    
    def get_full_health_report(self) -> dict:
        """Get comprehensive health report"""
        return {
            'system': self.check_system_health(),
            'dependencies': self.check_dependencies(),
            'timestamp': datetime.utcnow().isoformat()
        }
