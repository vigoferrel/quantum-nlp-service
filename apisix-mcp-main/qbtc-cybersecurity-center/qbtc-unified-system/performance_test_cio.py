#!/usr/bin/env python3
"""
Quantum CIO Performance Test
===========================
Performs performance testing on the Quantum CIO system components.

- Tests endpoints with simulated load.
"""

import time
import asyncio
import aiohttp
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [PerformanceTest] - %(levelname)s - %(message)s')
logger = logging.getLogger("PerformanceTest")

# Endpoints to test
API_GATEWAY_URL = "http://localhost:8000/v1/chat/completions"
QUANTUM_CORE_URL = "http://localhost:8001/process_query"

# Test configurations
NUM_REQUESTS = 100
CONCURRENCY = 10

async def perform_request(session: aiohttp.ClientSession, url: str, payload: Dict) -> Dict:
    """Perform a single HTTP request and measure performance."""
    try:
        start_time = time.time()
        async with session.post(url, json=payload) as response:
            await response.text()  # Read to complete the request
            elapsed_time = time.time() - start_time
            return {"status": response.status, "elapsed_time": elapsed_time}
    except Exception as e:
        logger.error("Request to %s failed: %s", url, e)
        return {"status": 0, "elapsed_time": None}

async def perform_test(url: str, payload: Dict) -> List[Dict]:
    """Perform a load test on the given URL."""
    async with aiohttp.ClientSession() as session:
        tasks = [perform_request(session, url, payload) for _ in range(NUM_REQUESTS)]
        responses = await asyncio.gather(*tasks)
        return responses

async def main():
    """Main function to conduct performance tests."""
    logger.info("Starting performance tests...")

    # Payloads
    api_gateway_payload = {
        "model": "local-qcc-26d",
        "messages": [{"role": "user", "content": "Test message payload"}],
    }
    quantum_core_payload = {"query": "Test message payload"}

    # Testing API Gateway
    logger.info("Testing API Gateway...")
    api_gateway_responses = await perform_test(API_GATEWAY_URL, api_gateway_payload)
    logger.info("API Gateway Test Completed.")

    # Testing Quantum Core
    logger.info("Testing Quantum Core...")
    quantum_core_responses = await perform_test(QUANTUM_CORE_URL, quantum_core_payload)
    logger.info("Quantum Core Test Completed.")

    # Gather results
    logger.info("Analyzing results...")
    analyze_results("API Gateway", api_gateway_responses)
    analyze_results("Quantum Core", quantum_core_responses)


def analyze_results(service_name: str, responses: List[Dict]):
    """Analyze performance results and print a summary."""
    successful_requests = [r for r in responses if r['status'] == 200]
    failed_requests = [r for r in responses if r['status'] != 200]
    avg_time = sum(r['elapsed_time'] for r in successful_requests) / len(successful_requests) if successful_requests else float('inf')

    logger.info("%s Results:", service_name)
    logger.info("Total Requests: %d", len(responses))
    logger.info("Successful Requests: %d", len(successful_requests))
    logger.info("Failed Requests: %d", len(failed_requests))
    logger.info("Average Time: %.3fs", avg_time)


if __name__ == "__main__":
    asyncio.run(main())

