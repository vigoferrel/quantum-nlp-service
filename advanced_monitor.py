#!/usr/bin/env python3
"""
📊 MONITOR DE RENDIMIENTO AVANZADO
==================================
"""

import time
import psutil
import json
from datetime import datetime
from collections import deque
import threading

class AdvancedMonitor:
    def __init__(self):
        self.metrics = {
            "response_times": deque(maxlen=1000),
            "requests_count": 0,
            "errors_count": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "start_time": time.time()
        }
        self.lock = threading.Lock()
    
    def record_request(self, response_time: float, success: bool, cache_hit: bool = False):
        with self.lock:
            self.metrics["response_times"].append(response_time)
            self.metrics["requests_count"] += 1
            if not success:
                self.metrics["errors_count"] += 1
            if cache_hit:
                self.metrics["cache_hits"] += 1
            else:
                self.metrics["cache_misses"] += 1
    
    def get_stats(self):
        with self.lock:
            response_times = list(self.metrics["response_times"])
            return {
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.metrics["start_time"],
                "requests": {
                    "total": self.metrics["requests_count"],
                    "errors": self.metrics["errors_count"],
                    "success_rate": (self.metrics["requests_count"] - self.metrics["errors_count"]) / max(self.metrics["requests_count"], 1) * 100
                },
                "performance": {
                    "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                    "min_response_time": min(response_times) if response_times else 0,
                    "max_response_time": max(response_times) if response_times else 0
                },
                "cache": {
                    "hits": self.metrics["cache_hits"],
                    "misses": self.metrics["cache_misses"],
                    "hit_rate": self.metrics["cache_hits"] / max(self.metrics["cache_hits"] + self.metrics["cache_misses"], 1) * 100
                },
                "system": {
                    "memory_usage": psutil.virtual_memory().percent,
                    "cpu_usage": psutil.cpu_percent()
                }
            }

# Instancia global
advanced_monitor = AdvancedMonitor()

def test_monitor():
    print("🧪 Probando monitor avanzado...")
    for i in range(5):
        time.sleep(1)
        advanced_monitor.record_request(1.5 + i * 0.2, True, i % 2 == 0)
    
    stats = advanced_monitor.get_stats()
    print("📊 Estadísticas:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_monitor()
