#!/usr/bin/env python3
"""
CIO Advanced Performance Benchmark Suite
=========================================
Comprehensive performance testing for the Quantum CIO system with detailed metrics.
"""

import asyncio
import aiohttp
import json
import time
import statistics
import psutil
import platform
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [CIOBenchmark] - %(levelname)s - %(message)s'
)
logger = logging.getLogger("CIOBenchmark")

@dataclass
class TestConfig:
    """Configuration for performance tests"""
    name: str
    url: str
    payload: Dict[str, Any]
    num_requests: int = 100
    concurrency: int = 10
    timeout: int = 30

@dataclass
class RequestResult:
    """Result of a single request"""
    status_code: int
    response_time: float
    success: bool
    error_message: Optional[str] = None
    response_size: int = 0

@dataclass
class TestResult:
    """Results of a complete test"""
    test_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    median_response_time: float
    percentile_95: float
    percentile_99: float
    requests_per_second: float
    total_test_time: float
    cpu_usage_avg: float
    memory_usage_avg: float
    errors: List[str]

class CIOPerformanceBenchmark:
    """Advanced performance benchmark suite for CIO system"""
    
    def __init__(self):
        self.test_configs = [
            TestConfig(
                name="Python API - Simple Code Generation",
                url="http://localhost:8000/api/generate-code",
                payload={
                    "query": "Create a simple hello world function in Python"
                },
                num_requests=50,
                concurrency=5
            ),
            TestConfig(
                name="Python API - Complex Code Generation",
                url="http://localhost:8000/api/generate-code",
                payload={
                    "query": "Create a quantum-enhanced trading algorithm with risk management and portfolio optimization using machine learning in Python"
                },
                num_requests=30,
                concurrency=3
            ),
            TestConfig(
                name="Quantum Core - Simple Query",
                url="http://localhost:8001/quantum/process",
                payload={
                    "query": "Explain quantum entanglement in simple terms"
                },
                num_requests=50,
                concurrency=5
            ),
            TestConfig(
                name="Quantum Core - Trading Query",
                url="http://localhost:8001/quantum/process",
                payload={
                    "query": "Analyze AAPL stock performance and recommend trading strategy"
                },
                num_requests=25,
                concurrency=3
            )
        ]
        
        self.system_monitor = SystemMonitor()
        self.results: List[TestResult] = []
    
    async def run_single_request(self, session: aiohttp.ClientSession, config: TestConfig) -> RequestResult:
        """Execute a single request and measure performance"""
        start_time = time.time()
        
        try:
            async with session.post(
                config.url, 
                json=config.payload,
                timeout=aiohttp.ClientTimeout(total=config.timeout)
            ) as response:
                response_text = await response.text()
                response_time = time.time() - start_time
                
                return RequestResult(
                    status_code=response.status,
                    response_time=response_time,
                    success=response.status == 200,
                    response_size=len(response_text)
                )
                
        except asyncio.TimeoutError:
            return RequestResult(
                status_code=408,
                response_time=time.time() - start_time,
                success=False,
                error_message="Request timeout"
            )
        except Exception as e:
            return RequestResult(
                status_code=0,
                response_time=time.time() - start_time,
                success=False,
                error_message=str(e)
            )
    
    async def run_test_batch(self, config: TestConfig) -> List[RequestResult]:
        """Run a batch of requests with specified concurrency"""
        logger.info(f"Starting test: {config.name}")
        logger.info(f"Requests: {config.num_requests}, Concurrency: {config.concurrency}")
        
        connector = aiohttp.TCPConnector(limit=config.concurrency)
        timeout = aiohttp.ClientTimeout(total=config.timeout)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Create semaphore to limit concurrency
            semaphore = asyncio.Semaphore(config.concurrency)
            
            async def limited_request():
                async with semaphore:
                    return await self.run_single_request(session, config)
            
            # Execute all requests
            tasks = [limited_request() for _ in range(config.num_requests)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and convert to RequestResult
            valid_results = []
            for result in results:
                if isinstance(result, RequestResult):
                    valid_results.append(result)
                else:
                    valid_results.append(RequestResult(
                        status_code=0,
                        response_time=0,
                        success=False,
                        error_message=str(result)
                    ))
            
            return valid_results
    
    def analyze_results(self, config: TestConfig, results: List[RequestResult], test_duration: float) -> TestResult:
        """Analyze test results and calculate metrics"""
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        if successful_results:
            response_times = [r.response_time for r in successful_results]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            median_response_time = statistics.median(response_times)
            percentile_95 = np.percentile(response_times, 95)
            percentile_99 = np.percentile(response_times, 99)
        else:
            avg_response_time = min_response_time = max_response_time = 0
            median_response_time = percentile_95 = percentile_99 = 0
        
        requests_per_second = len(successful_results) / test_duration if test_duration > 0 else 0
        
        # Collect error messages
        errors = [r.error_message for r in failed_results if r.error_message]
        
        # Get system metrics
        cpu_avg, memory_avg = self.system_monitor.get_averages()
        
        return TestResult(
            test_name=config.name,
            total_requests=len(results),
            successful_requests=len(successful_results),
            failed_requests=len(failed_results),
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            median_response_time=median_response_time,
            percentile_95=percentile_95,
            percentile_99=percentile_99,
            requests_per_second=requests_per_second,
            total_test_time=test_duration,
            cpu_usage_avg=cpu_avg,
            memory_usage_avg=memory_avg,
            errors=errors
        )
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all configured tests"""
        logger.info("Starting CIO Performance Benchmark Suite")
        logger.info("=" * 60)
        
        all_results = []
        
        for config in self.test_configs:
            # Start system monitoring
            self.system_monitor.start_monitoring()
            
            # Run the test
            start_time = time.time()
            request_results = await self.run_test_batch(config)
            test_duration = time.time() - start_time
            
            # Stop system monitoring
            self.system_monitor.stop_monitoring()
            
            # Analyze results
            test_result = self.analyze_results(config, request_results, test_duration)
            all_results.append(test_result)
            
            # Log summary
            self.log_test_summary(test_result)
            
            # Wait between tests
            await asyncio.sleep(2)
        
        self.results = all_results
        return all_results
    
    def log_test_summary(self, result: TestResult):
        """Log a summary of test results"""
        logger.info(f"\n--- {result.test_name} ---")
        logger.info(f"Total Requests: {result.total_requests}")
        logger.info(f"Successful: {result.successful_requests}")
        logger.info(f"Failed: {result.failed_requests}")
        logger.info(f"Success Rate: {(result.successful_requests/result.total_requests*100):.1f}%")
        logger.info(f"Avg Response Time: {result.avg_response_time:.3f}s")
        logger.info(f"Min/Max: {result.min_response_time:.3f}s / {result.max_response_time:.3f}s")
        logger.info(f"95th Percentile: {result.percentile_95:.3f}s")
        logger.info(f"Requests/sec: {result.requests_per_second:.2f}")
        logger.info(f"CPU Usage: {result.cpu_usage_avg:.1f}%")
        logger.info(f"Memory Usage: {result.memory_usage_avg:.1f}%")
        
        if result.errors:
            logger.warning(f"Errors: {len(result.errors)} unique error types")
    
    def generate_report(self) -> str:
        """Generate comprehensive performance report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"cio_performance_report_{timestamp}.json"
        
        report_data = {
            "timestamp": timestamp,
            "system_info": {
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total / (1024**3),  # GB
                "platform": platform.platform()
            },
            "test_results": [asdict(result) for result in self.results],
            "summary": self.generate_summary()
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Performance report saved: {report_file}")
        return report_file
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate overall summary statistics"""
        if not self.results:
            return {}
        
        total_requests = sum(r.total_requests for r in self.results)
        total_successful = sum(r.successful_requests for r in self.results)
        avg_response_times = [r.avg_response_time for r in self.results if r.successful_requests > 0]
        
        return {
            "total_tests": len(self.results),
            "total_requests": total_requests,
            "total_successful": total_successful,
            "overall_success_rate": (total_successful / total_requests * 100) if total_requests > 0 else 0,
            "avg_response_time_across_tests": statistics.mean(avg_response_times) if avg_response_times else 0,
            "fastest_test": min(self.results, key=lambda x: x.avg_response_time).test_name if self.results else None,
            "slowest_test": max(self.results, key=lambda x: x.avg_response_time).test_name if self.results else None
        }

class SystemMonitor:
    """Monitor system resources during tests"""
    
    def __init__(self):
        self.cpu_readings = []
        self.memory_readings = []
        self.monitoring = False
        self.monitor_task = None
    
    def start_monitoring(self):
        """Start monitoring system resources"""
        self.monitoring = True
        self.cpu_readings = []
        self.memory_readings = []
        self.monitor_task = asyncio.create_task(self._monitor_loop())
    
    def stop_monitoring(self):
        """Stop monitoring system resources"""
        self.monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
    
    async def _monitor_loop(self):
        """Monitor system resources periodically"""
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_percent = psutil.virtual_memory().percent
                
                self.cpu_readings.append(cpu_percent)
                self.memory_readings.append(memory_percent)
                
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.warning(f"Error monitoring system: {e}")
    
    def get_averages(self) -> tuple:
        """Get average CPU and memory usage"""
        cpu_avg = statistics.mean(self.cpu_readings) if self.cpu_readings else 0
        memory_avg = statistics.mean(self.memory_readings) if self.memory_readings else 0
        return cpu_avg, memory_avg

async def main():
    """Main function to run performance benchmark"""
    benchmark = CIOPerformanceBenchmark()
    
    try:
        # Run all tests
        results = await benchmark.run_all_tests()
        
        # Generate report
        report_file = benchmark.generate_report()
        
        # Print final summary
        logger.info("\n" + "=" * 60)
        logger.info("BENCHMARK COMPLETED")
        logger.info("=" * 60)
        
        summary = benchmark.generate_summary()
        logger.info(f"Total Tests: {summary.get('total_tests', 0)}")
        logger.info(f"Total Requests: {summary.get('total_requests', 0)}")
        logger.info(f"Overall Success Rate: {summary.get('overall_success_rate', 0):.1f}%")
        logger.info(f"Average Response Time: {summary.get('avg_response_time_across_tests', 0):.3f}s")
        logger.info(f"Report saved: {report_file}")
        
    except KeyboardInterrupt:
        logger.info("Benchmark interrupted by user")
    except Exception as e:
        logger.error(f"Benchmark failed: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
