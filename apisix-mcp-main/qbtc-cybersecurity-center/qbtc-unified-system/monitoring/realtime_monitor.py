# QBTC Real-time Monitoring System
import asyncio
import time
import json
import requests
from datetime import datetime
from pathlib import Path
import logging


class QBTCMonitor:
    """Real-time monitoring system for QBTC"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.quantum_url = "http://localhost:8001"
        self.ollama_url = "http://localhost:11434"
        self.monitoring_interval = 30  # seconds
        self.alert_thresholds = {
            'response_time': 5.0,  # seconds
            'memory_usage': 4096,  # MB
            'cpu_usage': 90,       # percentage
            'disk_usage': 90       # percentage
        }
        self.setup_logging()
    
    def setup_logging(self):
        """Setup monitoring logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def monitor_health_endpoints(self):
        """Monitor system health endpoints"""
        endpoints = {
            'api_gateway': f"{self.base_url}/health",
            'quantum_core': f"{self.quantum_url}/health", 
            'ollama_service': f"{self.ollama_url}/api/version"
        }
        
        health_status = {}
        
        for service, endpoint in endpoints.items():
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=10)
                response_time = time.time() - start_time
                
                health_status[service] = {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Check response time threshold
                if response_time > self.alert_thresholds['response_time']:
                    self.logger.warning(f"{service} response time: {response_time:.2f}s")
                
            except Exception as e:
                health_status[service] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                self.logger.error(f"{service} health check failed: {e}")
        
        return health_status
    
    async def run_monitoring_cycle(self):
        """Run a complete monitoring cycle"""
        self.logger.info("Starting monitoring cycle...")
        
        # Collect all monitoring data
        health_data = await self.monitor_health_endpoints()
        
        # Compile monitoring report
        monitoring_report = {
            'timestamp': datetime.now().isoformat(),
            'health_status': health_data,
            'overall_status': self._calculate_overall_status(health_data)
        }
        
        # Save monitoring data
        self._save_monitoring_data(monitoring_report)
        
        return monitoring_report
    
    def _calculate_overall_status(self, health):
        """Calculate overall system status"""
        # Health status score
        healthy_services = sum(1 for service in health.values() if service.get('status') == 'healthy')
        health_score = healthy_services / len(health) if health else 0
        
        if health_score >= 0.9:
            return 'excellent'
        elif health_score >= 0.7:
            return 'good'
        elif health_score >= 0.5:
            return 'warning'
        else:
            return 'critical'
    
    def _save_monitoring_data(self, data):
        """Save monitoring data to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"logs/monitoring_{timestamp}.json"
        
        Path("logs").mkdir(exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def start_continuous_monitoring(self):
        """Start continuous monitoring loop"""
        self.logger.info(f"Starting continuous monitoring (interval: {self.monitoring_interval}s)")
        
        while True:
            try:
                await self.run_monitoring_cycle()
                self.logger.info(f"Monitoring cycle completed. Waiting {self.monitoring_interval}s...")
                await asyncio.sleep(self.monitoring_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Monitoring cycle failed: {e}")
                await asyncio.sleep(5)  # Short wait before retry


async def run_monitoring():
    """Run QBTC monitoring system"""
    monitor = QBTCMonitor()
    
    print("QBTC Real-time Monitoring System")
    print("=" * 50)
    print("Press Ctrl+C to stop monitoring")
    
    # Start monitoring
    await monitor.start_continuous_monitoring()


if __name__ == "__main__":
    asyncio.run(run_monitoring())
