#!/usr/bin/env python3
"""
PLAN DE PRUEBAS DE PERFORMANCE - ANTES Y DESPUÉS
Evaluación completa de la transformación del sistema
"""

import asyncio
import aiohttp
import time
import json
import statistics
import psutil
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class TestPhase(Enum):
    BEFORE = "before"  # Sistema básico (puerto 5001)
    AFTER = "after"    # Sistema avanzado (puerto 5004)

@dataclass
class TestResult:
    phase: TestPhase
    test_name: str
    response_time: float
    success: bool
    quality_score: float
    nlp_score: float
    quantum_score: float
    memory_usage: float
    cpu_usage: float

class PerformanceTester:
    def __init__(self):
        self.before_url = "http://localhost:5001"
        self.after_url = "http://localhost:5004"
        self.results = []
        
        # Tests de texto
        self.text_tests = [
            {"name": "Simple Greeting", "text": "Hola, ¿cómo estás?"},
            {"name": "Technical Question", "text": "¿Puedes explicarme cómo funciona el algoritmo Random Forest?"},
            {"name": "Complex Programming", "text": "Implementa un sistema de microservicios con Docker"},
            {"name": "Emotional Analysis", "text": "Estoy muy feliz porque acabo de conseguir mi trabajo soñado!"},
            {"name": "Multi-language", "text": "Hello, I need help with Python programming. Bonjour!"}
        ]
        
        # Tests de carga
        self.load_tests = [
            {"name": "10 Users", "users": 10},
            {"name": "50 Users", "users": 50},
            {"name": "100 Users", "users": 100}
        ]

    async def run_comprehensive_testing(self):
        print("🚀 INICIANDO PRUEBAS DE PERFORMANCE")
        print("=" * 50)
        
        # Fase 1: Sistema básico
        print("\n📊 FASE 1: SISTEMA BÁSICO (PUERTO 5001)")
        await self.test_system(TestPhase.BEFORE)
        
        # Fase 2: Sistema avanzado
        print("\n📊 FASE 2: SISTEMA AVANZADO (PUERTO 5004)")
        await self.test_system(TestPhase.AFTER)
        
        # Fase 3: Análisis comparativo
        print("\n📊 FASE 3: ANÁLISIS COMPARATIVO")
        await self.generate_comparison()
        
        # Fase 4: Reporte
        print("\n📊 FASE 4: GENERANDO REPORTE")
        await self.generate_report()

    async def test_system(self, phase: TestPhase):
        url = self.before_url if phase == TestPhase.BEFORE else self.after_url
        print(f"🧪 Probando {phase.value} en {url}...")
        
        # Verificar conectividad
        if not await self.check_connectivity(url):
            print(f"❌ {phase.value} no disponible")
            return
        
        # Tests de texto
        for test in self.text_tests:
            await self.run_text_test(phase, test)
        
        # Tests de carga
        for test in self.load_tests:
            await self.run_load_test(phase, test)

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
                        
                        result = TestResult(
                            phase=phase,
                            test_name=test["name"],
                            response_time=response_time,
                            success=True,
                            quality_score=self.calculate_quality_score(response_data, phase),
                            nlp_score=self.calculate_nlp_score(response_data, phase),
                            quantum_score=self.calculate_quantum_score(response_data, phase),
                            memory_usage=memory_after - memory_before,
                            cpu_usage=cpu_after - cpu_before
                        )
                        
                        self.results.append(result)
                        print(f"    ✅ {response_time:.3f}s | Quality: {result.quality_score:.2f}")
                    else:
                        print(f"    ❌ Error {response.status}")
                        
        except Exception as e:
            print(f"    ❌ Error: {e}")

    async def run_load_test(self, phase: TestPhase, test: Dict[str, Any]):
        print(f"  🔄 Load Test: {test['name']}...")
        
        concurrent_users = test["users"]
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
        
        result = TestResult(
            phase=phase,
            test_name=f"Load Test {test['name']}",
            response_time=statistics.mean(response_times) if response_times else 0,
            success=successful_requests > 0,
            quality_score=successful_requests / total_requests if total_requests > 0 else 0,
            nlp_score=0.0,
            quantum_score=0.0,
            memory_usage=psutil.Process().memory_info().rss / 1024 / 1024,
            cpu_usage=psutil.cpu_percent()
        )
        
        self.results.append(result)
        print(f"    ✅ {successful_requests}/{total_requests} successful | Avg: {result.response_time:.3f}s")

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

    def calculate_nlp_score(self, response_data: Dict[str, Any], phase: TestPhase) -> float:
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

    async def generate_comparison(self):
        print("📊 Generando análisis comparativo...")
        
        before_results = [r for r in self.results if r.phase == TestPhase.BEFORE]
        after_results = [r for r in self.results if r.phase == TestPhase.AFTER]
        
        if before_results and after_results:
            # Calcular promedios
            before_avg_time = statistics.mean([r.response_time for r in before_results])
            after_avg_time = statistics.mean([r.response_time for r in after_results])
            
            before_avg_quality = statistics.mean([r.quality_score for r in before_results])
            after_avg_quality = statistics.mean([r.quality_score for r in after_results])
            
            # Calcular mejoras/regresiones
            time_improvement = ((before_avg_time - after_avg_time) / before_avg_time) * 100
            quality_improvement = ((after_avg_quality - before_avg_quality) / before_avg_quality) * 100
            
            print(f"  📈 Tiempo de respuesta:")
            print(f"     Antes: {before_avg_time:.3f}s | Después: {after_avg_time:.3f}s")
            print(f"     Mejora: {time_improvement:.1f}%")
            
            print(f"  📈 Calidad de respuesta:")
            print(f"     Antes: {before_avg_quality:.2f} | Después: {after_avg_quality:.2f}")
            print(f"     Mejora: {quality_improvement:.1f}%")
            
            # Análisis NLP y Cuántico
            after_nlp_avg = statistics.mean([r.nlp_score for r in after_results])
            after_quantum_avg = statistics.mean([r.quantum_score for r in after_results])
            
            print(f"  🧠 NLP Score promedio: {after_nlp_avg:.2f}")
            print(f"  ⚛️ Quantum Score promedio: {after_quantum_avg:.2f}")

    async def generate_report(self):
        print("📊 Generando reporte...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(self.results),
                "before_tests": len([r for r in self.results if r.phase == TestPhase.BEFORE]),
                "after_tests": len([r for r in self.results if r.phase == TestPhase.AFTER])
            },
            "results": [
                {
                    "phase": result.phase.value,
                    "test_name": result.test_name,
                    "response_time": result.response_time,
                    "success": result.success,
                    "quality_score": result.quality_score,
                    "nlp_score": result.nlp_score,
                    "quantum_score": result.quantum_score,
                    "memory_usage": result.memory_usage,
                    "cpu_usage": result.cpu_usage
                }
                for result in self.results
            ]
        }
        
        with open("performance_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("  📄 Reporte: performance_report.json")

async def main():
    tester = PerformanceTester()
    await tester.run_comprehensive_testing()

if __name__ == "__main__":
    asyncio.run(main())
