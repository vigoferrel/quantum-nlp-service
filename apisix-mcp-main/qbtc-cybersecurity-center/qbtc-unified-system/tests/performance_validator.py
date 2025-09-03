#!/usr/bin/env python3
"""QBTC Performance Validation and Benchmarking"""

import asyncio
import aiohttp
import time
import statistics
import json
from datetime import datetime
import requests


class QBTCPerformanceValidator:
    """Performance validation for QBTC system"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.quantum_url = "http://localhost:8001"
        self.results = {}
    
    async def test_response_times(self, concurrent_requests=10, total_requests=100):
        """Test API response times under load"""
        print(f"Testing response times with {concurrent_requests} concurrent requests...")
        
        endpoints = [
            f"{self.base_url}/health",
            f"{self.base_url}/api/status",
            f"{self.quantum_url}/health"
        ]
        
        results = {}
        
        for endpoint in endpoints:
            print(f"Testing endpoint: {endpoint}")
            response_times = []
            
            async with aiohttp.ClientSession() as session:
                semaphore = asyncio.Semaphore(concurrent_requests)
                
                async def make_request():
                    async with semaphore:
                        start_time = time.time()
                        try:
                            async with session.get(endpoint, timeout=30) as response:
                                await response.text()
                                return time.time() - start_time
                        except Exception as e:
                            print(f"Request failed: {e}")
                            return None
                
                tasks = [make_request() for _ in range(total_requests)]
                times = await asyncio.gather(*tasks)
                response_times = [t for t in times if t is not None]
            
            if response_times:
                results[endpoint] = {
                    'avg_response_time': statistics.mean(response_times),
                    'min_response_time': min(response_times),
                    'max_response_time': max(response_times),
                    'median_response_time': statistics.median(response_times),
                    'std_deviation': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                    'successful_requests': len(response_times),
                    'total_requests': total_requests,
                    'success_rate': len(response_times) / total_requests
                }
        
        return results
    
    async def run_full_performance_suite(self):
        """Run complete performance validation suite"""
        print("QBTC Performance Validation Suite")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run performance tests
        response_time_results = await self.test_response_times()
        
        total_time = time.time() - start_time
        
        # Compile results
        performance_report = {
            'timestamp': datetime.now().isoformat(),
            'test_duration_seconds': total_time,
            'response_times': response_time_results,
            'performance_score': self._calculate_performance_score(response_time_results)
        }
        
        return performance_report
    
    def _calculate_performance_score(self, response_times):
        """Calculate overall performance score (0-100)"""
        scores = []
        
        # Response time score (lower is better)
        if response_times:
            avg_response_times = []
            for endpoint_data in response_times.values():
                if 'avg_response_time' in endpoint_data:
                    avg_response_times.append(endpoint_data['avg_response_time'])
            
            if avg_response_times:
                avg_response_time = statistics.mean(avg_response_times)
                # Score: 100 for <0.1s, 50 for 1s, 0 for >5s
                response_score = max(0, min(100, 100 - (avg_response_time * 20)))
                scores.append(response_score)
        
        return statistics.mean(scores) if scores else 0


async def run_performance_validation():
    """Run QBTC performance validation"""
    validator = QBTCPerformanceValidator()
    results = await validator.run_full_performance_suite()
    
    # Save results
    with open('performance_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Performance Score: {results['performance_score']:.1f}/100")
    print("Performance results saved to performance_results.json")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_performance_validation())
