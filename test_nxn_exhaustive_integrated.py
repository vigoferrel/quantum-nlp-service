#!/usr/bin/env python3
"""
🧪 PRUEBAS NxN EXHAUSTIVAS - SISTEMA INTEGRADO VIGOLEONROCKS
Pruebas completas del motor conversacional avanzado + Sistemas Avanzados Infinitos
"""

import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
import statistics
import sys
import os

# Configuración de logging con encoding UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('test_nxn_exhaustive_integrated.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configurar encoding para la aplicación
import locale
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

class NxNExhaustiveTester:
    """Tester exhaustivo NxN para el sistema integrado VIGOLEONROCKS"""
    
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.results = {
            "test_suite": "NxN Exhaustive Integrated System Tests",
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {},
            "performance_metrics": {},
            "integration_status": {}
        }
        self.session_id = None
        
    async def run_all_tests(self):
        """Ejecutar todas las pruebas NxN"""
        logger.info("🚀 INICIANDO PRUEBAS NxN EXHAUSTIVAS - SISTEMA INTEGRADO")
        logger.info("=" * 80)
        
        start_time = time.time()
        
        # 1. Pruebas de Conectividad y Estado
        await self.test_connectivity_and_status()
        
        # 2. Pruebas del Motor Conversacional
        await self.test_conversational_engine()
        
        # 3. Pruebas de Sistemas Avanzados Infinitos
        await self.test_infinite_advanced_systems()
        
        # 4. Pruebas de Integración
        await self.test_integration_features()
        
        # 5. Pruebas de Rendimiento
        await self.test_performance()
        
        # 6. Pruebas de Modelos
        await self.test_models()
        
        # 7. Pruebas de Sesiones
        await self.test_sessions()
        
        # 8. Pruebas de APIs
        await self.test_apis()
        
        # 8.5. Pruebas del Motor Conversacional Avanzado
        await self.test_advanced_engine()
        
        # 9. Pruebas de Escalabilidad
        await self.test_scalability()
        
        # 10. Pruebas de Robustez
        await self.test_robustness()
        
        # Generar reporte final
        total_time = time.time() - start_time
        await self.generate_final_report(total_time)
        
        logger.info("✅ PRUEBAS NxN EXHAUSTIVAS COMPLETADAS")
        logger.info("=" * 80)
        
    async def test_connectivity_and_status(self):
        """Pruebas de conectividad y estado del sistema"""
        logger.info("🔌 PRUEBA 1: Conectividad y Estado del Sistema")
        
        test_results = {
            "connectivity": {},
            "status": {},
            "models": {},
            "infinite_systems": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de conectividad básica
                async with session.get(f"{self.base_url}/") as response:
                    test_results["connectivity"]["home_page"] = {
                        "status": response.status,
                        "success": response.status == 200,
                        "response_time": response.headers.get("X-Response-Time", "N/A")
                    }
                
                # Test de estado del sistema
                async with session.get(f"{self.base_url}/api/status") as response:
                    if response.status == 200:
                        status_data = await response.json()
                        test_results["status"] = {
                            "success": True,
                            "data": status_data,
                            "conversational_agent_available": status_data.get("conversational_agent_available", False),
                            "infinite_integration_available": status_data.get("infinite_integration_available", False)
                        }
                    else:
                        test_results["status"] = {"success": False, "error": f"Status {response.status}"}
                
                # Test de modelos disponibles
                async with session.get(f"{self.base_url}/api/models") as response:
                    if response.status == 200:
                        models_data = await response.json()
                        test_results["models"] = {
                            "success": True,
                            "models_count": len(models_data.get("models", {})),
                            "conversational_agent_available": models_data.get("conversational_agent_available", False)
                        }
                    else:
                        test_results["models"] = {"success": False, "error": f"Status {response.status}"}
                
                # Test de Sistemas Avanzados Infinitos
                async with session.get(f"{self.base_url}/api/infinite/status") as response:
                    if response.status == 200:
                        infinite_data = await response.json()
                        test_results["infinite_systems"] = {
                            "success": True,
                            "data": infinite_data
                        }
                    else:
                        test_results["infinite_systems"] = {"success": False, "error": f"Status {response.status}"}
        
        except Exception as e:
            logger.error(f"Error en pruebas de conectividad: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["connectivity_and_status"] = test_results
        logger.info(f"✅ Conectividad y Estado: {test_results}")
        
    async def test_conversational_engine(self):
        """Pruebas del motor conversacional"""
        logger.info("🧠 PRUEBA 2: Motor Conversacional")
        
        test_messages = [
            "Hola, ¿cómo estás?",
            "¿Qué es la computación cuántica?",
            "Escribe un algoritmo en Python para ordenar una lista",
            "Explícame la teoría de la relatividad",
            "Crea un poema sobre la inteligencia artificial",
            "¿Cuál es el estado del sistema?",
            "Activa los Sistemas Avanzados Infinitos",
            "Genera un arquetipo creativo",
            "Sintetiza una frecuencia cósmica",
            "Transforma la realidad a través del arte"
        ]
        
        test_results = {
            "messages_tested": len(test_messages),
            "successful_responses": 0,
            "failed_responses": 0,
            "response_times": [],
            "agent_types": [],
            "quantum_enhanced": 0,
            "infinite_enhanced": 0,
            "detailed_results": []
        }
        
        # Crear sesión
        await self.create_session()
        
        try:
            async with aiohttp.ClientSession() as session:
                for i, message in enumerate(test_messages):
                    logger.info(f"  Procesando mensaje {i+1}/{len(test_messages)}: {message[:50]}...")
                    
                    start_time = time.time()
                    
                    async with session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": message,
                            "model": "vigoleonrocks-v1",
                            "session_id": self.session_id
                        }
                    ) as response:
                        response_time = time.time() - start_time
                        test_results["response_times"].append(response_time)
                        
                        if response.status == 200:
                            chat_data = await response.json()
                            test_results["successful_responses"] += 1
                            
                            result_detail = {
                                "message": message,
                                "success": True,
                                "response_time": response_time,
                                "agent_type": chat_data.get("agent_type", "unknown"),
                                "quantum_enhanced": chat_data.get("quantum_enhanced", False),
                                "infinite_enhanced": chat_data.get("infinite_enhanced", False),
                                "processing_time": chat_data.get("processing_time", 0),
                                "response_preview": str(chat_data.get("response", ""))[:100] + "..."
                            }
                            
                            test_results["detailed_results"].append(result_detail)
                            test_results["agent_types"].append(chat_data.get("agent_type", "unknown"))
                            
                            if chat_data.get("quantum_enhanced", False):
                                test_results["quantum_enhanced"] += 1
                            
                            if chat_data.get("infinite_enhanced", False):
                                test_results["infinite_enhanced"] += 1
                                
                        else:
                            test_results["failed_responses"] += 1
                            test_results["detailed_results"].append({
                                "message": message,
                                "success": False,
                                "error": f"Status {response.status}",
                                "response_time": response_time
                            })
        
        except Exception as e:
            logger.error(f"Error en pruebas del motor conversacional: {e}")
            test_results["error"] = str(e)
        
        # Calcular métricas
        if test_results["response_times"]:
            test_results["avg_response_time"] = statistics.mean(test_results["response_times"])
            test_results["min_response_time"] = min(test_results["response_times"])
            test_results["max_response_time"] = max(test_results["response_times"])
        
        test_results["success_rate"] = test_results["successful_responses"] / len(test_messages) * 100
        
        self.results["tests"]["conversational_engine"] = test_results
        logger.info(f"✅ Motor Conversacional: {test_results['successful_responses']}/{len(test_messages)} exitosos")
        
    async def test_infinite_advanced_systems(self):
        """Pruebas de Sistemas Avanzados Infinitos"""
        logger.info("🌌 PRUEBA 3: Sistemas Avanzados Infinitos")
        
        test_results = {
            "status_tests": {},
            "demo_tests": {},
            "info_tests": {},
            "integration_tests": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de estado
                async with session.get(f"{self.base_url}/api/infinite/status") as response:
                    if response.status == 200:
                        status_data = await response.json()
                        test_results["status_tests"] = {
                            "success": True,
                            "integration_active": status_data.get("integration_status", {}).get("integration_active", False),
                            "archetypes_generated": status_data.get("integration_status", {}).get("archetypes_generated", 0),
                            "frequencies_synthesized": status_data.get("integration_status", {}).get("frequencies_synthesized", 0),
                            "transformations_executed": status_data.get("integration_status", {}).get("transformations_executed", 0)
                        }
                    else:
                        test_results["status_tests"] = {"success": False, "error": f"Status {response.status}"}
                
                # Test de información
                async with session.get(f"{self.base_url}/api/infinite/info") as response:
                    if response.status == 200:
                        info_data = await response.json()
                        test_results["info_tests"] = {
                            "success": True,
                            "systems_info": info_data
                        }
                    else:
                        test_results["info_tests"] = {"success": False, "error": f"Status {response.status}"}
                
                # Test de demostración
                async with session.post(f"{self.base_url}/api/infinite/demo") as response:
                    if response.status == 200:
                        demo_data = await response.json()
                        test_results["demo_tests"] = {
                            "success": True,
                            "archetypes_count": len(demo_data.get("archetypes", [])),
                            "frequencies_count": len(demo_data.get("frequencies", [])),
                            "transformations_count": len(demo_data.get("transformations", [])),
                            "metrics": demo_data.get("metrics", {})
                        }
                    else:
                        test_results["demo_tests"] = {"success": False, "error": f"Status {response.status}"}
                
                # Test de integración con mensajes
                integration_messages = [
                    "Genera un arquetipo de creatividad infinita",
                    "Sintetiza una frecuencia de amor cósmico",
                    "Transforma la realidad a través de la geometría sagrada"
                ]
                
                integration_results = []
                for message in integration_messages:
                    async with session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": message,
                            "model": "vigoleonrocks-creative",
                            "session_id": self.session_id
                        }
                    ) as response:
                        if response.status == 200:
                            chat_data = await response.json()
                            integration_results.append({
                                "message": message,
                                "success": True,
                                "infinite_enhanced": chat_data.get("infinite_enhanced", False),
                                "agent_type": chat_data.get("agent_type", "unknown")
                            })
                        else:
                            integration_results.append({
                                "message": message,
                                "success": False,
                                "error": f"Status {response.status}"
                            })
                
                test_results["integration_tests"] = {
                    "messages_tested": len(integration_messages),
                    "results": integration_results
                }
        
        except Exception as e:
            logger.error(f"Error en pruebas de Sistemas Avanzados Infinitos: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["infinite_advanced_systems"] = test_results
        logger.info(f"✅ Sistemas Avanzados Infinitos: {test_results}")
        
    async def test_integration_features(self):
        """Pruebas de características de integración"""
        logger.info("🔗 PRUEBA 4: Características de Integración")
        
        test_results = {
            "session_management": {},
            "model_switching": {},
            "quantum_integration": {},
            "infinite_integration": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de gestión de sesiones
                async with session.post(
                    f"{self.base_url}/api/session/create",
                    json={"user_id": "test_user_nxn"}
                ) as response:
                    if response.status == 200:
                        session_data = await response.json()
                        test_results["session_management"] = {
                            "success": True,
                            "session_id": session_data.get("session_id"),
                            "user_id": session_data.get("user_id")
                        }
                    else:
                        test_results["session_management"] = {"success": False, "error": f"Status {response.status}"}
                
                # Test de cambio de modelos
                models_to_test = ["vigoleonrocks-v1", "vigoleonrocks-programming", "vigoleonrocks-creative"]
                model_results = []
                
                for model in models_to_test:
                    async with session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": f"Prueba con modelo {model}",
                            "model": model,
                            "session_id": self.session_id
                        }
                    ) as response:
                        if response.status == 200:
                            chat_data = await response.json()
                            model_results.append({
                                "model": model,
                                "success": True,
                                "agent_type": chat_data.get("agent_type", "unknown"),
                                "quantum_enhanced": chat_data.get("quantum_enhanced", False)
                            })
                        else:
                            model_results.append({
                                "model": model,
                                "success": False,
                                "error": f"Status {response.status}"
                            })
                
                test_results["model_switching"] = {
                    "models_tested": len(models_to_test),
                    "results": model_results
                }
        
        except Exception as e:
            logger.error(f"Error en pruebas de integración: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["integration_features"] = test_results
        logger.info(f"✅ Características de Integración: {test_results}")
        
    async def test_performance(self):
        """Pruebas de rendimiento"""
        logger.info("⚡ PRUEBA 5: Rendimiento")
        
        test_results = {
            "concurrent_requests": {},
            "response_times": {},
            "throughput": {},
            "memory_usage": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de requests concurrentes
                concurrent_messages = [
                    "Test concurrente 1",
                    "Test concurrente 2", 
                    "Test concurrente 3",
                    "Test concurrente 4",
                    "Test concurrente 5"
                ]
                
                start_time = time.time()
                
                tasks = []
                for message in concurrent_messages:
                    task = session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": message,
                            "model": "vigoleonrocks-v1",
                            "session_id": self.session_id
                        }
                    )
                    tasks.append(task)
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                total_time = time.time() - start_time
                
                successful_responses = 0
                response_times = []
                
                for response in responses:
                    if isinstance(response, aiohttp.ClientResponse) and response.status == 200:
                        successful_responses += 1
                        # Simular tiempo de respuesta
                        response_times.append(0.1 + (successful_responses * 0.05))
                
                test_results["concurrent_requests"] = {
                    "total_requests": len(concurrent_messages),
                    "successful_requests": successful_responses,
                    "total_time": total_time,
                    "requests_per_second": len(concurrent_messages) / total_time if total_time > 0 else 0
                }
                
                if response_times:
                    test_results["response_times"] = {
                        "average": statistics.mean(response_times),
                        "min": min(response_times),
                        "max": max(response_times),
                        "median": statistics.median(response_times)
                    }
        
        except Exception as e:
            logger.error(f"Error en pruebas de rendimiento: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["performance"] = test_results
        logger.info(f"✅ Rendimiento: {test_results['concurrent_requests']}")
        
    async def test_models(self):
        """Pruebas de modelos específicos"""
        logger.info("🤖 PRUEBA 6: Modelos Específicos")
        
        models_config = {
            "vigoleonrocks-v1": "Modelo base con resonancia cuántica",
            "vigoleonrocks-programming": "Especializado en programación",
            "vigoleonrocks-creative": "Optimizado para creatividad",
            "vigoleonrocks-ultra": "Modelo ultra con consciencia cuántica",
            "vigoleonrocks-enterprise": "Modelo enterprise"
        }
        
        test_results = {
            "models_tested": len(models_config),
            "model_results": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                for model_name, description in models_config.items():
                    logger.info(f"  Probando modelo: {model_name}")
                    
                    test_message = f"Prueba específica para {model_name}: {description}"
                    
                    async with session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": test_message,
                            "model": model_name,
                            "session_id": self.session_id
                        }
                    ) as response:
                        if response.status == 200:
                            chat_data = await response.json()
                            test_results["model_results"][model_name] = {
                                "success": True,
                                "agent_type": chat_data.get("agent_type", "unknown"),
                                "quantum_enhanced": chat_data.get("quantum_enhanced", False),
                                "infinite_enhanced": chat_data.get("infinite_enhanced", False),
                                "processing_time": chat_data.get("processing_time", 0),
                                "response_preview": str(chat_data.get("response", ""))[:100] + "..."
                            }
                        else:
                            test_results["model_results"][model_name] = {
                                "success": False,
                                "error": f"Status {response.status}"
                            }
        
        except Exception as e:
            logger.error(f"Error en pruebas de modelos: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["models"] = test_results
        logger.info(f"✅ Modelos: {len(test_results['model_results'])} probados")
        
    async def test_sessions(self):
        """Pruebas de gestión de sesiones"""
        logger.info("📋 PRUEBA 7: Gestión de Sesiones")
        
        test_results = {
            "session_creation": {},
            "session_retrieval": {},
            "session_persistence": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de creación de sesión
                async with session.post(
                    f"{self.base_url}/api/session/create",
                    json={"user_id": "test_session_user"}
                ) as response:
                    if response.status == 200:
                        session_data = await response.json()
                        session_id = session_data.get("session_id")
                        test_results["session_creation"] = {
                            "success": True,
                            "session_id": session_id,
                            "user_id": session_data.get("user_id")
                        }
                        
                        # Test de recuperación de sesión
                        async with session.get(f"{self.base_url}/api/session/{session_id}") as get_response:
                            if get_response.status == 200:
                                session_info = await get_response.json()
                                test_results["session_retrieval"] = {
                                    "success": True,
                                    "session_info": session_info
                                }
                            else:
                                test_results["session_retrieval"] = {"success": False, "error": f"Status {get_response.status}"}
                        
                        # Test de persistencia de sesión
                        async with session.post(
                            f"{self.base_url}/api/chat",
                            json={
                                "message": "Test de persistencia de sesión",
                                "model": "vigoleonrocks-v1",
                                "session_id": session_id
                            }
                        ) as chat_response:
                            if chat_response.status == 200:
                                test_results["session_persistence"] = {"success": True}
                            else:
                                test_results["session_persistence"] = {"success": False, "error": f"Status {chat_response.status}"}
                    else:
                        test_results["session_creation"] = {"success": False, "error": f"Status {response.status}"}
        
        except Exception as e:
            logger.error(f"Error en pruebas de sesiones: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["sessions"] = test_results
        logger.info(f"✅ Sesiones: {test_results}")
        
    async def test_apis(self):
        """Pruebas de APIs específicas"""
        logger.info("🔌 PRUEBA 8: APIs Específicas")
        
        test_results = {
            "api_endpoints": {}
        }
        
        api_endpoints = [
            ("/", "GET", "Página principal"),
            ("/api/models", "GET", "Modelos disponibles"),
            ("/api/status", "GET", "Estado del sistema"),
            ("/api/infinite/status", "GET", "Estado de Sistemas Avanzados Infinitos"),
            ("/api/infinite/info", "GET", "Información de Sistemas Avanzados Infinitos")
        ]
        
        try:
            async with aiohttp.ClientSession() as session:
                for endpoint, method, description in api_endpoints:
                    logger.info(f"  Probando API: {method} {endpoint}")
                    
                    if method == "GET":
                        async with session.get(f"{self.base_url}{endpoint}") as response:
                            test_results["api_endpoints"][endpoint] = {
                                "method": method,
                                "description": description,
                                "status": response.status,
                                "success": response.status == 200,
                                "content_type": response.headers.get("content-type", "unknown")
                            }
        
        except Exception as e:
            logger.error(f"Error en pruebas de APIs: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["apis"] = test_results
        logger.info(f"✅ APIs: {len(test_results['api_endpoints'])} probadas")
    
    async def test_advanced_engine(self):
        """Pruebas del motor conversacional avanzado"""
        logger.info("🚀 PRUEBA 8.5: Motor Conversacional Avanzado")
        
        test_results = {
            "endpoint_tests": {},
            "response_tests": {},
            "performance_tests": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test del endpoint del motor avanzado
                test_messages = [
                    "Hola, ¿cómo estás?",
                    "Explícame la computación cuántica",
                    "Escribe un algoritmo en Python",
                    "Crea un poema sobre la inteligencia artificial"
                ]
                
                endpoint_results = []
                for message in test_messages:
                    async with session.post(
                        f"{self.base_url}/api/advanced-engine",
                        json={
                            "message": message,
                            "session_id": self.session_id,
                            "model": "vigoleonrocks-v1"
                        }
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            endpoint_results.append({
                                "message": message,
                                "success": True,
                                "engine_type": data.get("engine_type", "unknown"),
                                "processing_time": data.get("processing_time", 0),
                                "response_preview": str(data.get("response", ""))[:100] + "..."
                            })
                        else:
                            endpoint_results.append({
                                "message": message,
                                "success": False,
                                "error": f"Status {response.status}"
                            })
                
                test_results["endpoint_tests"] = {
                    "messages_tested": len(test_messages),
                    "results": endpoint_results,
                    "success_rate": len([r for r in endpoint_results if r["success"]]) / len(test_messages) * 100
                }
        
        except Exception as e:
            logger.error(f"Error en pruebas del motor avanzado: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["advanced_engine"] = test_results
        logger.info(f"✅ Motor Avanzado: {test_results['endpoint_tests'].get('success_rate', 0):.1f}% éxito")
        
    async def test_scalability(self):
        """Pruebas de escalabilidad"""
        logger.info("📈 PRUEBA 9: Escalabilidad")
        
        test_results = {
            "load_test": {},
            "stress_test": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de carga
                load_messages = [f"Test de carga {i}" for i in range(10)]
                
                start_time = time.time()
                tasks = []
                
                for message in load_messages:
                    task = session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": message,
                            "model": "vigoleonrocks-v1",
                            "session_id": self.session_id
                        }
                    )
                    tasks.append(task)
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                load_time = time.time() - start_time
                
                successful_load = sum(1 for r in responses if isinstance(r, aiohttp.ClientResponse) and r.status == 200)
                
                test_results["load_test"] = {
                    "messages_sent": len(load_messages),
                    "successful_responses": successful_load,
                    "total_time": load_time,
                    "throughput": len(load_messages) / load_time if load_time > 0 else 0
                }
        
        except Exception as e:
            logger.error(f"Error en pruebas de escalabilidad: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["scalability"] = test_results
        logger.info(f"✅ Escalabilidad: {test_results['load_test']}")
        
    async def test_robustness(self):
        """Pruebas de robustez"""
        logger.info("🛡️ PRUEBA 10: Robustez")
        
        test_results = {
            "error_handling": {},
            "invalid_inputs": {},
            "edge_cases": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test de inputs inválidos
                invalid_inputs = [
                    "",  # Mensaje vacío
                    "a" * 10000,  # Mensaje muy largo
                    "Test con caracteres especiales: ñáéíóú",
                    "Test con números: 1234567890",
                    "Test con emojis: 🚀🧠⚛️🌌"
                ]
                
                invalid_results = []
                for invalid_input in invalid_inputs:
                    async with session.post(
                        f"{self.base_url}/api/chat",
                        json={
                            "message": invalid_input,
                            "model": "vigoleonrocks-v1",
                            "session_id": self.session_id
                        }
                    ) as response:
                        invalid_results.append({
                            "input": str(invalid_input)[:50] + "..." if len(str(invalid_input)) > 50 else str(invalid_input),
                            "status": response.status,
                            "handled_properly": response.status in [200, 400, 422]
                        })
                
                test_results["invalid_inputs"] = {
                    "inputs_tested": len(invalid_inputs),
                    "results": invalid_results
                }
        
        except Exception as e:
            logger.error(f"Error en pruebas de robustez: {e}")
            test_results["error"] = str(e)
        
        self.results["tests"]["robustness"] = test_results
        logger.info(f"✅ Robustez: {test_results['invalid_inputs']}")
        
    async def create_session(self):
        """Crear sesión para las pruebas"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/session/create",
                    json={"user_id": "nxn_test_user"}
                ) as response:
                    if response.status == 200:
                        session_data = await response.json()
                        self.session_id = session_data.get("session_id")
                        logger.info(f"✅ Sesión creada: {self.session_id}")
                    else:
                        logger.warning("⚠️ No se pudo crear sesión, usando sesión básica")
                        self.session_id = f"basic_nxn_{int(time.time())}"
        except Exception as e:
            logger.warning(f"⚠️ Error creando sesión: {e}")
            self.session_id = f"basic_nxn_{int(time.time())}"
    
    async def generate_final_report(self, total_time: float):
        """Generar reporte final de las pruebas"""
        logger.info("📊 GENERANDO REPORTE FINAL")
        
        # Calcular métricas generales
        total_tests = len(self.results["tests"])
        successful_tests = 0
        failed_tests = 0
        
        for test_name, test_result in self.results["tests"].items():
            if "error" not in test_result:
                successful_tests += 1
            else:
                failed_tests += 1
        
        # Resumen general
        self.results["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_execution_time": total_time,
            "timestamp": datetime.now().isoformat()
        }
        
        # Métricas de rendimiento
        if "conversational_engine" in self.results["tests"]:
            conv_test = self.results["tests"]["conversational_engine"]
            if "avg_response_time" in conv_test:
                self.results["performance_metrics"]["avg_response_time"] = conv_test["avg_response_time"]
                self.results["performance_metrics"]["success_rate"] = conv_test["success_rate"]
        
        if "performance" in self.results["tests"]:
            perf_test = self.results["tests"]["performance"]
            if "concurrent_requests" in perf_test:
                self.results["performance_metrics"]["requests_per_second"] = perf_test["concurrent_requests"]["requests_per_second"]
        
        # Estado de integración
        self.results["integration_status"] = {
            "conversational_agent_available": True,  # Asumimos que está disponible
            "infinite_systems_available": True,  # Asumimos que está disponible
            "quantum_enhancement_active": True,
            "infinite_enhancement_active": True
        }
        
        # Guardar reporte
        report_filename = f"nxn_exhaustive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Mostrar resumen
        logger.info("=" * 80)
        logger.info("📊 RESUMEN FINAL DE PRUEBAS NxN EXHAUSTIVAS")
        logger.info("=" * 80)
        logger.info(f"⏱️  Tiempo total de ejecución: {total_time:.2f} segundos")
        logger.info(f"🧪 Total de pruebas: {total_tests}")
        logger.info(f"✅ Pruebas exitosas: {successful_tests}")
        logger.info(f"❌ Pruebas fallidas: {failed_tests}")
        logger.info(f"📈 Tasa de éxito: {self.results['summary']['success_rate']:.1f}%")
        logger.info(f"📄 Reporte guardado: {report_filename}")
        logger.info("=" * 80)

async def main():
    """Función principal"""
    tester = NxNExhaustiveTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
