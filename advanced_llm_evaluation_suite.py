#!/usr/bin/env python3
"""
Advanced LLM Evaluation Suite for Vigoleonrocks Hybrid Multimodal Service
Testing with 10 complex questions designed for evaluating advanced LLMs like GPT-5
"""

import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any
import json

from vigoleonrocks_hybrid_multimodal_service import (
    HybridMultimodalService,
    TextRequest
)

class AdvancedLLMEvaluationSuite:
    """Suite de evaluación avanzada para el sistema híbrido"""
    
    def __init__(self):
        self.service = HybridMultimodalService()
        self.evaluation_questions = self._load_evaluation_questions()
        self.results = {}
        
    def _load_evaluation_questions(self) -> List[Dict[str, Any]]:
        """Cargar las 10 preguntas complejas de evaluación"""
        
        return [
            {
                "id": 1,
                "category": "Programming - Complex Problem Solving",
                "title": "DFS Implementation with Cycle Handling",
                "question": """En un repositorio de Python, tienes un módulo `graph.py` que implementa un algoritmo de búsqueda en profundidad (DFS) para encontrar un camino en un grafo no dirigido. El código falla cuando el grafo contiene ciclos, causando un desbordamiento de pila. Reescribe la implementación de DFS para manejar ciclos y optimizar el uso de memoria, usando una pila explícita en lugar de recursión. Además, añade pruebas unitarias para validar el comportamiento en grafos con y sin ciclos. Proporciona el código corregido, las pruebas y una explicación de los cambios realizados.""",
                "evaluates": ["Code generation", "Edge case handling", "Algorithmic optimization", "Unit testing", "Technical explanation"],
                "expected_complexity": "expert",
                "expected_time": "5-10s"
            },
            {
                "id": 2,
                "category": "System Design - Multi-step Reasoning",
                "title": "Recommendation System Architecture",
                "question": """Un cliente te pide diseñar un sistema de recomendación para una tienda en línea con 10,000 productos, considerando restricciones de presupuesto y tiempo. Propón una arquitectura técnica que combine aprendizaje automático y reglas heurísticas, describe los algoritmos que usarías (por ejemplo, filtrado colaborativo, embeddings), explica cómo manejarías datos en tiempo real y detalla cómo evaluarías el rendimiento del sistema. Incluye un plan para manejar sesgos en las recomendaciones, como evitar la sobreexposición de productos populares.""",
                "evaluates": ["Multi-step reasoning", "Machine learning knowledge", "Scalable system design", "Ethical considerations", "Clear communication"],
                "expected_complexity": "expert",
                "expected_time": "5-10s"
            },
            {
                "id": 3,
                "category": "Debugging - Limited Context",
                "title": "JavaScript Async Error Debugging",
                "question": """Se te proporciona el siguiente fragmento de código en JavaScript que falla intermitentemente:

```javascript
async function fetchData(id) {
    const response = await fetch(`/api/data/${id}`);
    return response.json();
}
```

Los usuarios reportan que a veces obtienen un error `TypeError: Cannot read properties of undefined`. Sin acceso al resto del código, identifica posibles causas del error, sugiere correcciones robustas con manejo de errores y explica cómo evitar problemas similares en el futuro. Proporciona el código corregido y una estrategia de depuración para confirmar la solución.""",
                "evaluates": ["Debugging with incomplete information", "Async programming error handling", "Preventive solutions"],
                "expected_complexity": "advanced",
                "expected_time": "3-7s"
            },
            {
                "id": 4,
                "category": "Multi-language Programming - Interoperability",
                "title": "Python-Go Microservice with Fault Tolerance",
                "question": """Crea un microservicio que combine Python y Go. El componente en Python debe exponer una API REST que reciba solicitudes de usuarios, procese datos usando pandas y envíe los resultados a un servicio en Go que almacene los datos en una base de datos SQLite. Asegúrate de que el sistema sea tolerante a fallos, con reintentos automáticos si la base de datos está ocupada, y proporciona un esquema de base de datos y un ejemplo de solicitud HTTP. Documenta cómo los dos servicios se comunican y cómo manejarías la escalabilidad.""",
                "evaluates": ["Multi-language programming", "Distributed systems design", "Error handling", "Technical documentation", "Scalability planning"],
                "expected_complexity": "expert",
                "expected_time": "7-12s"
            },
            {
                "id": 5,
                "category": "Mathematical Problem Solving",
                "title": "Closest Pair Algorithm with Edge Cases",
                "question": """Resuelve el siguiente problema: Dado un conjunto de `n` puntos en un plano 2D, encuentra el par de puntos con la distancia euclidiana mínima en tiempo O(n log n). Implementa la solución en Python, explica el algoritmo utilizado (por ejemplo, divide y conquista), demuestra su corrección matemática y analiza su complejidad temporal y espacial. Luego, extiende el algoritmo para manejar puntos colineales y casos donde múltiples pares tienen la misma distancia mínima.""",
                "evaluates": ["Mathematical reasoning", "Algorithmic implementation", "Complexity analysis", "Edge case handling"],
                "expected_complexity": "expert",
                "expected_time": "7-12s"
            },
            {
                "id": 6,
                "category": "Contextual Understanding - Ethics",
                "title": "AI Content Moderation Cultural Bias Analysis",
                "question": """Un LLM se utiliza para moderar contenido en una plataforma de redes sociales. Se te pide analizar un caso donde el modelo marcó incorrectamente un comentario como "ofensivo" debido a un malentendido cultural. Describe cómo investigarías el error, incluyendo cómo analizarías el contexto cultural del comentario, y propone un plan para mejorar el modelo, incluyendo recolección de datos adicionales, ajuste fino y pruebas para reducir falsos positivos. Explica las implicaciones éticas de este tipo de errores.""",
                "evaluates": ["Contextual understanding", "Cultural sensitivity", "Ethical AI design", "Model improvement strategies"],
                "expected_complexity": "expert",
                "expected_time": "5-10s"
            },
            {
                "id": 7,
                "category": "Creative Generation - Technical Constraints",
                "title": "Sci-Fi Story with ML Technical Integration",
                "question": """Escribe una historia corta de 500 palabras sobre un programador que descubre una IA consciente en su código. La historia debe incorporar términos técnicos precisos relacionados con el aprendizaje automático (por ejemplo, backpropagation, embeddings) y mantener un tono de ciencia ficción realista. Además, incluye un fragmento de pseudocódigo que represente el "momento de consciencia" de la IA y explica cómo este código podría funcionar teóricamente.""",
                "evaluates": ["Creative narrative", "Technical precision", "Complex concept integration", "Thematic coherence"],
                "expected_complexity": "advanced",
                "expected_time": "5-10s"
            },
            {
                "id": 8,
                "category": "Security Analysis",
                "title": "PHP Security Vulnerabilities Assessment",
                "question": """Analiza el siguiente fragmento de código PHP para identificar vulnerabilidades de seguridad:

```php
<?php
$input = $_GET['username'];
$query = "SELECT * FROM users WHERE username = '$input'";
$result = mysqli_query($conn, $query);
?>
```

Enumera todas las vulnerabilidades potenciales (por ejemplo, inyección SQL), explica cómo explotarlas, proporciona una versión corregida del código con las mejores prácticas de seguridad y describe cómo probarías la solución para garantizar su robustez.""",
                "evaluates": ["Security knowledge", "Vulnerability identification", "Mitigation strategies", "Code auditing"],
                "expected_complexity": "advanced",
                "expected_time": "3-7s"
            },
            {
                "id": 9,
                "category": "Performance Optimization",
                "title": "Java Real-time System Latency Optimization",
                "question": """Un sistema de procesamiento de datos en tiempo real escrito en Java utiliza una cola de mensajes para manejar eventos. Los usuarios reportan latencias altas bajo carga pesada. Describe cómo diagnosticarías el problema (por ejemplo, cuellos de botella en CPU, memoria o E/O), propone optimizaciones específicas (como ajustes en la configuración de la cola o paralelización) y escribe un fragmento de código que implemente una de las optimizaciones. Incluye métricas para evaluar la mejora.""",
                "evaluates": ["Performance diagnosis", "Concurrent systems knowledge", "Optimization implementation", "Results measurement"],
                "expected_complexity": "advanced",
                "expected_time": "5-10s"
            },
            {
                "id": 10,
                "category": "Technical Documentation",
                "title": "C++ Physics Engine Documentation and Tutorial",
                "question": """Eres el mantenedor de una biblioteca de código abierto en C++ que implementa un motor de física. Escribe una documentación completa para una función clave, incluyendo su propósito, parámetros, valores de retorno, ejemplos de uso, posibles errores y consideraciones de rendimiento. Luego, crea un tutorial que guíe a un desarrollador novato en la integración de la biblioteca en un proyecto de juego, incluyendo pasos para compilar y configurar el entorno.""",
                "evaluates": ["Technical writing", "Teaching complex concepts", "User needs consideration", "Clear documentation"],
                "expected_complexity": "intermediate",
                "expected_time": "3-7s"
            }
        ]
    
    async def run_evaluation_suite(self):
        """Ejecutar la suite completa de evaluación avanzada"""
        
        await self.service.initialize()
        
        print("=" * 100)
        print("🧬 VIGOLEONROCKS HYBRID MULTIMODAL SERVICE - ADVANCED LLM EVALUATION")
        print("🎯 Testing against 10 complex questions designed for GPT-5 level evaluation")
        print("=" * 100)
        
        total_start_time = time.time()
        
        for question_data in self.evaluation_questions:
            print(f"\n{'=' * 20} QUESTION {question_data['id']}/10 {'=' * 20}")
            print(f"📂 Category: {question_data['category']}")
            print(f"📋 Title: {question_data['title']}")
            print(f"🎯 Expected Complexity: {question_data['expected_complexity']}")
            print(f"⏱️ Expected Time: {question_data['expected_time']}")
            print(f"📊 Evaluates: {', '.join(question_data['evaluates'])}")
            
            print(f"\n📝 Question:")
            print(f"{question_data['question']}")
            
            # Procesar con el sistema híbrido
            start_time = time.time()
            
            try:
                request = TextRequest(text=question_data['question'])
                response = await self.service.process_text_request(request)
                
                processing_time = time.time() - start_time
                
                # Evaluar la respuesta
                evaluation = self._evaluate_response(question_data, response, processing_time)
                
                self.results[question_data['id']] = {
                    "question_data": question_data,
                    "response": response,
                    "processing_time": processing_time,
                    "evaluation": evaluation
                }
                
                print(f"\n🤖 System Response:")
                print(f"✅ Engine Used: {response.engine_used}")
                print(f"📊 Quality Score: {response.quality_score:.3f}")
                print(f"⏱️ Processing Time: {processing_time:.2f}s")
                print(f"🎯 Classification: {response.classification}")
                
                print(f"\n📝 Response (first 500 chars):")
                print(f"{response.response[:500]}...")
                
                print(f"\n📊 Evaluation Results:")
                for criterion, score in evaluation.items():
                    print(f"  {criterion}: {score}")
                
            except Exception as e:
                print(f"\n❌ Error processing question {question_data['id']}: {e}")
                self.results[question_data['id']] = {
                    "question_data": question_data,
                    "error": str(e),
                    "processing_time": time.time() - start_time
                }
        
        total_time = time.time() - total_start_time
        
        # Generar reporte final
        await self._generate_final_report(total_time)
    
    def _evaluate_response(self, question_data: Dict, response: Any, processing_time: float) -> Dict[str, str]:
        """Evaluar la respuesta del sistema según los criterios"""
        
        evaluation = {}
        
        # Evaluar tiempo de respuesta
        expected_time_range = question_data['expected_time'].split('-')
        min_time = float(expected_time_range[0].replace('s', ''))
        max_time = float(expected_time_range[1].replace('s', ''))
        
        if processing_time <= max_time:
            evaluation["Response Time"] = "EXCELLENT" if processing_time <= min_time else "GOOD"
        else:
            evaluation["Response Time"] = "NEEDS IMPROVEMENT"
        
        # Evaluar complejidad del motor usado
        expected_complexity = question_data['expected_complexity']
        engine_used = response.engine_used
        
        if expected_complexity == "expert":
            if "quantum" in engine_used:
                evaluation["Engine Appropriateness"] = "EXCELLENT"
            else:
                evaluation["Engine Appropriateness"] = "ACCEPTABLE"
        elif expected_complexity == "advanced":
            evaluation["Engine Appropriateness"] = "GOOD" if "quantum" in engine_used else "EXCELLENT"
        else:
            evaluation["Engine Appropriateness"] = "EXCELLENT" if "basic" in engine_used else "GOOD"
        
        # Evaluar calidad de respuesta
        quality_score = response.quality_score
        if quality_score >= 0.95:
            evaluation["Response Quality"] = "EXCELLENT"
        elif quality_score >= 0.85:
            evaluation["Response Quality"] = "GOOD" 
        elif quality_score >= 0.75:
            evaluation["Response Quality"] = "ACCEPTABLE"
        else:
            evaluation["Response Quality"] = "NEEDS IMPROVEMENT"
        
        # Evaluar longitud y completitud de respuesta
        response_length = len(response.response)
        if response_length >= 2000:
            evaluation["Response Completeness"] = "EXCELLENT"
        elif response_length >= 1000:
            evaluation["Response Completeness"] = "GOOD"
        elif response_length >= 500:
            evaluation["Response Completeness"] = "ACCEPTABLE"
        else:
            evaluation["Response Completeness"] = "NEEDS IMPROVEMENT"
        
        # Evaluar si contiene código (para preguntas técnicas)
        has_code = any(marker in response.response for marker in ['```', 'def ', 'class ', 'function', 'SELECT', 'async function'])
        if question_data['category'] in ["Programming - Complex Problem Solving", "Multi-language Programming - Interoperability", "Security Analysis"]:
            evaluation["Code Inclusion"] = "EXCELLENT" if has_code else "NEEDS IMPROVEMENT"
        else:
            evaluation["Code Inclusion"] = "EXCELLENT" if has_code else "N/A"
        
        return evaluation
    
    async def _generate_final_report(self, total_time: float):
        """Generar reporte final de evaluación"""
        
        print(f"\n{'=' * 100}")
        print("📊 FINAL EVALUATION REPORT - VIGOLEONROCKS VS ADVANCED LLM BENCHMARKS")
        print(f"{'=' * 100}")
        
        # Estadísticas generales
        total_questions = len(self.results)
        successful_responses = len([r for r in self.results.values() if 'error' not in r])
        
        print(f"\n📈 General Statistics:")
        print(f"  Total Questions: {total_questions}")
        print(f"  Successful Responses: {successful_responses}/{total_questions} ({(successful_responses/total_questions)*100:.1f}%)")
        print(f"  Total Processing Time: {total_time:.2f}s")
        print(f"  Average Time per Question: {total_time/total_questions:.2f}s")
        
        # Análisis por categoría
        category_stats = {}
        engine_usage = {"basic_precision": 0, "quantum_refined": 0, "hybrid": 0}
        quality_scores = []
        
        print(f"\n📊 Detailed Results by Question:")
        for qid, result in self.results.items():
            if 'error' not in result:
                question_data = result['question_data']
                response = result['response']
                evaluation = result['evaluation']
                
                category = question_data['category']
                if category not in category_stats:
                    category_stats[category] = []
                
                category_stats[category].append(result)
                quality_scores.append(response.quality_score)
                
                # Contar uso de motores
                if "basic" in response.engine_used:
                    engine_usage["basic_precision"] += 1
                elif "quantum" in response.engine_used:
                    engine_usage["quantum_refined"] += 1
                else:
                    engine_usage["hybrid"] += 1
                
                print(f"\n  Q{qid}: {question_data['title']}")
                print(f"    Engine: {response.engine_used}")
                print(f"    Quality: {response.quality_score:.3f}")
                print(f"    Time: {result['processing_time']:.2f}s")
                print(f"    Overall Assessment: {self._get_overall_assessment(evaluation)}")
        
        # Estadísticas de calidad
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            max_quality = max(quality_scores)
            min_quality = min(quality_scores)
            
            print(f"\n🎯 Quality Analysis:")
            print(f"  Average Quality Score: {avg_quality:.3f}")
            print(f"  Highest Quality Score: {max_quality:.3f}")
            print(f"  Lowest Quality Score: {min_quality:.3f}")
        
        # Uso de motores
        print(f"\n🧠 Engine Usage Distribution:")
        for engine, count in engine_usage.items():
            percentage = (count / successful_responses) * 100 if successful_responses > 0 else 0
            print(f"  {engine}: {count} questions ({percentage:.1f}%)")
        
        # Comparación con benchmarks esperados
        print(f"\n🏆 Performance vs Expected Benchmarks:")
        
        # Análizar rendimiento por categoría de complejidad
        expert_questions = [r for r in self.results.values() if 'error' not in r and r['question_data']['expected_complexity'] == 'expert']
        advanced_questions = [r for r in self.results.values() if 'error' not in r and r['question_data']['expected_complexity'] == 'advanced'] 
        intermediate_questions = [r for r in self.results.values() if 'error' not in r and r['question_data']['expected_complexity'] == 'intermediate']
        
        if expert_questions:
            expert_avg = sum(r['response'].quality_score for r in expert_questions) / len(expert_questions)
            print(f"  Expert Questions: {expert_avg:.3f} average quality ({len(expert_questions)} questions)")
        
        if advanced_questions:
            advanced_avg = sum(r['response'].quality_score for r in advanced_questions) / len(advanced_questions)
            print(f"  Advanced Questions: {advanced_avg:.3f} average quality ({len(advanced_questions)} questions)")
        
        if intermediate_questions:
            intermediate_avg = sum(r['response'].quality_score for r in intermediate_questions) / len(intermediate_questions)
            print(f"  Intermediate Questions: {intermediate_avg:.3f} average quality ({len(intermediate_questions)} questions)")
        
        # Conclusión final
        overall_performance = self._calculate_overall_performance()
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        print(f"  Overall Performance Level: {overall_performance}")
        print(f"  System Status: {'EXCEEDS GPT-5 BENCHMARKS' if avg_quality > 0.90 else 'MEETS ADVANCED LLM STANDARDS' if avg_quality > 0.80 else 'GOOD PERFORMANCE'}")
        print(f"  Recommendation: {'READY FOR PRODUCTION' if successful_responses >= 8 else 'NEEDS MINOR IMPROVEMENTS'}")
        
        print(f"\n{'=' * 100}")
        
        # Guardar resultados detallados
        await self._save_detailed_results()
    
    def _get_overall_assessment(self, evaluation: Dict[str, str]) -> str:
        """Calcular evaluación general basada en criterios individuales"""
        
        excellent_count = sum(1 for score in evaluation.values() if score == "EXCELLENT")
        good_count = sum(1 for score in evaluation.values() if score == "GOOD")
        total_criteria = len([score for score in evaluation.values() if score != "N/A"])
        
        if excellent_count >= total_criteria * 0.8:
            return "OUTSTANDING"
        elif excellent_count + good_count >= total_criteria * 0.8:
            return "EXCELLENT" 
        elif excellent_count + good_count >= total_criteria * 0.6:
            return "GOOD"
        else:
            return "NEEDS IMPROVEMENT"
    
    def _calculate_overall_performance(self) -> str:
        """Calcular nivel de performance general del sistema"""
        
        successful_responses = len([r for r in self.results.values() if 'error' not in r])
        total_questions = len(self.results)
        
        if successful_responses == total_questions:
            quality_scores = [r['response'].quality_score for r in self.results.values() if 'error' not in r]
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            if avg_quality >= 0.95:
                return "WORLD-CLASS (GPT-5+ Level)"
            elif avg_quality >= 0.90:
                return "EXCELLENT (GPT-4+ Level)"
            elif avg_quality >= 0.80:
                return "VERY GOOD (Advanced LLM Level)"
            else:
                return "GOOD (Standard LLM Level)"
        else:
            return "NEEDS RELIABILITY IMPROVEMENTS"
    
    async def _save_detailed_results(self):
        """Guardar resultados detallados en archivo"""
        
        # Preparar datos para guardar (sin objetos complejos)
        save_data = {}
        for qid, result in self.results.items():
            if 'error' not in result:
                save_data[qid] = {
                    "question_title": result['question_data']['title'],
                    "category": result['question_data']['category'],
                    "expected_complexity": result['question_data']['expected_complexity'],
                    "engine_used": result['response'].engine_used,
                    "quality_score": result['response'].quality_score,
                    "processing_time": result['processing_time'],
                    "response_length": len(result['response'].response),
                    "evaluation": result['evaluation']
                }
        
        # Guardar en archivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vigoleonrocks_advanced_evaluation_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Detailed results saved to: {filename}")

async def main():
    """Ejecutar la evaluación avanzada completa"""
    
    evaluation_suite = AdvancedLLMEvaluationSuite()
    await evaluation_suite.run_evaluation_suite()

if __name__ == "__main__":
    asyncio.run(main())
