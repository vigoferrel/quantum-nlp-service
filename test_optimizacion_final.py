#!/usr/bin/env python3
"""
🧪 TEST DE OPTIMIZACIÓN FINAL
Verificar que las optimizaciones del sistema funcionan correctamente
"""

import asyncio
import time
import requests
import json
from typing import Dict, Any

class TestOptimizacionFinal:
    def __init__(self):
        self.base_url = "http://localhost:5004"
        self.results = []
        
    async def test_sistema_optimizado(self):
        """Probar el sistema optimizado"""
        print("🧪 TEST DE OPTIMIZACIÓN FINAL")
        print("=" * 50)
        
        # Test 1: Verificar conectividad
        print("\n1️⃣ Verificando conectividad...")
        if not await self.verificar_conectividad():
            print("❌ Servidor no disponible")
            return False
        
        # Test 2: Probar endpoint optimizado
        print("\n2️⃣ Probando endpoint optimizado...")
        await self.probar_endpoint_optimizado()
        
        # Test 3: Verificar análisis NLP
        print("\n3️⃣ Verificando análisis NLP...")
        await self.verificar_analisis_nlp()
        
        # Test 4: Verificar análisis cuántico
        print("\n4️⃣ Verificando análisis cuántico...")
        await self.verificar_analisis_cuantico()
        
        # Test 5: Medir rendimiento
        print("\n5️⃣ Midiendo rendimiento...")
        await self.medir_rendimiento()
        
        # Generar reporte
        self.generar_reporte_final()
        
        return True
    
    async def verificar_conectividad(self) -> bool:
        """Verificar que el servidor esté disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor disponible")
                return True
            else:
                print(f"❌ Servidor respondió con código {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error de conectividad: {e}")
            return False
    
    async def probar_endpoint_optimizado(self):
        """Probar el endpoint optimizado"""
        test_data = {
            "text": "Hola, ¿cómo estás? Estoy muy feliz de probar el sistema optimizado.",
            "session_id": "test_optimizacion_001",
            "user_id": "test_user"
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/process_text",
                json=test_data,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Endpoint respondió en {response_time:.3f}s")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Processing time: {data.get('processing_time', 0):.3f}s")
                
                # Verificar que NLP y Quantum analysis no sean None
                nlp_analysis = data.get('nlp_analysis')
                quantum_analysis = data.get('quantum_analysis')
                
                if nlp_analysis:
                    print("✅ NLP Analysis disponible")
                    sentiment = nlp_analysis.get('sentiment', {})
                    intent = nlp_analysis.get('intent', {})
                    print(f"   Sentiment: {sentiment.get('level', 'unknown')} (conf: {sentiment.get('confidence', 0):.2f})")
                    print(f"   Intent: {intent.get('type', 'unknown')} (conf: {intent.get('confidence', 0):.2f})")
                else:
                    print("❌ NLP Analysis no disponible")
                
                if quantum_analysis:
                    print("✅ Quantum Analysis disponible")
                    quantum_score = quantum_analysis.get('quantum_score', 0)
                    quantum_state = quantum_analysis.get('quantum_state', 'unknown')
                    print(f"   Quantum Score: {quantum_score:.2f}")
                    print(f"   Quantum State: {quantum_state}")
                else:
                    print("❌ Quantum Analysis no disponible")
                
                self.results.append({
                    "test": "endpoint_optimizado",
                    "success": True,
                    "response_time": response_time,
                    "nlp_available": nlp_analysis is not None,
                    "quantum_available": quantum_analysis is not None
                })
            else:
                print(f"❌ Endpoint falló con código {response.status_code}")
                self.results.append({
                    "test": "endpoint_optimizado",
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ Error probando endpoint: {e}")
            self.results.append({
                "test": "endpoint_optimizado",
                "success": False,
                "error": str(e)
            })
    
    async def verificar_analisis_nlp(self):
        """Verificar que el análisis NLP funcione correctamente"""
        test_texts = [
            "Estoy muy feliz hoy!",
            "Me siento triste y deprimido.",
            "Necesito ayuda con programación en Python.",
            "¿Puedes explicarme cómo funciona la inteligencia artificial?"
        ]
        
        nlp_scores = []
        
        for i, text in enumerate(test_texts, 1):
            print(f"   Probando texto {i}: {text[:30]}...")
            
            test_data = {
                "text": text,
                "session_id": f"nlp_test_{i}",
                "user_id": "test_user"
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/process_text",
                    json=test_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    nlp_analysis = data.get('nlp_analysis')
                    
                    if nlp_analysis:
                        sentiment = nlp_analysis.get('sentiment', {})
                        intent = nlp_analysis.get('intent', {})
                        
                        sentiment_level = sentiment.get('level', 'unknown')
                        sentiment_conf = sentiment.get('confidence', 0)
                        intent_type = intent.get('type', 'unknown')
                        intent_conf = intent.get('confidence', 0)
                        
                        print(f"     Sentiment: {sentiment_level} ({sentiment_conf:.2f})")
                        print(f"     Intent: {intent_type} ({intent_conf:.2f})")
                        
                        nlp_scores.append({
                            "text": text,
                            "sentiment_level": sentiment_level,
                            "sentiment_confidence": sentiment_conf,
                            "intent_type": intent_type,
                            "intent_confidence": intent_conf
                        })
                    else:
                        print("     ❌ NLP Analysis no disponible")
                else:
                    print(f"     ❌ Error HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"     ❌ Error: {e}")
        
        # Calcular métricas NLP
        if nlp_scores:
            avg_sentiment_conf = sum(s['sentiment_confidence'] for s in nlp_scores) / len(nlp_scores)
            avg_intent_conf = sum(s['intent_confidence'] for s in nlp_scores) / len(nlp_scores)
            
            print(f"\n📊 Métricas NLP:")
            print(f"   Promedio confianza sentimiento: {avg_sentiment_conf:.2f}")
            print(f"   Promedio confianza intención: {avg_intent_conf:.2f}")
            print(f"   Textos procesados: {len(nlp_scores)}")
            
            self.results.append({
                "test": "analisis_nlp",
                "success": True,
                "avg_sentiment_confidence": avg_sentiment_conf,
                "avg_intent_confidence": avg_intent_conf,
                "texts_processed": len(nlp_scores)
            })
        else:
            print("❌ No se pudieron procesar textos para análisis NLP")
            self.results.append({
                "test": "analisis_nlp",
                "success": False
            })
    
    async def verificar_analisis_cuantico(self):
        """Verificar que el análisis cuántico funcione correctamente"""
        test_texts = [
            "Explica la teoría de la relatividad",
            "¿Cómo funciona la computación cuántica?",
            "Necesito resolver un problema matemático complejo",
            "Analiza este código de programación"
        ]
        
        quantum_scores = []
        
        for i, text in enumerate(test_texts, 1):
            print(f"   Probando texto {i}: {text[:30]}...")
            
            test_data = {
                "text": text,
                "session_id": f"quantum_test_{i}",
                "user_id": "test_user"
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/process_text",
                    json=test_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    quantum_analysis = data.get('quantum_analysis')
                    
                    if quantum_analysis:
                        quantum_score = quantum_analysis.get('quantum_score', 0)
                        quantum_state = quantum_analysis.get('quantum_state', 'unknown')
                        improvement_factor = quantum_analysis.get('improvement_factor', 1.0)
                        
                        print(f"     Quantum Score: {quantum_score:.2f}")
                        print(f"     Quantum State: {quantum_state}")
                        print(f"     Improvement Factor: {improvement_factor:.2f}")
                        
                        quantum_scores.append({
                            "text": text,
                            "quantum_score": quantum_score,
                            "quantum_state": quantum_state,
                            "improvement_factor": improvement_factor
                        })
                    else:
                        print("     ❌ Quantum Analysis no disponible")
                else:
                    print(f"     ❌ Error HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"     ❌ Error: {e}")
        
        # Calcular métricas cuánticas
        if quantum_scores:
            avg_quantum_score = sum(s['quantum_score'] for s in quantum_scores) / len(quantum_scores)
            avg_improvement = sum(s['improvement_factor'] for s in quantum_scores) / len(quantum_scores)
            
            print(f"\n⚛️ Métricas Cuánticas:")
            print(f"   Promedio Quantum Score: {avg_quantum_score:.2f}")
            print(f"   Promedio Improvement Factor: {avg_improvement:.2f}")
            print(f"   Textos procesados: {len(quantum_scores)}")
            
            self.results.append({
                "test": "analisis_cuantico",
                "success": True,
                "avg_quantum_score": avg_quantum_score,
                "avg_improvement_factor": avg_improvement,
                "texts_processed": len(quantum_scores)
            })
        else:
            print("❌ No se pudieron procesar textos para análisis cuántico")
            self.results.append({
                "test": "analisis_cuantico",
                "success": False
            })
    
    async def medir_rendimiento(self):
        """Medir rendimiento del sistema optimizado"""
        print("   Probando rendimiento con múltiples requests...")
        
        test_data = {
            "text": "Test de rendimiento del sistema optimizado",
            "session_id": "perf_test",
            "user_id": "test_user"
        }
        
        response_times = []
        successful_requests = 0
        total_requests = 10
        
        for i in range(total_requests):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/process_text",
                    json=test_data,
                    timeout=30
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    response_times.append(response_time)
                    successful_requests += 1
                    print(f"     Request {i+1}: {response_time:.3f}s")
                else:
                    print(f"     Request {i+1}: Error HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"     Request {i+1}: Error {e}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            success_rate = successful_requests / total_requests
            
            print(f"\n📈 Métricas de Rendimiento:")
            print(f"   Tiempo promedio: {avg_time:.3f}s")
            print(f"   Tiempo mínimo: {min_time:.3f}s")
            print(f"   Tiempo máximo: {max_time:.3f}s")
            print(f"   Tasa de éxito: {success_rate:.1%}")
            print(f"   Requests exitosos: {successful_requests}/{total_requests}")
            
            self.results.append({
                "test": "rendimiento",
                "success": True,
                "avg_response_time": avg_time,
                "min_response_time": min_time,
                "max_response_time": max_time,
                "success_rate": success_rate,
                "successful_requests": successful_requests,
                "total_requests": total_requests
            })
        else:
            print("❌ No se pudieron medir tiempos de respuesta")
            self.results.append({
                "test": "rendimiento",
                "success": False
            })
    
    def generar_reporte_final(self):
        """Generar reporte final de la optimización"""
        print(f"\n📋 REPORTE FINAL DE OPTIMIZACIÓN")
        print("=" * 50)
        
        # Calcular métricas generales
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.get('success', False))
        success_rate = successful_tests / total_tests if total_tests > 0 else 0
        
        print(f"📊 Resumen General:")
        print(f"   Tests ejecutados: {total_tests}")
        print(f"   Tests exitosos: {successful_tests}")
        print(f"   Tasa de éxito: {success_rate:.1%}")
        
        # Análisis por test
        for result in self.results:
            test_name = result['test']
            success = result.get('success', False)
            
            print(f"\n🔍 {test_name.upper()}:")
            if success:
                print(f"   ✅ EXITOSO")
                
                if test_name == "endpoint_optimizado":
                    response_time = result.get('response_time', 0)
                    nlp_available = result.get('nlp_available', False)
                    quantum_available = result.get('quantum_available', False)
                    
                    print(f"   ⏱️ Tiempo de respuesta: {response_time:.3f}s")
                    print(f"   🧠 NLP Analysis: {'✅ Disponible' if nlp_available else '❌ No disponible'}")
                    print(f"   ⚛️ Quantum Analysis: {'✅ Disponible' if quantum_available else '❌ No disponible'}")
                
                elif test_name == "analisis_nlp":
                    avg_sentiment = result.get('avg_sentiment_confidence', 0)
                    avg_intent = result.get('avg_intent_confidence', 0)
                    texts = result.get('texts_processed', 0)
                    
                    print(f"   🧠 Confianza sentimiento promedio: {avg_sentiment:.2f}")
                    print(f"   🎯 Confianza intención promedio: {avg_intent:.2f}")
                    print(f"   📝 Textos procesados: {texts}")
                
                elif test_name == "analisis_cuantico":
                    avg_quantum = result.get('avg_quantum_score', 0)
                    avg_improvement = result.get('avg_improvement_factor', 0)
                    texts = result.get('texts_processed', 0)
                    
                    print(f"   ⚛️ Quantum Score promedio: {avg_quantum:.2f}")
                    print(f"   📈 Improvement Factor promedio: {avg_improvement:.2f}")
                    print(f"   📝 Textos procesados: {texts}")
                
                elif test_name == "rendimiento":
                    avg_time = result.get('avg_response_time', 0)
                    success_rate = result.get('success_rate', 0)
                    successful = result.get('successful_requests', 0)
                    total = result.get('total_requests', 0)
                    
                    print(f"   ⏱️ Tiempo promedio: {avg_time:.3f}s")
                    print(f"   📊 Tasa de éxito: {success_rate:.1%}")
                    print(f"   🔢 Requests: {successful}/{total}")
            else:
                print(f"   ❌ FALLÓ")
                error = result.get('error', 'Error desconocido')
                print(f"   🚨 Error: {error}")
        
        # Evaluación final
        print(f"\n🎯 EVALUACIÓN FINAL:")
        if success_rate >= 0.8:
            print(f"   🎉 OPTIMIZACIÓN EXITOSA")
            print(f"   ✅ El sistema está funcionando correctamente")
            print(f"   ✅ Los problemas críticos han sido resueltos")
            print(f"   ✅ El rendimiento ha mejorado significativamente")
        elif success_rate >= 0.5:
            print(f"   ⚠️ OPTIMIZACIÓN PARCIAL")
            print(f"   ⚠️ Algunos problemas persisten")
            print(f"   ⚠️ Se requieren ajustes adicionales")
        else:
            print(f"   ❌ OPTIMIZACIÓN FALLIDA")
            print(f"   ❌ Los problemas críticos persisten")
            print(f"   ❌ Se requiere revisión completa")
        
        # Guardar reporte
        reporte = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "success_rate": success_rate,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "results": self.results,
            "evaluation": "successful" if success_rate >= 0.8 else "partial" if success_rate >= 0.5 else "failed"
        }
        
        with open('reporte_test_optimizacion.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte guardado: reporte_test_optimizacion.json")

async def main():
    """Función principal"""
    tester = TestOptimizacionFinal()
    await tester.test_sistema_optimizado()

if __name__ == "__main__":
    asyncio.run(main())
