# QBTC Automated Test Suite
import asyncio
import requests
import json
import time
from datetime import datetime


class QBTCTestSuite:
    """Comprehensive test suite for QBTC system"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.quantum_url = "http://localhost:8001"
        self.ollama_url = "http://localhost:11434"
    
    async def test_system_health(self):
        """Test system health endpoints"""
        endpoints = [
            f"{self.base_url}/health",
            f"{self.quantum_url}/health",
            f"{self.ollama_url}/api/version"
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=10)
                results[endpoint] = {
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'healthy': response.status_code == 200
                }
            except Exception as e:
                results[endpoint] = {
                    'error': str(e),
                    'healthy': False
                }
        
        return results
    
    async def test_api_endpoints(self):
        """Test critical API endpoints"""
        test_cases = [
            {
                'endpoint': f"{self.base_url}/api/chat",
                'method': 'POST',
                'data': {'message': 'test message', 'user_id': 'test_user'}
            },
            {
                'endpoint': f"{self.quantum_url}/quantum/state",
                'method': 'GET'
            },
            {
                'endpoint': f"{self.base_url}/api/status",
                'method': 'GET'
            }
        ]
        
        results = []
        for test_case in test_cases:
            try:
                if test_case['method'] == 'POST':
                    response = requests.post(
                        test_case['endpoint'], 
                        json=test_case.get('data', {}),
                        timeout=30
                    )
                else:
                    response = requests.get(test_case['endpoint'], timeout=30)
                
                results.append({
                    'endpoint': test_case['endpoint'],
                    'method': test_case['method'],
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'success': response.status_code in [200, 201, 202]
                })
                
            except Exception as e:
                results.append({
                    'endpoint': test_case['endpoint'],
                    'method': test_case['method'],
                    'error': str(e),
                    'success': False
                })
        
        return results
    
    async def run_full_test_suite(self):
        """Run complete test suite"""
        print("QBTC Automated Test Suite")
        print("=" * 50)
        
        # Run all tests
        health_results = await self.test_system_health()
        api_results = await self.test_api_endpoints()
        
        # Compile results
        test_summary = {
            'health_checks': health_results,
            'api_tests': api_results,
            'timestamp': datetime.now().isoformat(),
            'overall_health': self._calculate_overall_health(health_results, api_results)
        }
        
        return test_summary
    
    def _calculate_overall_health(self, health, api):
        """Calculate overall system health score"""
        scores = []
        
        # Health checks score
        healthy_endpoints = sum(1 for r in health.values() if r.get('healthy', False))
        health_score = healthy_endpoints / len(health) if health else 0
        scores.append(health_score)
        
        # API tests score
        successful_apis = sum(1 for r in api if r.get('success', False))
        api_score = successful_apis / len(api) if api else 0
        scores.append(api_score)
        
        return sum(scores) / len(scores)


async def run_tests():
    """Run QBTC test suite"""
    suite = QBTCTestSuite()
    results = await suite.run_full_test_suite()
    
    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Overall Health Score: {results['overall_health']:.2%}")
    print("Test results saved to test_results.json")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_tests())
