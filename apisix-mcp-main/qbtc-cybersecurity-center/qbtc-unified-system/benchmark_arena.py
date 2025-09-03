#!/usr/bin/env python3
"""
QBTC Benchmark Arena
Sistema de benchmarking para QBTC Quantum Consciousness System
Basado en el modelo de benchmark_arena.py original
"""

import requests
import json
import re
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

class QBTCGladiator:
    """
    Adaptador que presenta nuestro QBTC System como un gladiador 
    en la arena de benchmarks
    """
    
    def __init__(self, api_url="http://localhost:8000", quantum_url="http://localhost:8001"):
        self.api_url = api_url
        self.quantum_url = quantum_url
        self.session = requests.Session()
        self.test_results = []
    
    def predict(self, prompt: str, use_quantum=True) -> Dict[str, Any]:
        """
        Envia consulta al sistema QBTC y devuelve respuesta con métricas
        """
        start_time = time.time()
        
        if use_quantum:
            # Usar Quantum Core Service - puerto 8001
            payload = {
                "query": prompt,
                "temperature": 0.7,
                "max_tokens": 1024
            }
            endpoint = f"{self.quantum_url}/quantum/process"
        else:
            # Usar Python API Service - puerto 8000
            payload = {
                "query": prompt,
                "language": "python",
                "style": "functional"
            }
            endpoint = f"{self.api_url}/api/generate-code"
        
        try:
            response = self.session.post(endpoint, json=payload, timeout=60)
            response_time = time.time() - start_time
            
            response.raise_for_status()
            data = response.json()
            
            if use_quantum:
                response_text = data.get("response", "[SIN RESPUESTA]")
            else:
                response_text = data.get("code", data.get("response", "[SIN RESPUESTA]"))
            
            return {
                "response": response_text,
                "response_time": response_time,
                "status_code": response.status_code,
                "endpoint": "quantum" if use_quantum else "standard"
            }
            
        except requests.RequestException as e:
            return {
                "response": f"[ERROR DE CONEXIÓN: {e}]",
                "response_time": time.time() - start_time,
                "status_code": 0,
                "endpoint": "quantum" if use_quantum else "standard",
                "error": str(e)
            }
        except json.JSONDecodeError as e:
            return {
                "response": "[ERROR DE JSON EN RESPUESTA]",
                "response_time": time.time() - start_time,
                "status_code": response.status_code if 'response' in locals() else 0,
                "endpoint": "quantum" if use_quantum else "standard",
                "error": str(e)
            }

