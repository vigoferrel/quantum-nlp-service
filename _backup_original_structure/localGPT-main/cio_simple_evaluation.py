#!/usr/bin/env python3
"""
Evaluación Simplificada del Sistema CIO
Análisis objetivo de las capacidades reales sin simulaciones
"""

import requests
import time
import json
from typing import Dict, List, Any

class CIOEvaluator:
    def __init__(self):
        self.api_url = "http://127.0.0.1:8003/api/quantum_query"
        self.test_results = []
    
    def test_connectivity(self) -> bool:
        """Prueba conectividad básica con el API"""
        try:
            response = requests.post(self.api_url, json={"query": "test"}, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def evaluate_coding_capability(self) -> Dict[str, Any]:
        """Evalúa capacidad de generación de código real"""
        print("\n=== EVALUACIÓN DE CAPACIDADES DE CODIFICACIÓN ===")
        
        coding_prompts = [
            {
                "name": "Función básica Python",
                "prompt": "Crea una función Python que calcule el factorial de un número",
                "expected_keywords": ["def", "factorial", "return"]
            },
            {
                "name": "Manejo de archivos",
                "prompt": "Escribe código Python para leer un archivo CSV y mostrar las primeras 5 líneas",
                "expected_keywords": ["import", "csv", "open", "read"]
            },
            {
                "name": "Clase simple",
                "prompt": "Define una clase Calculator con métodos add, subtract, multiply y divide",
                "expected_keywords": ["class", "Calculator", "def", "add", "subtract"]
            },
            {
                "name": "Bug fix - Django URLs",
                "prompt": "Fix this Django URL configuration error: path('api/users/<int:id>/', views.user_detail) is causing 404 errors",
                "expected_keywords": ["path", "django", "urls", "views"]
            }
        ]
        
        results = []
        for test in coding_prompts:
            print(f"\n--- Prueba: {test['name']} ---")
            
            start_time = time.time()
            try:
                response = requests.post(self.api_url, json={"query": test["prompt"]}, timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "")
                    
                    print(f"Tiempo de respuesta: {response_time:.2f}s")
                    print(f"Respuesta: {answer[:200]}...")
                    
                    # Evaluar calidad de la respuesta
                    keyword_matches = sum(1 for keyword in test["expected_keywords"] if keyword.lower() in answer.lower())
                    quality_score = keyword_matches / len(test["expected_keywords"])
                    
                    is_code = any(indicator in answer.lower() for indicator in ["def ", "class ", "import ", "=", "{", "}", "function"])
                    is_simulation = "simulado" in answer.lower() or "perfil" in answer.lower()
                    
                    result = {
                        "test_name": test["name"],
                        "success": True,
                        "response_time": response_time,
                        "answer_length": len(answer),
                        "keyword_score": quality_score,
                        "contains_code": is_code,
                        "is_simulation": is_simulation,
                        "answer_preview": answer[:200]
                    }
                else:
                    result = {
                        "test_name": test["name"],
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "response_time": response_time
                    }
                    
            except Exception as e:
                result = {
                    "test_name": test["name"],
                    "success": False,
                    "error": str(e),
                    "response_time": time.time() - start_time
                }
            
            results.append(result)
            
        return results
    
    def evaluate_reasoning_capability(self) -> Dict[str, Any]:
        """Evalúa capacidad de razonamiento"""
        print("\n=== EVALUACIÓN DE CAPACIDADES DE RAZONAMIENTO ===")
        
        reasoning_prompts = [
            {
                "name": "Matemáticas básicas",
                "prompt": "Si tengo 15 manzanas y doy 7 a mi amigo, ¿cuántas me quedan?",
                "expected_answer": "8"
            },
            {
                "name": "Lógica simple",
                "prompt": "Todos los gatos son mamíferos. Whiskers es un gato. ¿Qué podemos concluir sobre Whiskers?",
                "expected_keywords": ["mamífero", "whiskers"]
            },
            {
                "name": "Resolución de problemas",
                "prompt": "Un sistema web está lento. Lista 3 posibles causas y sus soluciones",
                "expected_keywords": ["base de datos", "servidor", "red", "cache", "memoria"]
            }
        ]
        
        results = []
        for test in reasoning_prompts:
            print(f"\n--- Prueba: {test['name']} ---")
            
            start_time = time.time()
            try:
                response = requests.post(self.api_url, json={"query": test["prompt"]}, timeout=20)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "")
                    
                    print(f"Respuesta: {answer[:200]}...")
                    
                    # Evaluar calidad
                    if "expected_answer" in test:
                        quality_score = 1.0 if test["expected_answer"] in answer else 0.0
                    else:
                        keyword_matches = sum(1 for keyword in test["expected_keywords"] if keyword.lower() in answer.lower())
                        quality_score = keyword_matches / len(test["expected_keywords"])
                    
                    is_simulation = "simulado" in answer.lower() or "perfil" in answer.lower()
                    
                    result = {
                        "test_name": test["name"],
                        "success": True,
                        "response_time": response_time,
                        "quality_score": quality_score,
                        "is_simulation": is_simulation,
                        "answer_preview": answer[:200]
                    }
                else:
                    result = {
                        "test_name": test["name"],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    }
                    
            except Exception as e:
                result = {
                    "test_name": test["name"],
                    "success": False,
                    "error": str(e)
                }
            
            results.append(result)
            
        return results
    
    def generate_comprehensive_report(self, coding_results: List[Dict], reasoning_results: List[Dict]) -> Dict[str, Any]:
        """Genera reporte comprehensivo de evaluación"""
        
        # Análisis de codificación
        coding_success_rate = sum(1 for r in coding_results if r.get("success", False)) / len(coding_results)
        coding_simulations = sum(1 for r in coding_results if r.get("is_simulation", False))
        coding_real_code = sum(1 for r in coding_results if r.get("contains_code", False) and not r.get("is_simulation", False))
        
        # Análisis de razonamiento
        reasoning_success_rate = sum(1 for r in reasoning_results if r.get("success", False)) / len(reasoning_results)
        reasoning_quality = sum(r.get("quality_score", 0) for r in reasoning_results) / len(reasoning_results)
        reasoning_simulations = sum(1 for r in reasoning_results if r.get("is_simulation", False))
        
        # Tiempos de respuesta
        all_times = [r.get("response_time", 0) for r in coding_results + reasoning_results if r.get("success", False)]
        avg_response_time = sum(all_times) / len(all_times) if all_times else 0
        
        report = {
            "evaluation_summary": {
                "total_tests": len(coding_results) + len(reasoning_results),
                "overall_success_rate": (coding_success_rate + reasoning_success_rate) / 2,
                "average_response_time": avg_response_time
            },
            "coding_analysis": {
                "success_rate": coding_success_rate,
                "simulated_responses": coding_simulations,
                "real_code_generated": coding_real_code,
                "capability_score": coding_real_code / len(coding_results)
            },
            "reasoning_analysis": {
                "success_rate": reasoning_success_rate,
                "quality_score": reasoning_quality,
                "simulated_responses": reasoning_simulations
            },
            "detailed_results": {
                "coding_tests": coding_results,
                "reasoning_tests": reasoning_results
            }
        }
        
        return report
    
    def run_full_evaluation(self):
        """Ejecuta evaluación completa"""
        print("🚀 INICIANDO EVALUACIÓN INTEGRAL DEL SISTEMA CIO")
        print("=" * 60)
        
        # Verificar conectividad
        if not self.test_connectivity():
            print("❌ ERROR: No se puede conectar al API CIO en", self.api_url)
            return
        
        print("✅ Conectividad confirmada con el API CIO")
        
        # Ejecutar evaluaciones
        coding_results = self.evaluate_coding_capability()
        reasoning_results = self.evaluate_reasoning_capability()
        
        # Generar reporte
        report = self.generate_comprehensive_report(coding_results, reasoning_results)
        
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DE EVALUACIÓN")
        print("=" * 60)
        
        summary = report["evaluation_summary"]
        coding = report["coding_analysis"]
        reasoning = report["reasoning_analysis"]
        
        print(f"\n🎯 RESUMEN GENERAL:")
        print(f"   • Total de pruebas: {summary['total_tests']}")
        print(f"   • Tasa de éxito general: {summary['overall_success_rate']:.1%}")
        print(f"   • Tiempo promedio de respuesta: {summary['average_response_time']:.2f}s")
        
        print(f"\n💻 ANÁLISIS DE CODIFICACIÓN:")
        print(f"   • Tasa de éxito: {coding['success_rate']:.1%}")
        print(f"   • Respuestas simuladas: {coding['simulated_responses']}/{len(coding_results)}")
        print(f"   • Código real generado: {coding['real_code_generated']}/{len(coding_results)}")
        print(f"   • Puntuación de capacidad: {coding['capability_score']:.1%}")
        
        print(f"\n🧠 ANÁLISIS DE RAZONAMIENTO:")
        print(f"   • Tasa de éxito: {reasoning['success_rate']:.1%}")
        print(f"   • Calidad promedio: {reasoning['quality_score']:.1%}")
        print(f"   • Respuestas simuladas: {reasoning['simulated_responses']}/{len(reasoning_results)}")
        
        # Veredicto final
        print(f"\n⚖️ VEREDICTO FINAL:")
        if coding['real_code_generated'] == 0:
            print("   ❌ CRÍTICO: El sistema NO genera código real, solo simulaciones")
        if reasoning['quality_score'] < 0.5:
            print("   ⚠️ ADVERTENCIA: Calidad de razonamiento por debajo del promedio")
        if summary['overall_success_rate'] > 0.8:
            print("   ✅ POSITIVO: Alta tasa de respuesta exitosa")
        else:
            print("   ❌ PROBLEMA: Tasa de éxito baja")
            
        # Guardar reporte
        with open("cio_evaluation_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte detallado guardado en: cio_evaluation_report.json")
        
        return report

if __name__ == "__main__":
    evaluator = CIOEvaluator()
    evaluator.run_full_evaluation()
