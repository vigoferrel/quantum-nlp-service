#!/usr/bin/env python3
"""
QBTC Final Integration
=====================
Integración final completa del ecosistema QBTC desde la raíz.
Enfoque directo sin auto-fixes que puedan colgarse.
"""

import requests
import pika
import json
import time
import subprocess
from datetime import datetime

class QBTCFinalIntegration:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "timestamp": self.timestamp,
            "infrastructure_status": {},
            "integration_tests": {},
            "supabase_integration": {},
            "final_metrics": {},
            "recommendations": []
        }
    
    def verify_core_infrastructure(self):
        """Verificar infraestructura central"""
        print("VERIFICANDO INFRAESTRUCTURA CENTRAL")
        print("-" * 50)
        
        status = {}
        
        # 1. RabbitMQ
        print("1. RabbitMQ...")
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            channel = connection.channel()
            
            # Verificar colas principales
            queue_status = {}
            for queue in ['q_llm_requests', 'q_llm_responses']:
                try:
                    method = channel.queue_declare(queue=queue, passive=True)
                    queue_status[queue] = {
                        "exists": True,
                        "messages": method.method.message_count,
                        "consumers": method.method.consumer_count
                    }
                except Exception as e:
                    queue_status[queue] = {"exists": False, "error": str(e)}
            
            connection.close()
            
            status["rabbitmq"] = {
                "accessible": True,
                "queues": queue_status
            }
            
            # Verificar si hay consumers activos
            consumers_active = any(q.get("consumers", 0) > 0 for q in queue_status.values() if q.get("exists"))
            print(f"   Estado: FUNCIONAL - Consumers activos: {consumers_active}")
            
        except Exception as e:
            status["rabbitmq"] = {"accessible": False, "error": str(e)}
            print(f"   Estado: FALLO - {e}")
        
        # 2. Ollama
        print("2. Ollama...")
        try:
            response = requests.get("http://localhost:11434/api/version", timeout=5)
            if response.status_code == 200:
                version_info = response.json()
                
                # Verificar modelos
                models_resp = requests.get("http://localhost:11434/api/tags", timeout=10)
                models_info = {}
                if models_resp.status_code == 200:
                    models = models_resp.json()
                    vigoleonrocks_models = [m for m in models.get('models', []) if 'vigoleonrocks' in m['name']]
                    models_info = {
                        "total": len(models.get('models', [])),
                        "vigoleonrocks": len(vigoleonrocks_models),
                        "vigoleonrocks_models": [m['name'] for m in vigoleonrocks_models]
                    }
                
                status["ollama"] = {
                    "accessible": True,
                    "version": version_info.get("version"),
                    "models": models_info
                }
                print(f"   Estado: FUNCIONAL - Versión: {version_info.get('version')} - Modelos vigoleonrocks: {models_info.get('vigoleonrocks', 0)}")
                
            else:
                status["ollama"] = {"accessible": False, "status_code": response.status_code}
                print(f"   Estado: ERROR - Status {response.status_code}")
                
        except Exception as e:
            status["ollama"] = {"accessible": False, "error": str(e)}
            print(f"   Estado: FALLO - {e}")
        
        # 3. Servicios Docker
        print("3. Servicios Docker...")
        docker_services = {
            "kong_gateway": 8000,
            "api_server": 5001,
            "aics_service": 8001,
            "quantum_core": 8002
        }
        
        service_status = {}
        healthy_count = 0
        
        for service, port in docker_services.items():
            try:
                response = requests.get(f"http://localhost:{port}", timeout=3)
                if response.status_code in [200, 404, 405]:
                    service_status[service] = {"healthy": True, "status_code": response.status_code}
                    healthy_count += 1
                    print(f"   {service}: OK ({response.status_code})")
                else:
                    service_status[service] = {"healthy": False, "status_code": response.status_code}
                    print(f"   {service}: DEGRADADO ({response.status_code})")
            except Exception as e:
                service_status[service] = {"healthy": False, "error": str(e)}
                print(f"   {service}: FALLO")
        
        service_health_percentage = (healthy_count / len(docker_services)) * 100
        status["docker_services"] = {
            "services": service_status,
            "health_percentage": service_health_percentage,
            "healthy_count": healthy_count,
            "total_count": len(docker_services)
        }
        
        print(f"   Salud general: {service_health_percentage:.1f}% ({healthy_count}/{len(docker_services)})")
        
        self.results["infrastructure_status"] = status
        return status
    
    def test_message_flow_comprehensive(self):
        """Prueba completa del flujo de mensajes"""
        print("\nPRUEBA COMPLETA DE FLUJO DE MENSAJES")
        print("-" * 50)
        
        flow_results = {
            "message_sent": False,
            "message_routed": False,
            "response_received": False,
            "total_latency": 0,
            "ollama_response": None
        }
        
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            channel = connection.channel()
            
            # 1. Crear mensaje de prueba
            test_message = {
                "message_id": f"final_test_{self.timestamp}",
                "request": "What is quantum consciousness? Explain in 30 words.",
                "model": "vigoleonrocks:latest",
                "timestamp": time.time()
            }
            
            print("1. Enviando mensaje de prueba...")
            start_time = time.time()
            
            channel.basic_publish(
                exchange='llm_requests',
                routing_key='llm.request',
                body=json.dumps(test_message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            
            flow_results["message_sent"] = True
            print("   Mensaje enviado: OK")
            
            # 2. Verificar routing
            time.sleep(1)
            method = channel.queue_declare(queue='q_llm_requests', passive=True)
            messages_in_queue = method.method.message_count
            
            if messages_in_queue > 0:
                flow_results["message_routed"] = True
                print(f"   Mensaje en cola: OK ({messages_in_queue} mensajes)")
            else:
                print("   Mensaje en cola: NO ENCONTRADO")
            
            # 3. Esperar respuesta (45 segundos)
            print("3. Esperando respuesta (45 segundos)...")
            
            for attempt in range(45):
                try:
                    method, properties, body = channel.basic_get(queue='q_llm_responses', auto_ack=True)
                    if method:
                        response = json.loads(body.decode())
                        if response.get("message_id") == test_message["message_id"]:
                            end_time = time.time()
                            flow_results["response_received"] = True
                            flow_results["total_latency"] = end_time - start_time
                            flow_results["ollama_response"] = response.get("response", "")[:100]
                            
                            print(f"   Respuesta recibida: OK ({flow_results['total_latency']:.2f}s)")
                            print(f"   Contenido: {flow_results['ollama_response']}...")
                            break
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"   Error verificando respuesta: {e}")
                    break
            
            if not flow_results["response_received"]:
                print("   Respuesta: TIMEOUT (45s)")
            
            connection.close()
            
        except Exception as e:
            print(f"   Error en flujo de mensajes: {e}")
        
        self.results["integration_tests"]["message_flow"] = flow_results
        return flow_results
    
    def integrate_supabase_final(self):
        """Integración final con Supabase XL"""
        print("\nINTEGRACIÓN SUPABASE XL")
        print("-" * 50)
        
        supabase_results = {
            "volumes_detected": 0,
            "service_accessible": False,
            "configuration_created": False
        }
        
        # 1. Detectar volúmenes Supabase
        try:
            result = subprocess.run(['docker', 'volume', 'ls'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                supabase_volumes = [line.split()[-1] for line in result.stdout.split('\n') 
                                 if 'supabase' in line.lower() and 'vigoleonrocks' in line.lower()]
                supabase_results["volumes_detected"] = len(supabase_volumes)
                print(f"1. Volúmenes Supabase detectados: {len(supabase_volumes)}")
                
                for vol in supabase_volumes:
                    print(f"   - {vol}")
                    
        except Exception as e:
            print(f"1. Error detectando volúmenes: {e}")
        
        # 2. Probar acceso a Supabase
        try:
            response = requests.get("http://localhost:54321", timeout=5)
            supabase_results["service_accessible"] = True
            print(f"2. Supabase accesible: SI (Status: {response.status_code})")
        except:
            print("2. Supabase accesible: NO")
        
        # 3. Crear configuración de integración
        integration_config = {
            "supabase_xl_integration": {
                "event_logging": {
                    "enabled": True,
                    "log_llm_requests": True,
                    "log_responses": True,
                    "log_performance_metrics": True
                },
                "model_management": {
                    "vigoleonrocks_models_tracking": True,
                    "quantum_states_storage": True,
                    "model_performance_analytics": True
                },
                "data_persistence": {
                    "conversation_history": True,
                    "user_preferences": True,
                    "system_metrics": True
                }
            },
            "endpoints": {
                "supabase_url": "http://localhost:54321",
                "supabase_key": "SUPABASE_ANON_KEY_PLACEHOLDER"
            }
        }
        
        try:
            with open("supabase_xl_final_config.json", "w") as f:
                json.dump(integration_config, f, indent=2)
            
            supabase_results["configuration_created"] = True
            print("3. Configuración de integración: CREADA")
            
        except Exception as e:
            print(f"3. Error creando configuración: {e}")
        
        self.results["supabase_integration"] = supabase_results
        return supabase_results
    
    def calculate_final_metrics(self):
        """Calcular métricas finales del ecosistema"""
        print("\nCÁLCULO DE MÉTRICAS FINALES")
        print("-" * 50)
        
        metrics = {
            "infrastructure_score": 0,
            "integration_score": 0,
            "overall_score": 0,
            "system_status": "UNKNOWN"
        }
        
        # Score de infraestructura (60 puntos máximo)
        infra_score = 0
        
        # RabbitMQ (20 puntos)
        if self.results["infrastructure_status"].get("rabbitmq", {}).get("accessible"):
            infra_score += 15
            queues = self.results["infrastructure_status"]["rabbitmq"].get("queues", {})
            if any(q.get("exists") for q in queues.values()):
                infra_score += 5
        
        # Ollama (20 puntos)
        if self.results["infrastructure_status"].get("ollama", {}).get("accessible"):
            infra_score += 15
            models = self.results["infrastructure_status"]["ollama"].get("models", {})
            if models.get("vigoleonrocks", 0) > 0:
                infra_score += 5
        
        # Servicios Docker (20 puntos)
        docker_health = self.results["infrastructure_status"].get("docker_services", {}).get("health_percentage", 0)
        infra_score += int((docker_health / 100) * 20)
        
        metrics["infrastructure_score"] = infra_score
        
        # Score de integración (40 puntos máximo)
        integration_score = 0
        
        # Flujo de mensajes (30 puntos)
        flow = self.results.get("integration_tests", {}).get("message_flow", {})
        if flow.get("message_sent"):
            integration_score += 10
        if flow.get("message_routed"):
            integration_score += 10
        if flow.get("response_received"):
            integration_score += 10
        
        # Supabase XL (10 puntos)
        supabase = self.results.get("supabase_integration", {})
        if supabase.get("volumes_detected", 0) > 0:
            integration_score += 3
        if supabase.get("service_accessible"):
            integration_score += 3
        if supabase.get("configuration_created"):
            integration_score += 4
        
        metrics["integration_score"] = integration_score
        
        # Score general
        metrics["overall_score"] = infra_score + integration_score
        
        # Estado del sistema
        if metrics["overall_score"] >= 90:
            metrics["system_status"] = "EXCELENTE"
        elif metrics["overall_score"] >= 75:
            metrics["system_status"] = "BUENO"
        elif metrics["overall_score"] >= 60:
            metrics["system_status"] = "REGULAR"
        elif metrics["overall_score"] >= 40:
            metrics["system_status"] = "DEGRADADO"
        else:
            metrics["system_status"] = "CRITICO"
        
        print(f"Score de infraestructura: {infra_score}/60")
        print(f"Score de integración: {integration_score}/40")
        print(f"Score general: {metrics['overall_score']}/100")
        print(f"Estado del sistema: {metrics['system_status']}")
        
        self.results["final_metrics"] = metrics
        return metrics
    
    def generate_recommendations(self):
        """Generar recomendaciones finales"""
        recommendations = []
        
        # Basado en infraestructura
        if not self.results["infrastructure_status"].get("rabbitmq", {}).get("accessible"):
            recommendations.append("CRITICO: Iniciar RabbitMQ - docker run -d --name rabbitmq-qbtc -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
        
        if not self.results["infrastructure_status"].get("ollama", {}).get("accessible"):
            recommendations.append("CRITICO: Iniciar Ollama con host binding - OLLAMA_HOST=0.0.0.0:11434 ollama serve")
        
        # Basado en integración
        flow = self.results.get("integration_tests", {}).get("message_flow", {})
        if flow.get("message_sent") and flow.get("message_routed") and not flow.get("response_received"):
            recommendations.append("ALTA: Iniciar Quantum Consumer - python quantum_core_consumer.py en segundo plano")
        
        # Basado en servicios
        docker_health = self.results["infrastructure_status"].get("docker_services", {}).get("health_percentage", 0)
        if docker_health < 75:
            recommendations.append("MEDIA: Verificar servicios Docker no funcionales y reiniciarlos")
        
        # Supabase
        if not self.results.get("supabase_integration", {}).get("service_accessible"):
            recommendations.append("BAJA: Considerar iniciar Supabase para persistencia de datos")
        
        self.results["recommendations"] = recommendations
        return recommendations
    
    def generate_final_report(self):
        """Generar reporte final completo"""
        report_file = f"qbtc_final_integration_report_{self.timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nREPORTE FINAL GENERADO")
        print("=" * 60)
        print(f"Archivo: {report_file}")
        
        # Resumen ejecutivo
        metrics = self.results["final_metrics"]
        recommendations = self.results["recommendations"]
        
        print(f"\nRESUMEN EJECUTIVO:")
        print(f"Estado del ecosistema: {metrics['system_status']}")
        print(f"Score general: {metrics['overall_score']}/100")
        print(f"Score infraestructura: {metrics['infrastructure_score']}/60")
        print(f"Score integración: {metrics['integration_score']}/40")
        
        # Flujo end-to-end
        flow = self.results.get("integration_tests", {}).get("message_flow", {})
        flow_status = "FUNCIONANDO" if flow.get("response_received") else "FALLIDO"
        print(f"Flujo end-to-end: {flow_status}")
        
        if flow.get("response_received"):
            print(f"Latencia: {flow.get('total_latency', 0):.2f}s")
        
        print(f"\nRecomendaciones críticas: {len([r for r in recommendations if 'CRITICO' in r])}")
        print(f"Total recomendaciones: {len(recommendations)}")
        
        return report_file
    
    def run_complete_integration(self):
        """Ejecutar integración completa"""
        print("QBTC FINAL INTEGRATION")
        print("=" * 60)
        print("Integración final completa del ecosistema desde la raíz")
        
        # Fase 1: Verificar infraestructura
        print("\nFASE 1: VERIFICACIÓN DE INFRAESTRUCTURA")
        self.verify_core_infrastructure()
        
        # Fase 2: Probar integración
        print("\nFASE 2: PRUEBAS DE INTEGRACIÓN")
        self.test_message_flow_comprehensive()
        
        # Fase 3: Integrar Supabase XL
        print("\nFASE 3: INTEGRACIÓN SUPABASE XL")
        self.integrate_supabase_final()
        
        # Fase 4: Calcular métricas
        print("\nFASE 4: MÉTRICAS FINALES")
        self.calculate_final_metrics()
        
        # Fase 5: Generar recomendaciones
        print("\nFASE 5: RECOMENDACIONES")
        recommendations = self.generate_recommendations()
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        # Fase 6: Reporte final
        print("\nFASE 6: REPORTE FINAL")
        report_file = self.generate_final_report()
        
        print(f"\nINTEGRACIÓN COMPLETADA - Ver: {report_file}")
        
        return self.results

def main():
    """Ejecutar integración final completa"""
    integration = QBTCFinalIntegration()
    results = integration.run_complete_integration()
    
    return results

if __name__ == "__main__":
    main()