class QBTCBenchmarkArena:
    """
    Arena de benchmarks para el sistema QBTC
    """
    
    def __init__(self):
        self.gladiator = QBTCGladiator()
        self.test_questions = self._create_test_questions()
        self.results = []
    
    def _create_test_questions(self) -> List[Dict[str, Any]]:
        """
        Crea conjunto de preguntas de prueba para benchmark
        """
        return [
            {
                "category": "Matemáticas Básicas",
                "question": "¿Cuál es el resultado de 25 + 37?",
                "expected_answer": "62",
                "type": "calculation"
            },
            {
                "category": "Matemáticas Avanzadas", 
                "question": "Si tengo 120 manzanas y las reparto igualmente entre 8 personas, ¿cuántas manzanas recibe cada persona?",
                "expected_answer": "15",
                "type": "word_problem"
            },
            {
                "category": "Lógica",
                "question": "Si todos los gatos son animales y algunos animales son domésticos, ¿qué se puede concluir sobre los gatos?",
                "expected_answer": "algunos gatos pueden ser domésticos",
                "type": "logic"
            },
            {
                "category": "Conocimiento General",
                "question": "¿Cuál es la capital de Francia?",
                "expected_answer": "París",
                "type": "knowledge"
            },
            {
                "category": "Procesamiento de Texto",
                "question": "Extrae la palabra más larga de esta frase: 'El extraordinario desarrollo tecnológico'",
                "expected_answer": "extraordinario",
                "type": "text_processing"
            },
            {
                "category": "Razonamiento Cuántico",
                "question": "En un sistema cuántico, si un qubit está en superposición, ¿cuántos estados puede representar simultáneamente?",
                "expected_answer": "2",
                "type": "quantum_reasoning"
            },
            {
                "category": "Análisis de Datos",
                "question": "Si tengo los números 10, 15, 20, 25, 30, ¿cuál es la media aritmética?",
                "expected_answer": "20",
                "type": "data_analysis"
            },
            {
                "category": "Creatividad",
                "question": "Describe brevemente una aplicación innovadora de la inteligencia artificial",
                "expected_answer": "variable",
                "type": "creativity"
            }
        ]
    
    def extract_answer(self, text: str, question_type: str) -> str:
        """
        Extrae la respuesta del texto de manera robusta según el tipo de pregunta
        """
        text_str = str(text).lower().strip()
        
        if question_type in ["calculation", "word_problem", "data_analysis", "quantum_reasoning"]:
            # Para preguntas numéricas, extraer números
            text_clean = text_str.replace(',', '').replace('.', '')
            matches = re.findall(r'-?\d+', text_clean)
            if matches:
                return matches[-1]  # Último número encontrado
            
        elif question_type == "knowledge":
            # Para conocimiento general, buscar palabras clave
            if "parís" in text_str or "paris" in text_str:
                return "París"
                
        elif question_type == "text_processing":
            # Buscar la palabra más larga mencionada
            words = re.findall(r'\w+', text_str)
            if words:
                longest = max(words, key=len)
                if len(longest) > 8:  # "extraordinario" tiene 13 letras
                    return longest
                    
        elif question_type == "logic":
            # Para lógica, buscar conceptos relacionados
            if any(word in text_str for word in ["algunos", "pueden", "domésticos", "posible"]):
                return "algunos gatos pueden ser domésticos"
        
        elif question_type == "creativity":
            # Para creatividad, si hay una respuesta coherente > 20 caracteres
            if len(text_str) > 20 and any(word in text_str for word in ["aplicación", "innovadora", "inteligencia", "artificial"]):
                return "respuesta_creativa_válida"
        
        return text_str[:50]  # Primeros 50 caracteres como fallback
    
    def calculate_accuracy(self, predictions: List[str], expected: List[str], types: List[str]) -> Dict[str, float]:
        """
        Calcula accuracy general y por categoría
        """
        total_correct = 0
        category_stats = {}
        
        for i, (pred, exp, qtype) in enumerate(zip(predictions, expected, types)):
            is_correct = False
            
            if exp == "variable":  # Para preguntas de creatividad
                is_correct = len(pred) > 10  # Respuesta mínimamente elaborada
            else:
                # Comparación flexible
                pred_clean = str(pred).lower().strip()
                exp_clean = str(exp).lower().strip()
                is_correct = pred_clean == exp_clean or exp_clean in pred_clean
            
            if is_correct:
                total_correct += 1
            
            # Estadísticas por categoría
            category = self.test_questions[i]["category"]
            if category not in category_stats:
                category_stats[category] = {"correct": 0, "total": 0}
            category_stats[category]["total"] += 1
            if is_correct:
                category_stats[category]["correct"] += 1
        
        # Calcular accuracy por categoría
        category_accuracy = {}
        for cat, stats in category_stats.items():
            category_accuracy[cat] = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        
        return {
            "overall_accuracy": total_correct / len(predictions) if predictions else 0,
            "category_accuracy": category_accuracy,
            "total_questions": len(predictions),
            "total_correct": total_correct
        }
    
    async def run_benchmark(self, use_quantum=True) -> Dict[str, Any]:
        """
        Ejecuta el benchmark completo
        """
        print("\n" + "="*60)
        print("QBTC BENCHMARK ARENA")
        print("="*60)
        print(f"Iniciando benchmark con {'Quantum Core' if use_quantum else 'Standard API'}")
        print(f"Preguntas de prueba: {len(self.test_questions)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        predictions = []
        response_times = []
        detailed_results = []
        
        print("Ejecutando pruebas...")
        for i, question_data in enumerate(tqdm(self.test_questions, desc="Procesando preguntas")):
            question = question_data["question"]
            expected = question_data["expected_answer"]
            qtype = question_data["type"]
            category = question_data["category"]
            
            # Hacer predicción
            result = self.gladiator.predict(question, use_quantum=use_quantum)
            
            # Procesar respuesta
            response_text = result["response"]
            response_time = result["response_time"]
            
            # Extraer respuesta limpia
            clean_answer = self.extract_answer(response_text, qtype)
            
            predictions.append(clean_answer)
            response_times.append(response_time)
            
            detailed_results.append({
                "question_id": i + 1,
                "category": category,
                "question": question,
                "expected_answer": expected,
                "raw_response": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                "extracted_answer": clean_answer,
                "response_time": response_time,
                "endpoint": result["endpoint"],
                "status_code": result.get("status_code", 0)
            })
        
        # Calcular métricas
        expected_answers = [q["expected_answer"] for q in self.test_questions]
        question_types = [q["type"] for q in self.test_questions]
        
        accuracy_results = self.calculate_accuracy(predictions, expected_answers, question_types)
        
        # Estadísticas de rendimiento
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        benchmark_results = {
            "benchmark_info": {
                "timestamp": datetime.now().isoformat(),
                "endpoint_used": "quantum" if use_quantum else "standard",
                "total_questions": len(self.test_questions),
                "test_duration": sum(response_times)
            },
            "accuracy_metrics": accuracy_results,
            "performance_metrics": {
                "avg_response_time": avg_response_time,
                "min_response_time": min_response_time,
                "max_response_time": max_response_time,
                "total_response_time": sum(response_times)
            },
            "detailed_results": detailed_results
        }
        
        # Mostrar resultados
        self._display_results(benchmark_results)
        
        # Guardar resultados
        self._save_results(benchmark_results)
        
        return benchmark_results
    
    def _display_results(self, results: Dict[str, Any]):
        """
        Muestra los resultados del benchmark de manera elegante
        """
        print("\n" + "="*60)
        print("RESULTADOS DEL BENCHMARK")
        print("="*60)
        
        # Información general
        info = results["benchmark_info"]
        print(f"Endpoint utilizado: {info['endpoint_used'].upper()}")
        print(f"Total de preguntas: {info['total_questions']}")
        print(f"Duración total: {info['test_duration']:.2f}s")
        print()
        
        # Métricas de accuracy
        acc = results["accuracy_metrics"]
        print("MÉTRICAS DE PRECISIÓN:")
        print(f"  Accuracy General: {acc['overall_accuracy']:.2%} ({acc['total_correct']}/{acc['total_questions']})")
        print()
        print("  Accuracy por Categoría:")
        for category, accuracy in acc["category_accuracy"].items():
            print(f"    {category}: {accuracy:.2%}")
        print()
        
        # Métricas de rendimiento
        perf = results["performance_metrics"]
        print("MÉTRICAS DE RENDIMIENTO:")
        print(f"  Tiempo promedio de respuesta: {perf['avg_response_time']:.2f}s")
        print(f"  Tiempo mínimo: {perf['min_response_time']:.2f}s")
        print(f"  Tiempo máximo: {perf['max_response_time']:.2f}s")
        print()
        
        # Análisis detallado de las primeras 3 preguntas
        print("ANÁLISIS DETALLADO (Primeros 3 casos):")
        print("-" * 60)
        for i, result in enumerate(results["detailed_results"][:3]):
            print(f"[{result['question_id']}] {result['category']}")
            print(f"  Pregunta: {result['question']}")
            print(f"  Esperado: {result['expected_answer']}")
            print(f"  Extraído: {result['extracted_answer']}")
            print(f"  Tiempo: {result['response_time']:.2f}s")
            print(f"  Respuesta completa: {result['raw_response'][:100]}...")
            print("-" * 40)
        
        print("\n" + "="*60)
    
    def _save_results(self, results: Dict[str, Any]):
        """
        Guarda los resultados en archivo JSON
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        endpoint = results["benchmark_info"]["endpoint_used"]
        filename = f"benchmark_results_{endpoint}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados guardados en: {filename}")

async def run_qbtc_benchmark():
    """
    Función principal para ejecutar el benchmark
    """
    arena = QBTCBenchmarkArena()
    
    print("QBTC Benchmark Arena - Sistema de Pruebas")
    print("Probando capacidades del sistema QBTC...")
    
    # Ejecutar con Quantum Core
    print("\n[1/2] Ejecutando benchmark con Quantum Core...")
    quantum_results = await arena.run_benchmark(use_quantum=True)
    
    # Ejecutar con API estándar
    print("\n[2/2] Ejecutando benchmark con API estándar...")
    standard_results = await arena.run_benchmark(use_quantum=False)
    
    # Comparación de resultados
    print("\n" + "="*60)
    print("COMPARACIÓN DE RESULTADOS")
    print("="*60)
    
    quantum_acc = quantum_results["accuracy_metrics"]["overall_accuracy"]
    standard_acc = standard_results["accuracy_metrics"]["overall_accuracy"]
    quantum_time = quantum_results["performance_metrics"]["avg_response_time"]
    standard_time = standard_results["performance_metrics"]["avg_response_time"]
    
    print(f"Quantum Core  - Accuracy: {quantum_acc:.2%}, Tiempo avg: {quantum_time:.2f}s")
    print(f"Standard API  - Accuracy: {standard_acc:.2%}, Tiempo avg: {standard_time:.2f}s")
    print()
    
    if quantum_acc > standard_acc:
        print("GANADOR (Accuracy): Quantum Core")
    elif standard_acc > quantum_acc:
        print("GANADOR (Accuracy): Standard API")
    else:
        print("EMPATE en Accuracy")
    
    if quantum_time < standard_time:
        print("GANADOR (Velocidad): Quantum Core")
    elif standard_time < quantum_time:
        print("GANADOR (Velocidad): Standard API")
    else:
        print("EMPATE en Velocidad")
    
    print("\nBenchmark completado exitosamente!")
    return quantum_results, standard_results

if __name__ == "__main__":
    asyncio.run(run_qbtc_benchmark())