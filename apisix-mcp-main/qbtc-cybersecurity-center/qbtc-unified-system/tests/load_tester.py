#!/usr/bin/env python3
"""QBTC Load Testing Framework"""

import asyncio
import aiohttp
import time
import statistics
import json
import argparse


class QBTCLoadTester:
    """Load testing framework for QBTC system"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    async def run_load_test(self, concurrent_users=10, requests_per_user=50):
        """Run comprehensive load test"""
        print(f"Starting load test:")
        print(f"- Concurrent users: {concurrent_users}")
        print(f"- Requests per user: {requests_per_user}")
        print(f"- Total requests: {concurrent_users * requests_per_user}")
        print("=" * 50)
        
        start_time = time.time()
        
        # Create user tasks
        user_tasks = []
        for user_id in range(concurrent_users):
            task = asyncio.create_task(
                self.simulate_user_session(user_id, requests_per_user)
            )
            user_tasks.append(task)
        
        # Wait for all users to complete
        all_results = await asyncio.gather(*user_tasks)
        
        # Flatten results
        flat_results = []
        for user_results in all_results:
            flat_results.extend(user_results)
        
        total_time = time.time() - start_time
        
        # Analyze results
        analysis = self._analyze_results(flat_results, total_time)
        
        # Save results
        test_report = {
            'test_parameters': {
                'concurrent_users': concurrent_users,
                'requests_per_user': requests_per_user,
                'total_requests': len(flat_results),
                'test_duration': total_time
            },
            'results': flat_results,
            'analysis': analysis
        }
        
        with open('load_test_results.json', 'w') as f:
            json.dump(test_report, f, indent=2)
        
        return test_report
    
    async def simulate_user_session(self, session_id, total_requests=50):
        """Simulate a complete user session"""
        session_results = []
        
        async with aiohttp.ClientSession() as session:
            for request_num in range(total_requests):
                start_time = time.time()
                try:
                    async with session.get(f"{self.base_url}/health") as response:
                        response_time = time.time() - start_time
                        session_results.append({
                            'session_id': session_id,
                            'request_num': request_num,
                            'response_time': response_time,
                            'status_code': response.status,
                            'success': response.status == 200
                        })
                    
                    # Realistic delay between requests
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    session_results.append({
                        'session_id': session_id,
                        'request_num': request_num,
                        'error': str(e),
                        'response_time': time.time() - start_time,
                        'success': False
                    })
        
        return session_results
    
    def _analyze_results(self, results, total_time):
        """Analyze load test results"""
        if not results:
            return {'error': 'No results to analyze'}
        
        # Basic statistics
        successful_requests = [r for r in results if r.get('success', False)]
        failed_requests = [r for r in results if not r.get('success', False)]
        
        response_times = [r['response_time'] for r in results if 'response_time' in r]
        
        analysis = {
            'summary': {
                'total_requests': len(results),
                'successful_requests': len(successful_requests),
                'failed_requests': len(failed_requests),
                'success_rate': len(successful_requests) / len(results) * 100,
                'requests_per_second': len(results) / total_time,
                'test_duration': total_time
            },
            'response_times': {
                'average': statistics.mean(response_times) if response_times else 0,
                'median': statistics.median(response_times) if response_times else 0,
                'min': min(response_times) if response_times else 0,
                'max': max(response_times) if response_times else 0
            }
        }
        
        return analysis


async def main():
    """Main function for load testing"""
    parser = argparse.ArgumentParser(description='QBTC Load Testing Framework')
    parser.add_argument('--users', type=int, default=10, help='Number of concurrent users')
    parser.add_argument('--requests', type=int, default=50, help='Requests per user')
    parser.add_argument('--base-url', default='http://localhost:8000', help='Base API URL')
    
    args = parser.parse_args()
    
    load_tester = QBTCLoadTester(args.base_url)
    results = await load_tester.run_load_test(
        concurrent_users=args.users,
        requests_per_user=args.requests
    )
    
    print("\nLoad Test Results:")
    print("=" * 50)
    print(f"Success Rate: {results['analysis']['summary']['success_rate']:.1f}%")
    print(f"Average Response Time: {results['analysis']['response_times']['average']:.3f}s")
    print(f"Requests per Second: {results['analysis']['summary']['requests_per_second']:.1f}")
    print(f"\nDetailed results saved to: load_test_results.json")


if __name__ == "__main__":
    asyncio.run(main())
