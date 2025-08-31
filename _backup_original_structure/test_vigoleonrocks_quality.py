#!/usr/bin/env python3
"""
Test de Calidad - Vigoleonrocks Unified Multimodal
Verificación exhaustiva de resultados de calidad
"""

import asyncio
import json
import time
import base64
from datetime import datetime
from typing import Dict, List, Any
from vigoleonrocks_unified_multimodal import OptimizedMultimodalProcessor, MultimodalRequest

class QualityTester:
    """Tester exhaustivo de calidad basado en benchmarks"""
    
    def __init__(self):
        self.processor = OptimizedMultimodalProcessor()
        self.test_cases = self._prepare_test_cases()
        self.results = []
        
    def _prepare_test_cases(self) -> List[Dict[str, Any]]:
        """Preparar casos de prueba basados en benchmarks históricos"""
        
        return [
            {
                "category": "PROGRAMMING_ELITE",
                "test_name": "Algoritmo Quicksort Optimizado",
                "query": "Implementa un algoritmo de ordenamiento quicksort optimizado en Python con análisis de complejidad O(n log n) y optimizaciones para casos edge",
                "expected_aspects": ["código funcional", "análisis complejidad", "optimizaciones memoria", "casos edge"],
                "difficulty": "EXPERT",
                "target_score": 0.905
            },
            {
                "category": "PROGRAMMING_ELITE", 
                "test_name": "Grafo Bipartito BFS",
                "query": "Crea una función que detecte si un grafo es bipartito usando BFS con validación de entrada y manejo de errores",
                "expected_aspects": ["algoritmo BFS", "validación entrada", "manejo errores", "casos edge"],
                "difficulty": "EXPERT",
                "target_score": 0.905
            },
            {
                "category": "PROGRAMMING_ELITE",
                "test_name": "Sistema Caché LRU O(1)",
                "query": "Desarrolla un sistema de caché LRU con complejidad O(1) para todas las operaciones incluyendo get, put y eviction",
                "expected_aspects": ["complejidad O(1)", "LRU implementation", "HashMap + LinkedList", "testing"],
                "difficulty": "EXPERT", 
                "target_score": 0.905
            },
            {
                "category": "REASONING_ELITE",
                "test_name": "Problema Lógico Tribal",
                "query": "En una isla hay 3 tribus: Veraces (siempre dicen verdad), Mentirosos (siempre mienten), y Aleatorios (responden al azar). Un explorador encuentra 3 habitantes: X dice 'Y es Veraz', Y dice 'Z es Aleatorio', Z dice 'X es Mentiroso'. Si solo hay un Veraz, ¿qué tribu es cada uno?",
                "expected_aspects": ["lógica formal", "análisis casos", "demostración", "conclusión"],
                "difficulty": "EXPERT",
                "target_score": 1.0
            },
            {
                "category": "MATHEMATICS_ELITE",
                "test_name": "Serie Infinita Convergente",
                "query": "Calcula la suma de la serie infinita: Σ(n=1 to ∞) n³/3ⁿ. Demuestra la convergencia usando el criterio de la raíz y encuentra el valor exacto mediante manipulación de series de potencias.",
                "expected_aspects": ["convergencia", "criterio raíz", "manipulación series", "cálculo exacto"],
                "difficulty": "EXPERT",
                "target_score": 1.0
            },
            {
                "category": "ANALYSIS_ELITE",
                "test_name": "Arquitecturas Distribuidas",
                "query": "Analiza las ventajas y desventajas de diferentes arquitecturas de software para sistemas distribuidos",
                "expected_aspects": ["análisis comparativo", "pros y contras", "casos de uso", "recomendaciones"],
                "difficulty": "EXPERT",
                "target_score": 1.0
            },
            {
                "category": "SYNTHESIS_ELITE",
                "test_name": "Integración Tecnológica",
                "query": "Sintetiza los principios fundamentales de la programación orientada a objetos con patrones de diseño",
                "expected_aspects": ["integración conceptual", "ejemplos prácticos", "síntesis coherente", "aplicación"],
                "difficulty": "EXPERT",
                "target_score": 1.0
            },
            {
                "category": "MULTIMODAL_TEST",
                "test_name": "Procesamiento Imagen + Texto",
                "query": "Analiza esta imagen y describe los elementos de programación que ves",
                "image_data": self._generate_dummy_image(),
                "expected_aspects": ["análisis visual", "identificación elementos", "descripción técnica"],
                "difficulty": "ADVANCED",
                "target_score": 0.95
            },
            {
                "category": "MULTIMODAL_TEST",
                "test_name": "Audio + Texto Combinado", 
                "query": "Procesa este audio y extrae las características técnicas principales",
                "audio_data": self._generate_dummy_audio(),
                "expected_aspects": ["procesamiento audio", "extracción características", "análisis técnico"],
                "difficulty": "ADVANCED",
                "target_score": 0.95
            },
            {
                "category": "PERFORMANCE_TEST",
                "test_name": "Test Velocidad vs Competidores",
                "query": "Explica las diferencias entre programación funcional y orientada a objetos con ejemplos prácticos",
                "expected_aspects": ["comparación detallada", "ejemplos código", "casos uso"],
                "difficulty": "INTERMEDIATE",
                "target_score": 0.89,
                "speed_target": 2.5  # Target: 96% más rápido que competidores
            }
        ]
    
    def _generate_dummy_image(self) -> str:
        """Generar imagen dummy en base64 para testing"""
        # Simular datos de imagen base64
        dummy_data = b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        return base64.b64encode(dummy_data).decode()
    
    def _generate_dummy_audio(self) -> str:
        """Generar audio dummy en base64 para testing"""
        # Simular datos de audio base64
        dummy_data = b"audio_dummy_data_for_testing_purposes"
        return base64.b64encode(dummy_data).decode()
    
    async def run_comprehensive_quality_test(self) -> Dict[str, Any]:
        """Ejecutar test exhaustivo de calidad"""
        
        print("=" * 80)
        print("VIGOLEONROCKS UNIFIED MULTIMODAL - TEST DE CALIDAD EXHAUSTIVO")
        print("=" * 80)
        print(f"Iniciando testing a las: {datetime.now().isoformat()}")
        print(f"Casos de prueba preparados: {len(self.test_cases)}")
        print("=" * 80)
        
        start_time = time.time()
        
        # Ejecutar todos los casos de prueba
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}] Ejecutando: {test_case['test_name']}")
            print(f"Categoría: {test_case['category']}")
            print(f"Dificultad: {test_case['difficulty']}")
            
            result = await self._execute_test_case(test_case)
            self.results.append(result)
            
            # Mostrar resultado inmediato
            print(f"✅ Completado en {result['processing_time']:.2f}s")
            print(f"📊 Quality Score: {result['quality_score']:.3f} (Target: {test_case['target_score']:.3f})")
            print(f"🔬 Quantum Score: {result['quantum_score']:.3f}")
            print(f"🚀 Strategy Used: {result['strategy']}")
            
            if result['quality_score'] >= test_case['target_score']:
                print("✅ PASSED - Score objetivo alcanzado")
            else:
                print("❌ REVIEW - Score por debajo del objetivo")
        
        # Generar reporte final
        total_time = time.time() - start_time
        final_report = self._generate_final_report(total_time)
        
        # Mostrar resumen
        print("\n" + "=" * 80)
        print("RESUMEN FINAL DE CALIDAD")
        print("=" * 80)
        print(f"Tests ejecutados: {final_report['tests_executed']}")
        print(f"Tests aprobados: {final_report['tests_passed']}")
        print(f"Tasa de éxito: {final_report['success_rate']:.1f}%")
        print(f"Quality Score promedio: {final_report['avg_quality_score']:.3f}")
        print(f"Quantum Score promedio: {final_report['avg_quantum_score']:.3f}")
        print(f"Tiempo total: {final_report['total_testing_time']:.2f}s")
        print(f"Tiempo promedio por test: {final_report['avg_processing_time']:.2f}s")
        
        # Comparación con benchmarks
        print("\n📈 COMPARACIÓN CON BENCHMARKS HISTÓRICOS:")
        print(f"Target Score: {final_report['target_benchmark']:.3f}")
        print(f"Achieved Score: {final_report['avg_quality_score']:.3f}")
        print(f"Performance: {final_report['performance_vs_target']}")
        
        # Análisis por estrategia
        print("\n🎯 ANÁLISIS POR ESTRATEGIA:")
        for strategy, data in final_report['strategy_analysis'].items():
            print(f"- {strategy}: {data['count']} tests, Score: {data['avg_score']:.3f}")
        
        # Análisis multimodal
        if final_report['multimodal_tests'] > 0:
            print(f"\n🌐 CAPACIDADES MULTIMODALES:")
            print(f"- Tests multimodales: {final_report['multimodal_tests']}")
            print(f"- Score multimodal promedio: {final_report['multimodal_score']:.3f}")
        
        print("\n" + "=" * 80)
        
        return final_report
    
    async def _execute_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar un caso de prueba individual"""
        
        # Crear request
        request = MultimodalRequest(
            text=test_case['query'],
            image_data=test_case.get('image_data'),
            audio_data=test_case.get('audio_data'),
            model="vigoleonrocks_optimized"
        )
        
        # Procesar request
        start_time = time.time()
        result = await self.processor.process_request(request)
        processing_time = time.time() - start_time
        
        # Analizar calidad de la respuesta
        quality_analysis = self._analyze_response_quality(result['response'], test_case)
        
        return {
            "test_name": test_case['test_name'],
            "category": test_case['category'],
            "difficulty": test_case['difficulty'],
            "processing_time": processing_time,
            "quality_score": result['quality_score'],
            "quantum_score": result['quantum_score'],
            "strategy": result['model_used'].replace('vigoleonrocks_', ''),
            "target_score": test_case['target_score'],
            "passed": result['quality_score'] >= test_case['target_score'],
            "response_length": len(result['response']),
            "multimodal_features": result['multimodal_features'],
            "quality_analysis": quality_analysis,
            "response_sample": result['response'][:300] + "..." if len(result['response']) > 300 else result['response']
        }
    
    def _analyze_response_quality(self, response: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar la calidad de la respuesta contra aspectos esperados"""
        
        expected_aspects = test_case.get('expected_aspects', [])
        found_aspects = []
        
        response_lower = response.lower()
        
        # Verificar aspectos específicos por categoría
        if test_case['category'] == "PROGRAMMING_ELITE":
            if "```python" in response or "def " in response_lower:
                found_aspects.append("código funcional")
            if "complejidad" in response_lower or "o(n" in response_lower:
                found_aspects.append("análisis complejidad")
            if "optimización" in response_lower or "optimizado" in response_lower:
                found_aspects.append("optimizaciones")
            if "test" in response_lower or "ejemplo" in response_lower:
                found_aspects.append("testing")
        
        elif test_case['category'] == "REASONING_ELITE":
            if "paso" in response_lower or "análisis" in response_lower:
                found_aspects.append("análisis detallado")
            if "lógica" in response_lower or "demostración" in response_lower:
                found_aspects.append("razonamiento lógico")
            if "conclusión" in response_lower or "resultado" in response_lower:
                found_aspects.append("conclusión")
        
        elif test_case['category'] == "MATHEMATICS_ELITE":
            if "convergencia" in response_lower or "serie" in response_lower:
                found_aspects.append("análisis matemático")
            if "criterio" in response_lower or "raíz" in response_lower:
                found_aspects.append("métodos específicos")
            if "cálculo" in response_lower or "valor" in response_lower:
                found_aspects.append("cálculo exacto")
        
        coverage_score = len(found_aspects) / len(expected_aspects) if expected_aspects else 1.0
        
        return {
            "expected_aspects": expected_aspects,
            "found_aspects": found_aspects,
            "coverage_score": coverage_score,
            "has_code": "```" in response,
            "has_analysis": "análisis" in response_lower,
            "has_examples": "ejemplo" in response_lower,
            "technical_depth": self._assess_technical_depth(response)
        }
    
    def _assess_technical_depth(self, response: str) -> str:
        """Evaluar la profundidad técnica de la respuesta"""
        
        depth_indicators = 0
        
        if len(response) > 500:
            depth_indicators += 1
        if "implementación" in response.lower():
            depth_indicators += 1  
        if "optimización" in response.lower():
            depth_indicators += 1
        if "complejidad" in response.lower():
            depth_indicators += 1
        if "```" in response:  # Código incluido
            depth_indicators += 2
        
        if depth_indicators >= 4:
            return "HIGH"
        elif depth_indicators >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_final_report(self, total_time: float) -> Dict[str, Any]:
        """Generar reporte final completo"""
        
        tests_executed = len(self.results)
        tests_passed = sum(1 for r in self.results if r['passed'])
        
        # Scores promedio
        avg_quality = sum(r['quality_score'] for r in self.results) / tests_executed
        avg_quantum = sum(r['quantum_score'] for r in self.results) / tests_executed
        avg_processing_time = sum(r['processing_time'] for r in self.results) / tests_executed
        
        # Análisis por estrategia
        strategy_stats = {}
        for result in self.results:
            strategy = result['strategy']
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {'scores': [], 'count': 0}
            strategy_stats[strategy]['scores'].append(result['quality_score'])
            strategy_stats[strategy]['count'] += 1
        
        strategy_analysis = {}
        for strategy, stats in strategy_stats.items():
            strategy_analysis[strategy] = {
                'count': stats['count'],
                'avg_score': sum(stats['scores']) / len(stats['scores'])
            }
        
        # Tests multimodales
        multimodal_tests = sum(1 for r in self.results if r.get('multimodal_features'))
        multimodal_score = sum(r['quality_score'] for r in self.results if r.get('multimodal_features')) / multimodal_tests if multimodal_tests > 0 else 0
        
        # Target benchmark (basado en benchmarks históricos)
        target_benchmark = 0.889  # Score de Vigoleonrocks vs competidores
        
        return {
            "timestamp": datetime.now().isoformat(),
            "tests_executed": tests_executed,
            "tests_passed": tests_passed,
            "success_rate": (tests_passed / tests_executed) * 100,
            "avg_quality_score": avg_quality,
            "avg_quantum_score": avg_quantum,
            "avg_processing_time": avg_processing_time,
            "total_testing_time": total_time,
            "target_benchmark": target_benchmark,
            "performance_vs_target": "SUPERIOR" if avg_quality >= target_benchmark else "REVIEW NEEDED",
            "strategy_analysis": strategy_analysis,
            "multimodal_tests": multimodal_tests,
            "multimodal_score": multimodal_score,
            "detailed_results": self.results
        }
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Guardar reporte en archivo JSON"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vigoleonrocks_quality_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte guardado en: {filename}")

async def main():
    """Función principal de testing"""
    
    print("🚀 Iniciando test de calidad Vigoleonrocks Unified Multimodal...")
    
    tester = QualityTester()
    
    try:
        # Ejecutar tests comprehensivos
        report = await tester.run_comprehensive_quality_test()
        
        # Guardar reporte
        tester.save_report(report)
        
        print("\n✅ Testing de calidad completado exitosamente!")
        
        return report
        
    except Exception as e:
        print(f"\n❌ Error durante testing: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(main())
