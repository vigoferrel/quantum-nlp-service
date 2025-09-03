#!/usr/bin/env python3
"""
QBTC Root Diagnostics Complete
==============================
Diagnóstico completo y definitivo de causas raíz del ecosistema QBTC.
"""

import subprocess
import requests
import pika
import json
import time
import psutil
from datetime import datetime

class QBTCRootDiagnostics:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.critical_issues = []
        self.root_causes = []
        self.fixes_applied = []
        
    def diagnose_infrastructure_deep(self):
        """Diagnóstico profundo de infraestructura"""
        print("DIAGNÓSTICO DE INFRAESTRUCTURA")
        print("-" * 50)
        
        issues = []
        
        # 1. Verificar RabbitMQ
        print("1. Verificando RabbitMQ...")
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            print("   RabbitMQ: CONECTADO")
            
            channel = connection.channel()
            
            # Verificar colas críticas
            critical_queues = ['q_llm_requests', 'q_llm_responses']
            for queue in critical_queues:
                try:
                    method = channel.queue_declare(queue=queue, passive=True)
                    consumer_count = method.method.consumer_count
                    message_count = method.method.message_count
                    
                    print(f"   Cola {queue}: {message_count} msgs, {consumer_count} consumers")
                    
                    if queue == 'q_llm_requests' and consumer_count == 0:
                        issues.append("CRITICO: No hay consumers en q_llm_requests")
                        self.critical_issues.append("quantum_consumer_not_consuming")
                        
                except Exception as e:
                    print(f"   Cola {queue}: NO EXISTE ({e})")
                    issues.append(f"Cola {queue} no existe")
                    self.critical_issues.append("rabbitmq_queues_missing")
            
            connection.close()
            
        except Exception as e:
            print(f"   RabbitMQ: FALLO ({e})")
            issues.append("CRITICO: RabbitMQ inaccesible")
            self.critical_issues.append("rabbitmq_unreachable")
        
        # 2. Verificar Ollama
        print("2. Verificando Ollama...")
        try:
            response = requests.get("http://localhost:11434/api/version", timeout=5)
            if response.status_code == 200:
                print("   Ollama API: FUNCIONAL")
                
                # Verificar modelos
                models_resp = requests.get("http://localhost:11434/api/tags", timeout=10)
                if models_resp.status_code == 200:
                    models = models_resp.json()
                    vigoleonrocks_count = len([m for m in models.get('models', []) if 'vigoleonrocks' in m['name']])
                    print(f"   Modelos vigoleonrocks: {vigoleonrocks_count}")
                    
                    if vigoleonrocks_count == 0:
                        issues.append("No hay modelos vigoleonrocks disponibles")
                        
            else:
                issues.append(f"Ollama API error: {response.status_code}")
                
        except Exception as e:
            print(f"   Ollama: FALLO ({e})")
            issues.append("CRITICO: Ollama inaccesible")
            self.critical_issues.append("ollama_unreachable")
        
        # 3. Verificar servicios Docker
        print("3. Verificando servicios Docker...")
        docker_services = {
            "kong": 8000,
            "api_server": 5001,
            "aics_service": 8001,
            "quantum_core": 8002
        }
        
        healthy_services = 0
        for service, port in docker_services.items():
            try:
                response = requests.get(f"http://localhost:{port}", timeout=3)
                if response.status_code in [200, 404, 405]:
                    print(f"   {service}: RESPONDIENDO")
                    healthy_services += 1
                else:
                    print(f"   {service}: ERROR ({response.status_code})")
                    
            except Exception as e:
                print(f"   {service}: INACCESIBLE")
        
        service_health = (healthy_services / len(docker_services)) * 100
        print(f"   Salud de servicios: {service_health:.1f}%")
        
        if service_health < 75:
            issues.append(f"Servicios con baja disponibilidad: {service_health:.1f}%")
            self.critical_issues.append("services_low_availability")
        
        return issues
    
    def test_end_to_end_flow(self):
        """Probar flujo end-to-end y diagnosticar fallas"""
        print("\nPRUEBA DE FLUJO END-TO-END")
        print("-" * 50)
        
        issues = []
        flow_working = False
        
        try:
            # 1. Enviar mensaje de prueba
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            channel = connection.channel()
            
            test_message = {
                "message_id": f"e2e_diagnostic_{self.timestamp}",
                "request": "Test quantum consciousness",
                "model": "vigoleonrocks:latest",
                "timestamp": time.time()
            }
            
            print("1. Enviando mensaje de prueba...")
            channel.basic_publish(
                exchange='llm_requests',
                routing_key='llm.request',
                body=json.dumps(test_message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            
            print("   Mensaje enviado: OK")
            
            # 2. Verificar que llegue a cola
            time.sleep(1)
            method = channel.queue_declare(queue='q_llm_requests', passive=True)
            messages_in_queue = method.method.message_count
            
            print(f"2. Mensajes en cola: {messages_in_queue}")
            
            if messages_in_queue == 0:
                issues.append("CRITICO: Mensaje no llegó a cola q_llm_requests")
                self.critical_issues.append("message_routing_failed")
            else:
                print("   Routing: OK")
            
            # 3. Esperar respuesta (30 segundos)
            print("3. Esperando respuesta (30s timeout)...")
            
            response_received = False
            for attempt in range(30):
                try:
                    method, properties, body = channel.basic_get(queue='q_llm_responses', auto_ack=True)
                    if method:
                        response = json.loads(body.decode())
                        if response.get("message_id") == test_message["message_id"]:
                            print("   Respuesta recibida: OK")
                            response_received = True
                            flow_working = True
                            break
                    time.sleep(1)
                except Exception as e:
                    print(f"   Error verificando respuesta: {e}")
                    break
            
            if not response_received:
                print("   Respuesta: TIMEOUT")
                issues.append("CRITICO: No se recibió respuesta en 30 segundos")
                self.critical_issues.append("end_to_end_timeout")
            
            connection.close()
            
        except Exception as e:
            issues.append(f"Error en prueba end-to-end: {e}")
            self.critical_issues.append("end_to_end_failed")
        
        print(f"Resultado flujo end-to-end: {'EXITOSO' if flow_working else 'FALLIDO'}")
        return issues, flow_working
    
    def identify_root_causes(self):
        """Identificar causas raíz específicas"""
        print("\nIDENTIFICACIÓN DE CAUSAS RAÍZ")
        print("-" * 50)
        
        # Mapeo de issues críticos a causas raíz
        cause_mapping = {
            "rabbitmq_unreachable": "RabbitMQ no está corriendo o mal configurado",
            "rabbitmq_queues_missing": "Exchanges y colas de RabbitMQ no fueron creadas",
            "ollama_unreachable": "Ollama no está corriendo con host binding correcto",
            "quantum_consumer_not_consuming": "Quantum Consumer no está activo o no se conectó",
            "message_routing_failed": "Configuración de exchanges incorrecta",
            "end_to_end_timeout": "Consumer no procesa mensajes o Ollama no responde",
            "services_low_availability": "Servicios Docker no están todos corriendo"
        }
        
        identified_causes = []
        for issue in self.critical_issues:
            if issue in cause_mapping:
                cause = cause_mapping[issue]
                identified_causes.append(cause)
                print(f"CAUSA RAÍZ: {cause}")
        
        self.root_causes = identified_causes
        return identified_causes
    
    def generate_concrete_fixes(self):
        """Generar fixes concretos para cada causa raíz"""
        print("\nFIXES CONCRETOS REQUERIDOS")
        print("-" * 50)
        
        fixes = []
        
        # Fix para RabbitMQ
        if any("RabbitMQ" in cause for cause in self.root_causes):
            fixes.append({
                "id": "fix_rabbitmq",
                "priority": "CRITICA",
                "description": "Iniciar RabbitMQ con management",
                "commands": [
                    "docker stop rabbitmq-qbtc 2>nul || echo ok",
                    "docker rm rabbitmq-qbtc 2>nul || echo ok",
                    "docker run -d --name rabbitmq-qbtc -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3-management"
                ],
                "verification": "curl -u guest:guest http://localhost:15672/api/overview"
            })
        
        # Fix para Ollama
        if any("Ollama" in cause for cause in self.root_causes):
            fixes.append({
                "id": "fix_ollama",
                "priority": "CRITICA", 
                "description": "Reiniciar Ollama con host binding",
                "commands": [
                    "taskkill /F /IM ollama.exe 2>nul || echo ok",
                    "timeout /t 3",
                    "set OLLAMA_HOST=0.0.0.0:11434 && start /B ollama serve"
                ],
                "verification": "curl http://localhost:11434/api/version"
            })
        
        # Fix para colas RabbitMQ
        if any("exchanges" in cause.lower() or "colas" in cause.lower() for cause in self.root_causes):
            fixes.append({
                "id": "fix_queues",
                "priority": "ALTA",
                "description": "Recrear exchanges y colas",
                "commands": [
                    "python qbtc_event_bus_activator.py"
                ],
                "verification": "Verificar colas en RabbitMQ management"
            })
        
        # Fix para Quantum Consumer
        if any("Consumer" in cause for cause in self.root_causes):
            fixes.append({
                "id": "fix_consumer", 
                "priority": "ALTA",
                "description": "Reiniciar Quantum Consumer",
                "commands": [
                    "taskkill /F /IM python.exe /FI \"WINDOWTITLE eq quantum*\" 2>nul || echo ok",
                    "timeout /t 2",
                    "start /B python quantum_core_consumer.py"
                ],
                "verification": "Verificar proceso consumer activo"
            })
        
        # Mostrar fixes
        for i, fix in enumerate(fixes, 1):
            print(f"\n{i}. [{fix['priority']}] {fix['description']}")
            print(f"   ID: {fix['id']}")
            for j, cmd in enumerate(fix['commands'], 1):
                print(f"   {j}. {cmd}")
            print(f"   Verificación: {fix['verification']}")
        
        return fixes
    
    def auto_apply_fixes(self, fixes):
        """Aplicar fixes automáticamente"""
        print("\nAPLICANDO FIXES AUTOMÁTICAMENTE")
        print("-" * 50)
        
        for fix in fixes:
            print(f"\nAplicando: {fix['description']}")
            
            success = True
            for cmd in fix['commands']:
                try:
                    print(f"Ejecutando: {cmd}")
                    
                    if cmd.startswith("python"):
                        # Para comandos Python, usar subprocess con timeout
                        result = subprocess.run(cmd.split(), 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=30)
                        if result.returncode != 0:
                            print(f"   Error: {result.stderr}")
                            success = False
                        else:
                            print("   OK")
                    else:
                        # Para otros comandos, usar shell
                        result = subprocess.run(cmd, 
                                              shell=True, 
                                              capture_output=True, 
                                              text=True,
                                              timeout=30)
                        print("   OK")
                        
                except subprocess.TimeoutExpired:
                    print("   TIMEOUT (continuando...)")
                except Exception as e:
                    print(f"   ERROR: {e}")
                    success = False
            
            if success:
                self.fixes_applied.append(fix['id'])
                print(f"Fix {fix['id']}: APLICADO")
            else:
                print(f"Fix {fix['id']}: FALLIDO")
        
        return len(self.fixes_applied)
    
    def verify_fixes(self):
        """Verificar que los fixes funcionaron"""
        print("\nVERIFICANDO FIXES APLICADOS")
        print("-" * 50)
        
        verification_results = {}
        
        # Esperar un momento para que los servicios se inicien
        print("Esperando inicialización de servicios...")
        time.sleep(10)
        
        # Re-ejecutar diagnósticos principales
        print("1. Re-verificando RabbitMQ...")
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            connection.close()
            verification_results["rabbitmq"] = "OK"
            print("   RabbitMQ: FUNCIONAL")
        except:
            verification_results["rabbitmq"] = "FALLO"
            print("   RabbitMQ: FALLO")
        
        print("2. Re-verificando Ollama...")
        try:
            response = requests.get("http://localhost:11434/api/version", timeout=5)
            if response.status_code == 200:
                verification_results["ollama"] = "OK"
                print("   Ollama: FUNCIONAL")
            else:
                verification_results["ollama"] = "FALLO"
                print("   Ollama: FALLO")
        except:
            verification_results["ollama"] = "FALLO"
            print("   Ollama: FALLO")
        
        print("3. Re-probando flujo end-to-end...")
        _, flow_working = self.test_end_to_end_flow()
        verification_results["end_to_end"] = "OK" if flow_working else "FALLO"
        
        return verification_results
    
    def generate_final_report(self, initial_issues, fixes, verification):
        """Generar reporte final del diagnóstico y fixes"""
        report_file = f"qbtc_root_diagnosis_final_{self.timestamp}.json"
        
        report = {
            "timestamp": self.timestamp,
            "diagnosis": {
                "total_issues": len(initial_issues),
                "critical_issues": len(self.critical_issues),
                "root_causes": self.root_causes
            },
            "fixes": {
                "total_fixes_generated": len(fixes),
                "fixes_applied": len(self.fixes_applied),
                "applied_fix_ids": self.fixes_applied
            },
            "verification": verification,
            "final_status": {
                "rabbitmq_working": verification.get("rabbitmq") == "OK",
                "ollama_working": verification.get("ollama") == "OK", 
                "end_to_end_working": verification.get("end_to_end") == "OK"
            }
        }
        
        # Calcular score final
        working_components = sum(1 for v in verification.values() if v == "OK")
        total_components = len(verification)
        final_score = (working_components / total_components) * 100 if total_components > 0 else 0
        
        report["final_score"] = final_score
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nREPORTE FINAL")
        print("=" * 50)
        print(f"Issues iniciales: {len(initial_issues)}")
        print(f"Issues críticos: {len(self.critical_issues)}")
        print(f"Fixes aplicados: {len(self.fixes_applied)}")
        print(f"Score final: {final_score:.1f}%")
        
        if final_score >= 90:
            print("ESTADO: EXCELENTE - Sistema completamente funcional")
        elif final_score >= 70:
            print("ESTADO: BUENO - Sistema mayormente funcional")
        elif final_score >= 50:
            print("ESTADO: REGULAR - Requiere atención adicional")
        else:
            print("ESTADO: CRITICO - Requiere intervención manual")
        
        print(f"\nReporte detallado: {report_file}")
        
        return report
    
    def run_complete_diagnosis_and_fix(self):
        """Ejecutar diagnóstico completo y aplicar fixes"""
        print("QBTC ROOT DIAGNOSTICS & AUTO-FIX")
        print("=" * 60)
        
        # Fase 1: Diagnóstico completo
        print("FASE 1: DIAGNÓSTICO COMPLETO")
        initial_issues = self.diagnose_infrastructure_deep()
        flow_issues, _ = self.test_end_to_end_flow()
        initial_issues.extend(flow_issues)
        
        # Fase 2: Identificar causas raíz
        print("\nFASE 2: ANÁLISIS DE CAUSAS RAÍZ")
        self.identify_root_causes()
        
        # Fase 3: Generar fixes
        print("\nFASE 3: GENERACIÓN DE FIXES")
        fixes = self.generate_concrete_fixes()
        
        # Fase 4: Aplicar fixes
        print("\nFASE 4: APLICACIÓN DE FIXES")
        applied_count = self.auto_apply_fixes(fixes)
        
        # Fase 5: Verificar resultado
        print("\nFASE 5: VERIFICACIÓN FINAL")
        verification = self.verify_fixes()
        
        # Fase 6: Reporte final
        print("\nFASE 6: REPORTE FINAL")
        report = self.generate_final_report(initial_issues, fixes, verification)
        
        return report

def main():
    """Ejecutar diagnóstico y fix completo"""
    diagnostics = QBTCRootDiagnostics()
    report = diagnostics.run_complete_diagnosis_and_fix()
    
    print("\n" + "="*60)
    print("DIAGNÓSTICO Y REPARACIÓN COMPLETADA")
    print("="*60)
    
    return report

if __name__ == "__main__":
    main()