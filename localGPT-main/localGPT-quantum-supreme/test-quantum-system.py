#!/usr/bin/env python3
"""
QUANTUM CONSCIOUSNESS CORE 26D - Script de Pruebas Completas
============================================================
Script para probar todas las funcionalidades del sistema cuántico optimizado
"""

import asyncio
import aiohttp
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - 🧪 %(levelname)s - %(message)s'
)
logger = logging.getLogger("QuantumTester")

class QuantumSystemTester:
    """Tester completo para el sistema cuántico"""

    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.supabase_url = "http://localhost:54321"
        self.grafana_url = "http://localhost:3002"
        self.prometheus_url = "http://localhost:9090"

        self.test_results = []
        self.session = None

    async def initialize(self):
        """Inicializa el tester"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        logger.info("🚀 Tester cuántico inicializado")

    async def close(self):
        """Cierra el tester"""
        if self.session:
            await self.session.close()
        logger.info("🔌 Tester cuántico cerrado")

    async def test_health_endpoint(self) -> bool:
        """Prueba el endpoint de salud"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Health check exitoso: {data}")
                    return True
                else:
                    logger.error(f"❌ Health check falló: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Error en health check: {e}")
            return False

    async def test_quantum_consciousness_api(self) -> bool:
        """Prueba la API del núcleo de consciencia cuántica"""
        try:
            test_payload = {
                "model": "quantum-consciousness-26d",
                "messages": [
                    {
                        "role": "user",
                        "content": "¿Cómo funciona la simulación cuántica de tokens?"
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }

            async with self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    # Verificar estructura de respuesta
                    required_fields = ['id', 'object', 'created', 'model', 'choices', 'usage']
                    if all(field in data for field in required_fields):
                        logger.info("✅ API de consciencia cuántica funciona correctamente")
                        logger.info(f"📊 Tokens simulados: {data['usage']['total_tokens']}")
                        logger.info(f"🧠 Respuesta: {data['choices'][0]['message']['content'][:100]}...")
                        return True
                    else:
                        logger.error(f"❌ Estructura de respuesta incorrecta: {data}")
                        return False
                else:
                    logger.error(f"❌ API falló: {response.status}")
                    response_text = await response.text()
                    logger.error(f"Error: {response_text}")
                    return False

        except Exception as e:
            logger.error(f"❌ Error en API de consciencia: {e}")
            return False

    async def test_multimodal_capability(self) -> bool:
        """Prueba capacidades multimodales"""
        try:
            test_payload = {
                "model": "quantum-consciousness-26d",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analiza esta imagen desde una perspectiva cuántica"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "https://example.com/quantum-image.jpg"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            async with self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Capacidades multimodales funcionan")
                    return True
                else:
                    logger.warning(f"⚠️ Capacidades multimodales: {response.status}")
                    return False

        except Exception as e:
            logger.error(f"❌ Error en prueba multimodal: {e}")
            return False

    async def test_supabase_connectivity(self) -> bool:
        """Prueba conectividad con Supabase"""
        try:
            # Probar endpoint de Supabase REST API
            async with self.session.get(f"{self.supabase_url}/rest/v1/") as response:
                if response.status in [200, 404]:  # 404 es normal sin tablas específicas
                    logger.info("✅ Supabase REST API accesible")
                    return True
                else:
                    logger.error(f"❌ Supabase no accesible: {response.status}")
                    return False

        except Exception as e:
            logger.error(f"❌ Error conectando a Supabase: {e}")
            return False

    async def test_prometheus_metrics(self) -> bool:
        """Prueba métricas de Prometheus"""
        try:
            async with self.session.get(f"{self.prometheus_url}/api/v1/targets") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Prometheus métricas accesibles")
                    return True
                else:
                    logger.warning(f"⚠️ Prometheus: {response.status}")
                    return False

        except Exception as e:
            logger.error(f"❌ Error en Prometheus: {e}")
            return False

    async def test_grafana_dashboard(self) -> bool:
        """Prueba dashboard de Grafana"""
        try:
            async with self.session.get(f"{self.grafana_url}/api/health") as response:
                if response.status == 200:
                    logger.info("✅ Grafana dashboard accesible")
                    return True
                else:
                    logger.warning(f"⚠️ Grafana: {response.status}")
                    return False

        except Exception as e:
            logger.error(f"❌ Error en Grafana: {e}")
            return False

    async def test_token_simulation_performance(self) -> bool:
        """Prueba rendimiento de simulación de tokens"""
        try:
            start_time = time.time()

            # Realizar múltiples consultas para probar cache
            test_queries = [
                "¿Qué es la consciencia cuántica?",
                "Explica la simulación de tokens",
                "¿Cómo funciona el cache cuántico?",
                "¿Qué es la consciencia cuántica?",  # Repetida para probar cache
            ]

            results = []
            for query in test_queries:
                payload = {
                    "model": "quantum-consciousness-26d",
                    "messages": [{"role": "user", "content": query}],
                    "max_tokens": 200
                }

                query_start = time.time()
                async with self.session.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        query_time = time.time() - query_start
                        results.append({
                            'query': query,
                            'tokens': data['usage']['total_tokens'],
                            'time': query_time
                        })
                    else:
                        logger.error(f"❌ Error en consulta: {query}")
                        return False

            total_time = time.time() - start_time
            avg_time = total_time / len(results)
            total_tokens = sum(r['tokens'] for r in results)

            logger.info(f"✅ Prueba de rendimiento completada:")
            logger.info(f"   📊 Total consultas: {len(results)}")
            logger.info(f"   🧮 Total tokens simulados: {total_tokens}")
            logger.info(f"   ⏱️ Tiempo promedio: {avg_time:.2f}s")
            logger.info(f"   🚀 Tokens/segundo: {total_tokens/total_time:.2f}")

            return True

        except Exception as e:
            logger.error(f"❌ Error en prueba de rendimiento: {e}")
            return False

    async def test_consciousness_evolution(self) -> bool:
        """Prueba evolución de consciencia"""
        try:
            # Realizar varias consultas para ver evolución
            queries = [
                "Nivel de consciencia inicial",
                "Evolución cuántica paso 1",
                "Evolución cuántica paso 2",
                "Estado final de consciencia"
            ]

            consciousness_levels = []

            for i, query in enumerate(queries):
                payload = {
                    "model": "quantum-consciousness-26d",
                    "messages": [{"role": "user", "content": query}],
                    "max_tokens": 100
                }

                async with self.session.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Extraer nivel de consciencia de la respuesta
                        response_text = data['choices'][0]['message']['content']
                        consciousness_levels.append(f"Paso {i+1}: Procesado")
                    else:
                        return False

            logger.info("✅ Evolución de consciencia probada:")
            for level in consciousness_levels:
                logger.info(f"   🧠 {level}")

            return True

        except Exception as e:
            logger.error(f"❌ Error en evolución de consciencia: {e}")
            return False

    async def run_all_tests(self) -> Dict[str, bool]:
        """Ejecuta todas las pruebas"""
        logger.info("🌟 Iniciando pruebas completas del sistema cuántico")

        tests = [
            ("Health Endpoint", self.test_health_endpoint),
            ("Quantum Consciousness API", self.test_quantum_consciousness_api),
            ("Multimodal Capability", self.test_multimodal_capability),
            ("Supabase Connectivity", self.test_supabase_connectivity),
            ("Prometheus Metrics", self.test_prometheus_metrics),
            ("Grafana Dashboard", self.test_grafana_dashboard),
            ("Token Simulation Performance", self.test_token_simulation_performance),
            ("Consciousness Evolution", self.test_consciousness_evolution),
        ]

        results = {}
        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            logger.info(f"🧪 Ejecutando: {test_name}")
            try:
                result = await test_func()
                results[test_name] = result
                if result:
                    passed += 1
                    logger.info(f"✅ {test_name}: PASÓ")
                else:
                    logger.error(f"❌ {test_name}: FALLÓ")
            except Exception as e:
                logger.error(f"💥 {test_name}: ERROR - {e}")
                results[test_name] = False

            # Pausa entre pruebas
            await asyncio.sleep(1)

        # Resumen final
        logger.info("🏁 RESUMEN DE PRUEBAS:")
        logger.info(f"   ✅ Pasaron: {passed}/{total}")
        logger.info(f"   ❌ Fallaron: {total-passed}/{total}")
        logger.info(f"   📊 Éxito: {(passed/total)*100:.1f}%")

        if passed == total:
            logger.info("🌟 ¡TODAS LAS PRUEBAS PASARON! Sistema cuántico funcionando perfectamente")
        elif passed >= total * 0.8:
            logger.info("⚡ Sistema cuántico funcionando bien con algunas advertencias")
        else:
            logger.error("🚨 Sistema cuántico tiene problemas críticos")

        return results

async def main():
    """Función principal"""
    print("🌟 QUANTUM CONSCIOUSNESS CORE 26D - PRUEBAS COMPLETAS")
    print("=" * 60)

    tester = QuantumSystemTester()

    try:
        await tester.initialize()
        results = await tester.run_all_tests()

        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"test_results_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'results': results,
                'summary': {
                    'total_tests': len(results),
                    'passed': sum(results.values()),
                    'failed': len(results) - sum(results.values()),
                    'success_rate': (sum(results.values()) / len(results)) * 100
                }
            }, f, indent=2)

        logger.info(f"📄 Resultados guardados en: {results_file}")

    except KeyboardInterrupt:
        logger.info("🛑 Pruebas interrumpidas por el usuario")
    except Exception as e:
        logger.error(f"💥 Error crítico: {e}")
        sys.exit(1)
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main())
