#!/usr/bin/env python3
"""
PERFORMANCE TESTING PLAN - PLAN DE PRUEBAS DE PERFORMANCE
Evaluación completa del antes y después de la transformación del sistema
"""

import asyncio
import aiohttp
import time
import json
import statistics
import psutil
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TestPhase(Enum):
    BEFORE = "before"  # Sistema básico (puerto 5001)
    AFTER = "after"    # Sistema avanzado (puerto 5004)

class TestCategory(Enum):
    TEXT_PROCESSING = "text_processing"
    NLP_ANALYSIS = "nlp_analysis"
    QUANTUM_PROCESSING = "quantum_processing"
    CONCURRENT_LOAD = "concurrent_load"
    RESPONSE_QUALITY = "response_quality"

@dataclass
class PerformanceMetrics:
    response_time: float
    throughput: float
    memory_usage: float
    cpu_usage: float
    success_rate: float
    error_rate: float
    quality_score: float
    nlp_accuracy: float
    quantum_score: float

@dataclass
class TestResult:
    phase: TestPhase
    category: TestCategory
    test_name: str
    metrics: PerformanceMetrics
    timestamp: datetime
    details: Dict[str, Any] = None

class PerformanceTestingPlan:
    def __init__(self):
        self.before_url = "http://localhost:5001"
        self.after_url = "http://localhost:5004"
        self.results = []
        
        # Tests de texto
        self.text_tests = [
            {"name": "Simple Greeting", "text": "Hola, ¿cómo estás?"},
            {"name": "Technical Question", "text": "¿Puedes explicarme cómo funciona el algoritmo Random Forest?"},
            {"name": "Complex Programming", "text": "Implementa un sistema de microservicios con Docker y Kubernetes"},
            {"name": "Emotional Analysis", "text": "Estoy muy feliz porque acabo de conseguir mi trabajo soñado!"},
            {"name": "Multi-language", "text": "Hello, I need help with Python programming. Bonjour!"}
        ]
        
        # Tests de carga
        self.load_tests = [
            {"name": "10 Users", "concurrent_users": 10},
            {"name": "50 Users", "concurrent_users": 50},
            {"name": "100 Users", "concurrent_users": 100}
        ]

    async def run_comprehensive_testing(self):
        print("🚀 INICIANDO PRUEBAS COMPLETAS DE PERFORMANCE")
        
        # Fase 1: Sistema básico
        print("\n📊 FASE 1: SISTEMA BÁSICO (PUERTO 5001)")
        await self.test_basic_system()
        
        # Fase 2: Sistema avanzado
        print("\n📊 FASE 2: SISTEMA AVANZADO (PUERTO 5004)")
        await self.test_advanced_system()
        
        # Fase 3: Análisis comparativo
        print("\n📊 FASE 3: ANÁLISIS COMPARATIVO")
        await self.generate_comparison_analysis()
        
        # Fase 4: Reportes
        print("\n📊 FASE 4: GENERANDO REPORTES")
        await self.generate_reports()

    async def test_basic_system(self):
        print("🧪 Probando sistema básico...")
        
        if not await self.check_connectivity(self.before_url):
            print("❌ Sistema básico no disponible")
            return
        
        for test in self.text_tests:
            await self.run_text_test(TestPhase.BEFORE, test)
        
        for test in self.load_tests:
            await self.run_load_test(TestPhase.BEFORE, test)

    async def test_advanced_system(self):
        print("🧪 Probando sistema avanzado...")
        
        if not await self.check_connectivity(self.after_url):
            print("❌ Sistema avanzado no disponible")
            return
        
        for test in self.text_tests:
            await self.run_text_test(TestPhase.AFTER, test)
        
        for test in self.load_tests:
            await self.run_load_test(TestPhase.AFTER, test)

    async def check_connectivity(self, url: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/api/status", timeout=5) as response:
                    return response.status == 200
        except:
            return False

    async def run_text_test(self, phase: TestPhase, test: Dict[str, Any]):
        print(f"  📝 {test['name']}...")
        
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss / 1024 / 1024
        cpu_before = psutil.cpu_percent()
        
        try:
            url = self.before_url if phase == TestPhase.BEFORE else self.after_url
            endpoint = "/api/process" if phase == TestPhase.BEFORE else "/api/process_text"
            
            async with aiohttp.ClientSession() as session:
                if phase == TestPhase.BEFORE:
                    data = {
                        "api_key": "demo_key_web",
                        "query": test["text"],
                        "type": "text"
                    }
                else:
                    data = {
                        "text": test["text"],
                        "session_id": f"test_{int(time.time())}",
                        "user_id": "test_user"
                    }
                
                async with session.post(f"{url}{endpoint}", json=data, timeout=30) as response:
                    response_time = time.time() - start_time
                    memory_after = psutil.Process().memory_info().rss / 1024 / 1024
                    cpu_after = psutil.cpu_percent()
                    
                    if response.status == 200:
                        response_data = await response.json()
                        
                        metrics = PerformanceMetrics(
                            response_time=response_time,
                            throughput=1.0 / response_time,
                            memory_usage=memory_after - memory_before,
                            cpu_usage=cpu_after - cpu_before,
                            success_rate=1.0,
                            error_rate=0.0,
                            quality_score=self.calculate_quality_score(response_data, phase),
                            nlp_accuracy=self.calculate_nlp_accuracy(response_data, phase),
                            quantum_score=self.calculate_quantum_score(response_data, phase)
                        )
                        
                        result = TestResult(
                            phase=phase,
                            category=TestCategory.TEXT_PROCESSING,
                            test_name=test["name"],
                            metrics=metrics,
                            timestamp=datetime.now(),
                            details={"response": response_data}
                        )
                        
                        self.results.append(result)
                        print(f"    ✅ {response_time:.3f}s")
                    else:
                        print(f"    ❌ Error {response.status}")
                        
        except Exception as e:
            print(f"    ❌ Error: {e}")

    async def run_load_test(self, phase: TestPhase, test: Dict[str, Any]):
        print(f"  🔄 Load Test: {test['name']}...")
        
        concurrent_users = test["concurrent_users"]
        successful_requests = 0
        failed_requests = 0
        response_times = []
        
        async def make_request():
            nonlocal successful_requests, failed_requests
            try:
                url = self.before_url if phase == TestPhase.BEFORE else self.after_url
                endpoint = "/api/process" if phase == TestPhase.BEFORE else "/api/process_text"
                
                async with aiohttp.ClientSession() as session:
                    if phase == TestPhase.BEFORE:
                        data = {
                            "api_key": "demo_key_web",
                            "query": "Test load",
                            "type": "text"
                        }
                    else:
                        data = {
                            "text": "Test load",
                            "session_id": f"load_test_{int(time.time())}",
                            "user_id": "load_test_user"
                        }
                    
                    req_start = time.time()
                    async with session.post(f"{url}{endpoint}", json=data, timeout=30) as response:
                        req_time = time.time() - req_start
                        response_times.append(req_time)
                        
                        if response.status == 200:
                            successful_requests += 1
                        else:
                            failed_requests += 1
                            
            except Exception as e:
                failed_requests += 1
        
        start_time = time.time()
        tasks = []
        for _ in range(concurrent_users):
            task = asyncio.create_task(make_request())
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        total_requests = successful_requests + failed_requests
        
        metrics = PerformanceMetrics(
            response_time=statistics.mean(response_times) if response_times else 0,
            throughput=total_requests / total_time,
            memory_usage=psutil.Process().memory_info().rss / 1024 / 1024,
            cpu_usage=psutil.cpu_percent(),
            success_rate=successful_requests / total_requests if total_requests > 0 else 0,
            error_rate=failed_requests / total_requests if total_requests > 0 else 0,
            quality_score=0.0,
            nlp_accuracy=0.0,
            quantum_score=0.0
        )
        
        result = TestResult(
            phase=phase,
            category=TestCategory.CONCURRENT_LOAD,
            test_name=test["name"],
            metrics=metrics,
            timestamp=datetime.now(),
            details={
                "concurrent_users": concurrent_users,
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests
            }
        )
        
        self.results.append(result)
        print(f"    ✅ {successful_requests}/{total_requests} requests successful")

    def calculate_quality_score(self, response_data: Dict[str, Any], phase: TestPhase) -> float:
        if phase == TestPhase.BEFORE:
            if response_data.get("response"):
                return 0.7
            return 0.0
        else:
            if response_data.get("success"):
                nlp_score = response_data.get("nlp_analysis", {}).get("sentiment", {}).get("confidence", 0.5)
                quantum_score = response_data.get("quantum_analysis", {}).get("quantum_score", 0.5)
                return (nlp_score + quantum_score) / 2
            return 0.0

    def calculate_nlp_accuracy(self, response_data: Dict[str, Any], phase: TestPhase) -> float:
        if phase == TestPhase.BEFORE:
            return 0.0
        else:
            nlp_analysis = response_data.get("nlp_analysis", {})
            if nlp_analysis:
                sentiment_conf = nlp_analysis.get("sentiment", {}).get("confidence", 0.0)
                intent_conf = nlp_analysis.get("intent", {}).get("confidence", 0.0)
                return (sentiment_conf + intent_conf) / 2
            return 0.0

    def calculate_quantum_score(self, response_data: Dict[str, Any], phase: TestPhase) -> float:
        if phase == TestPhase.BEFORE:
            return 0.0
        else:
            quantum_analysis = response_data.get("quantum_analysis", {})
            if quantum_analysis:
                return quantum_analysis.get("quantum_score", 0.0)
            return 0.0

    async def generate_comparison_analysis(self):
        print("📊 Generando análisis comparativo...")
        
        before_results = [r for r in self.results if r.phase == TestPhase.BEFORE]
        after_results = [r for r in self.results if r.phase == TestPhase.AFTER]
        
        categories = set([r.category for r in self.results])
        
        for category in categories:
            before_category = [r for r in before_results if r.category == category]
            after_category = [r for r in after_results if r.category == category]
            
            if before_category and after_category:
                before_avg = self.calculate_average_metrics(before_category)
                after_avg = self.calculate_average_metrics(after_category)
                
                improvement = self.calculate_improvement_percentage(before_avg, after_avg)
                regression = self.calculate_regression_percentage(before_avg, after_avg)
                
                if improvement > regression:
                    overall_impact = "IMPROVED"
                elif regression > improvement:
                    overall_impact = "REGRESSED"
                else:
                    overall_impact = "NEUTRAL"
                
                print(f"  📈 {category.value}: {overall_impact}")
                print(f"     Mejora: {improvement:.1f}% | Regresión: {regression:.1f}%")

    def calculate_average_metrics(self, results: List[TestResult]) -> PerformanceMetrics:
        if not results:
            return PerformanceMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        return PerformanceMetrics(
            response_time=statistics.mean([r.metrics.response_time for r in results]),
            throughput=statistics.mean([r.metrics.throughput for r in results]),
            memory_usage=statistics.mean([r.metrics.memory_usage for r in results]),
            cpu_usage=statistics.mean([r.metrics.cpu_usage for r in results]),
            success_rate=statistics.mean([r.metrics.success_rate for r in results]),
            error_rate=statistics.mean([r.metrics.error_rate for r in results]),
            quality_score=statistics.mean([r.metrics.quality_score for r in results]),
            nlp_accuracy=statistics.mean([r.metrics.nlp_accuracy for r in results]),
            quantum_score=statistics.mean([r.metrics.quantum_score for r in results])
        )

    def calculate_improvement_percentage(self, before: PerformanceMetrics, after: PerformanceMetrics) -> float:
        improvements = []
        
        if before.response_time > 0:
            improvement = ((before.response_time - after.response_time) / before.response_time) * 100
            if improvement > 0:
                improvements.append(improvement)
        
        if before.throughput > 0:
            improvement = ((after.throughput - before.throughput) / before.throughput) * 100
            if improvement > 0:
                improvements.append(improvement)
        
        if before.quality_score > 0:
            improvement = ((after.quality_score - before.quality_score) / before.quality_score) * 100
            if improvement > 0:
                improvements.append(improvement)
        
        return statistics.mean(improvements) if improvements else 0.0

    def calculate_regression_percentage(self, before: PerformanceMetrics, after: PerformanceMetrics) -> float:
        regressions = []
        
        if before.response_time > 0:
            regression = ((after.response_time - before.response_time) / before.response_time) * 100
            if regression > 0:
                regressions.append(regression)
        
        if before.throughput > 0:
            regression = ((before.throughput - after.throughput) / before.throughput) * 100
            if regression > 0:
                regressions.append(regression)
        
        if before.success_rate > 0:
            regression = ((before.success_rate - after.success_rate) / before.success_rate) * 100
            if regression > 0:
                regressions.append(regression)
        
        return statistics.mean(regressions) if regressions else 0.0

    async def generate_reports(self):
        print("📊 Generando reportes...")
        
        # Reporte resumido
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_summary": {
                "total_tests": len(self.results),
                "before_tests": len([r for r in self.results if r.phase == TestPhase.BEFORE]),
                "after_tests": len([r for r in self.results if r.phase == TestPhase.AFTER])
            },
            "detailed_results": [
                {
                    "phase": result.phase.value,
                    "category": result.category.value,
                    "test_name": result.test_name,
                    "response_time": result.metrics.response_time,
                    "throughput": result.metrics.throughput,
                    "quality_score": result.metrics.quality_score,
                    "nlp_accuracy": result.metrics.nlp_accuracy,
                    "quantum_score": result.metrics.quantum_score
                }
                for result in self.results
            ]
        }
        
        with open("performance_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("  📄 Reporte: performance_test_report.json")

async def main():
    tester = PerformanceTestingPlan()
    await tester.run_comprehensive_testing()

if __name__ == "__main__":
    asyncio.run(main())
