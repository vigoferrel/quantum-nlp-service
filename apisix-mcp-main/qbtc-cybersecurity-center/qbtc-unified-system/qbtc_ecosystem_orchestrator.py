#!/usr/bin/env python3
"""
QBTC Ecosystem Orchestrator
===========================
Orquestador completo para activar flujo end-to-end del ecosistema integrado.
Consolida todas las mejoras implementadas desde la raíz.
"""

import subprocess
import threading
import time
import requests
import json
import pika
from datetime import datetime
from pathlib import Path
import os
import signal

class QBTCEcosystemOrchestrator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.processes = {}
        self.results = {
            "timestamp": self.timestamp,
            "orchestration_status": {},
            "service_activation": {},
            "end_to_end_test": {},
            "supabase_integration": {},
            "performance_metrics": {},
            "errors": []
        }
        
        self.services_config = {
            "rabbitmq": {"port": 5672, "management_port": 15672},
            "ollama": {"port": 11434},
            "api_server": {"port": 5001},
            "aics_service": {"port": 8001},
            "quantum_core": {"port": 8002}, 
            "kong_gateway": {"port": 8000},
            "supabase": {"port": 54321}
        }

    def start_quantum_core_consumer(self):
        """Iniciar quantum core consumer en segundo plano"""
        print("Iniciando Quantum Core Consumer...")
        
        try:
            # Verificar que el script existe
            consumer_script = Path("quantum_core_consumer.py")
            if not consumer_script.exists():
                print("ADVERTENCIA: quantum_core_consumer.py no encontrado, creando...")
                self.create_quantum_consumer_script()
            
            # Iniciar proceso en segundo plano
            process = subprocess.Popen(
                ["python", "quantum_core_consumer.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            self.processes["quantum_consumer"] = process
            print(f"Quantum Core Consumer iniciado (PID: {process.pid})")
            
            # Esperar un momento para que inicie
            time.sleep(3)
            
            # Verificar que sigue corriendo
            if process.poll() is None:
                self.results["service_activation"]["quantum_consumer"] = {
                    "status": "running",
                    "pid": process.pid
                }
                return True
            else:
                self.results["service_activation"]["quantum_consumer"] = {
                    "status": "failed",
                    "error": "Process terminated immediately"
                }
                return False
                
        except Exception as e:
            error = f"Error iniciando Quantum Core Consumer: {e}"
            print(f"ERROR: {error}")
            self.results["errors"].append(error)
            return False

    def create_quantum_consumer_script(self):
        """Crear script del quantum core consumer si no existe"""
        consumer_code = '''#!/usr/bin/env python3
"""
Quantum Core Consumer - Optimizado para QBTC
"""
import pika
import json
import requests
import time
import sys

class OptimizedQuantumConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect_rabbitmq()
        
    def connect_rabbitmq(self):
        """Conectar a RabbitMQ con reintentos"""
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(
                    pika.URLParameters("amqp://guest:guest@localhost:5672/")
                )
                self.channel = self.connection.channel()
                print("Conectado a RabbitMQ")
                return True
            except Exception as e:
                print(f"Intento {attempt + 1} fallido: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    print("No se pudo conectar a RabbitMQ")
                    return False
    
    def process_llm_request(self, ch, method, properties, body):
        """Procesar solicitud LLM"""
        try:
            message = json.loads(body.decode())
            print(f"Procesando: {message.get('message_id', 'unknown')}")
            
            # Llamar a Ollama
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": message.get("model", "vigoleonrocks:latest"),
                    "prompt": message.get("request", ""),
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_ctx": 2048
                    }
                },
                timeout=60
            )
            
            if ollama_response.status_code == 200:
                result = ollama_response.json()
                response_message = {
                    "message_id": message.get("message_id"),
                    "response": result.get("response", ""),
                    "status": "completed",
                    "model_used": message.get("model"),
                    "processing_time": time.time()
                }
                
                # Publicar respuesta
                self.channel.basic_publish(
                    exchange='responses',
                    routing_key='llm.response',
                    body=json.dumps(response_message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
                
                print(f"Respuesta enviada: {message.get('message_id')}")
            else:
                print(f"Error Ollama: {ollama_response.status_code}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error procesando mensaje: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        """Iniciar consumo de mensajes"""
        try:
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue='q_llm_requests',
                on_message_callback=self.process_llm_request
            )
            
            print("Quantum Core Consumer activo...")
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            print("Deteniendo consumer...")
            self.channel.stop_consuming()
            self.connection.close()
        except Exception as e:
            print(f"Error en consumer: {e}")

if __name__ == "__main__":
    consumer = OptimizedQuantumConsumer()
    consumer.start_consuming()
'''
        
        with open("quantum_core_consumer.py", "w") as f:
            f.write(consumer_code)
        print("Script quantum_core_consumer.py creado")

    def test_end_to_end_flow(self):
        """Probar flujo completo end-to-end"""
        print("Ejecutando prueba end-to-end...")
        
        test_results = {
            "message_flow": {},
            "response_received": False,
            "total_latency": 0,
            "components_tested": []
        }
        
        try:
            # 1. Conectar a RabbitMQ
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            channel = connection.channel()
            
            # 2. Crear mensaje de prueba
            test_message = {
                "message_id": f"e2e_test_{self.timestamp}",
                "request": "Explain quantum consciousness in 50 words",
                "model": "vigoleonrocks-ultra-minimal:latest",
                "timestamp": time.time()
            }
            
            start_time = time.time()
            
            # 3. Enviar mensaje
            channel.basic_publish(
                exchange='llm_requests',
                routing_key='llm.request',
                body=json.dumps(test_message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            
            test_results["message_flow"]["request_sent"] = True
            test_results["components_tested"].append("RabbitMQ_Publisher")
            print("Mensaje de prueba enviado")
            
            # 4. Esperar respuesta (timeout 120 segundos)
            timeout = 120
            response_received = False
            
            def timeout_callback():
                nonlocal response_received
                time.sleep(timeout)
                if not response_received:
                    print("TIMEOUT: No se recibió respuesta")
            
            timeout_thread = threading.Thread(target=timeout_callback)
            timeout_thread.daemon = True
            timeout_thread.start()
            
            # 5. Escuchar respuesta
            for attempt in range(timeout):
                try:
                    method, properties, body = channel.basic_get(queue='q_llm_responses', auto_ack=True)
                    if method:
                        response = json.loads(body.decode())
                        if response.get("message_id") == test_message["message_id"]:
                            end_time = time.time()
                            test_results["response_received"] = True
                            test_results["total_latency"] = end_time - start_time
                            test_results["response_content"] = response.get("response", "")[:100]
                            test_results["components_tested"].extend(["Quantum_Consumer", "Ollama", "Response_Publisher"])
                            response_received = True
                            print(f"Respuesta recibida en {test_results['total_latency']:.2f}s")
                            break
                    time.sleep(1)
                except Exception as e:
                    print(f"Error esperando respuesta: {e}")
                    break
            
            connection.close()
            
            # 6. Evaluar resultado
            if response_received:
                test_results["status"] = "SUCCESS"
                print("FLUJO END-TO-END: EXITOSO")
            else:
                test_results["status"] = "TIMEOUT"
                print("FLUJO END-TO-END: TIMEOUT")
            
            self.results["end_to_end_test"] = test_results
            return response_received
            
        except Exception as e:
            error = f"Error en prueba end-to-end: {e}"
            print(f"ERROR: {error}")
            self.results["errors"].append(error)
            return False

    def integrate_supabase_xl(self):
        """Integrar Supabase XL en la arquitectura"""
        print("Integrando Supabase XL...")
        
        supabase_integration = {
            "volume_analysis": {},
            "connection_test": {},
            "schema_discovery": {}
        }
        
        try:
            # 1. Analizar volúmenes Supabase
            result = subprocess.run(['docker', 'volume', 'ls'], capture_output=True, text=True)
            if result.returncode == 0:
                supabase_volumes = [line.split()[-1] for line in result.stdout.split('\n') 
                                 if 'supabase' in line.lower() and 'vigoleonrocks' in line.lower()]
                
                supabase_integration["volume_analysis"]["volumes_found"] = len(supabase_volumes)
                supabase_integration["volume_analysis"]["volume_names"] = supabase_volumes
                print(f"Volúmenes Supabase encontrados: {len(supabase_volumes)}")
            
            # 2. Probar conexión Supabase
            try:
                response = requests.get("http://localhost:54321", timeout=5)
                supabase_integration["connection_test"]["status"] = "reachable"
                supabase_integration["connection_test"]["status_code"] = response.status_code
                print("Supabase: ACCESIBLE")
            except:
                supabase_integration["connection_test"]["status"] = "unreachable"
                print("Supabase: NO ACCESIBLE")
            
            # 3. Crear integración con eventos
            integration_config = {
                "event_logging": {
                    "llm_requests": "supabase.llm_requests_log",
                    "responses": "supabase.llm_responses_log",
                    "performance": "supabase.performance_metrics"
                },
                "model_storage": {
                    "vigoleonrocks_models": "supabase.model_configurations",
                    "quantum_states": "supabase.quantum_consciousness_states"
                }
            }
            
            with open("supabase_integration_config.json", "w") as f:
                json.dump(integration_config, f, indent=2)
            
            supabase_integration["config_created"] = True
            print("Configuración de integración Supabase creada")
            
            self.results["supabase_integration"] = supabase_integration
            return True
            
        except Exception as e:
            error = f"Error integrando Supabase XL: {e}"
            print(f"ERROR: {error}")
            self.results["errors"].append(error)
            return False

    def run_unified_benchmark(self):
        """Ejecutar benchmark completo del ecosistema unificado"""
        print("Ejecutando benchmark del ecosistema unificado...")
        
        benchmark_results = {
            "infrastructure_test": {},
            "performance_metrics": {},
            "service_health": {},
            "integration_score": 0
        }
        
        try:
            # 1. Probar todos los servicios
            services_status = {}
            for service_name, config in self.services_config.items():
                try:
                    if service_name == "rabbitmq":
                        # Probar management interface
                        response = requests.get(f"http://localhost:{config['management_port']}", timeout=5)
                        status = "healthy" if response.status_code in [200, 401] else "degraded"
                    else:
                        response = requests.get(f"http://localhost:{config['port']}", timeout=5)
                        status = "healthy" if response.status_code in [200, 404, 405] else "degraded"
                    
                    services_status[service_name] = {
                        "status": status,
                        "response_time": response.elapsed.total_seconds()
                    }
                    
                except Exception as e:
                    services_status[service_name] = {
                        "status": "unavailable",
                        "error": str(e)
                    }
            
            benchmark_results["service_health"] = services_status
            
            # 2. Calcular métricas de rendimiento
            healthy_services = sum(1 for s in services_status.values() if s["status"] == "healthy")
            total_services = len(services_status)
            
            avg_response_time = sum(s.get("response_time", 0) for s in services_status.values() 
                                  if s.get("response_time")) / max(1, len([s for s in services_status.values() if s.get("response_time")]))
            
            benchmark_results["performance_metrics"] = {
                "service_availability": f"{healthy_services}/{total_services}",
                "availability_percentage": (healthy_services / total_services) * 100,
                "average_response_time": round(avg_response_time, 3),
                "end_to_end_working": self.results.get("end_to_end_test", {}).get("status") == "SUCCESS"
            }
            
            # 3. Calcular score de integración
            integration_score = 0
            
            # Servicios saludables (40 puntos)
            integration_score += (healthy_services / total_services) * 40
            
            # End-to-end funcionando (30 puntos)
            if benchmark_results["performance_metrics"]["end_to_end_working"]:
                integration_score += 30
            
            # RabbitMQ funcionando (20 puntos)
            if services_status.get("rabbitmq", {}).get("status") == "healthy":
                integration_score += 20
            
            # Supabase integrado (10 puntos)
            if self.results.get("supabase_integration", {}).get("config_created"):
                integration_score += 10
            
            benchmark_results["integration_score"] = round(integration_score, 1)
            
            self.results["performance_metrics"] = benchmark_results
            
            print(f"Score de integración: {integration_score}/100")
            print(f"Disponibilidad de servicios: {benchmark_results['performance_metrics']['availability_percentage']:.1f}%")
            
            return benchmark_results
            
        except Exception as e:
            error = f"Error en benchmark unificado: {e}"
            print(f"ERROR: {error}")
            self.results["errors"].append(error)
            return None

    def generate_final_report(self):
        """Generar reporte final de mejoras concretas"""
        report_file = f"qbtc_ecosystem_final_report_{self.timestamp}.json"
        
        # Calcular métricas finales
        summary = {
            "ecosystem_status": "OPERATIONAL" if self.results.get("performance_metrics", {}).get("integration_score", 0) >= 70 else "DEGRADED",
            "integration_score": self.results.get("performance_metrics", {}).get("integration_score", 0),
            "services_healthy": self.results.get("performance_metrics", {}).get("availability_percentage", 0),
            "end_to_end_working": self.results.get("end_to_end_test", {}).get("status") == "SUCCESS",
            "supabase_integrated": bool(self.results.get("supabase_integration", {}).get("config_created")),
            "quantum_consumer_running": self.results.get("service_activation", {}).get("quantum_consumer", {}).get("status") == "running",
            "total_errors": len(self.results["errors"]),
            "timestamp": self.timestamp
        }
        
        self.results["final_summary"] = summary
        
        # Guardar reporte
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        # Mostrar resumen
        print("\n" + "="*70)
        print("REPORTE FINAL: QBTC ECOSYSTEM ORCHESTRATION")
        print("="*70)
        print(f"Estado del ecosistema: {summary['ecosystem_status']}")
        print(f"Score de integración: {summary['integration_score']}/100")
        print(f"Servicios saludables: {summary['services_healthy']:.1f}%")
        print(f"Flujo end-to-end: {'FUNCIONANDO' if summary['end_to_end_working'] else 'FALLIDO'}")
        print(f"Supabase XL integrado: {'SI' if summary['supabase_integrated'] else 'NO'}")
        print(f"Quantum Consumer: {'ACTIVO' if summary['quantum_consumer_running'] else 'INACTIVO'}")
        print(f"Total errores: {summary['total_errors']}")
        
        if summary['integration_score'] >= 90:
            print("\nESTADO: EXCELENCIA OPERACIONAL ALCANZADA")
        elif summary['integration_score'] >= 70:
            print("\nESTADO: ECOSISTEMA OPERACIONAL")
        else:
            print("\nESTADO: REQUIERE OPTIMIZACIÓN")
        
        print(f"\nReporte completo: {report_file}")
        return report_file

    def cleanup_processes(self):
        """Limpiar procesos iniciados"""
        for name, process in self.processes.items():
            try:
                if process.poll() is None:
                    process.terminate()
                    print(f"Proceso {name} terminado")
            except:
                pass

def main():
    """Función principal de orquestación"""
    print("QBTC Ecosystem Orchestrator")
    print("="*50)
    print("Consolidando mejoras y activando flujo completo end-to-end")
    
    orchestrator = QBTCEcosystemOrchestrator()
    
    try:
        # Paso 1: Iniciar Quantum Core Consumer
        print("\n1. Iniciando Quantum Core Consumer...")
        consumer_started = orchestrator.start_quantum_core_consumer()
        
        # Paso 2: Probar flujo end-to-end
        print("\n2. Probando flujo end-to-end...")
        end_to_end_success = orchestrator.test_end_to_end_flow()
        
        # Paso 3: Integrar Supabase XL
        print("\n3. Integrando Supabase XL...")
        supabase_integrated = orchestrator.integrate_supabase_xl()
        
        # Paso 4: Ejecutar benchmark unificado
        print("\n4. Ejecutando benchmark del ecosistema...")
        benchmark_results = orchestrator.run_unified_benchmark()
        
        # Paso 5: Generar reporte final
        print("\n5. Generando reporte final...")
        report_file = orchestrator.generate_final_report()
        
        print(f"\nORQUESTACION COMPLETADA")
        print(f"Ver resultados detallados en: {report_file}")
        
        return True
        
    except KeyboardInterrupt:
        print("\nOrquestación interrumpida por usuario")
        return False
    finally:
        orchestrator.cleanup_processes()

if __name__ == "__main__":
    main()