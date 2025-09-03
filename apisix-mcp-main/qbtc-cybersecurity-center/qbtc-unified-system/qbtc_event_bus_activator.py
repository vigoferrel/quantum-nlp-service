#!/usr/bin/env python3
"""
QBTC Event Bus Activator
========================
Implementa el bus de eventos RabbitMQ para conectar microservicios
según el Plan de Fusión Arquitectónica.
"""

import pika
import json
import requests
import time
import subprocess
from datetime import datetime
from pathlib import Path

class QBTCEventBusActivator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.rabbitmq_url = "amqp://guest:guest@localhost:5672/"
        self.results = {
            "timestamp": self.timestamp,
            "rabbitmq_status": {},
            "queue_setup": {},
            "service_connections": {},
            "event_flow_test": {},
            "errors": []
        }
        
        # Configuración de RabbitMQ según arquitectura
        self.exchanges = {
            "llm_requests": {"type": "direct", "durable": True},
            "trading_requests": {"type": "direct", "durable": True},
            "responses": {"type": "topic", "durable": True}
        }
        
        self.queues = {
            "q_llm_requests": {"durable": True, "exchange": "llm_requests", "routing_key": "llm.request"},
            "q_trading_requests": {"durable": True, "exchange": "trading_requests", "routing_key": "trading.request"},
            "q_llm_responses": {"durable": True, "exchange": "responses", "routing_key": "llm.response"},
            "q_trading_signals": {"durable": True, "exchange": "responses", "routing_key": "trading.signal"}
        }
        
        # Servicios y endpoints
        self.services = {
            "api_server": "http://localhost:5001",
            "aics_service": "http://localhost:8001", 
            "quantum_core": "http://localhost:8002",
            "kong_gateway": "http://localhost:8000"
        }

    def check_rabbitmq_status(self):
        """Verificar estado de RabbitMQ"""
        print("Verificando estado de RabbitMQ...")
        
        try:
            # Verificar si RabbitMQ está corriendo
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            rabbitmq_running = 'rabbitmq' in result.stdout
            
            print(f"RabbitMQ Docker container: {'CORRIENDO' if rabbitmq_running else 'NO ENCONTRADO'}")
            
            if not rabbitmq_running:
                print("Intentando iniciar RabbitMQ...")
                self.start_rabbitmq()
            
            # Probar conexión
            connection = self.connect_rabbitmq()
            if connection:
                print("[OK] Conexión a RabbitMQ exitosa")
                self.results["rabbitmq_status"]["connection"] = "success"
                connection.close()
                return True
            else:
                print("[ERROR] No se pudo conectar a RabbitMQ")
                self.results["rabbitmq_status"]["connection"] = "failed"
                return False
                
        except Exception as e:
            error = f"Error verificando RabbitMQ: {e}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
            return False

    def start_rabbitmq(self):
        """Iniciar RabbitMQ usando Docker"""
        try:
            cmd = [
                'docker', 'run', '-d',
                '--name', 'rabbitmq-qbtc',
                '-p', '5672:5672',
                '-p', '15672:15672',
                '-e', 'RABBITMQ_DEFAULT_USER=guest',
                '-e', 'RABBITMQ_DEFAULT_PASS=guest',
                'rabbitmq:3-management'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[OK] RabbitMQ iniciado")
                time.sleep(10)  # Esperar a que inicie
                return True
            else:
                print(f"[WARNING] Error iniciando RabbitMQ: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error iniciando RabbitMQ: {e}")
            return False

    def connect_rabbitmq(self):
        """Conectar a RabbitMQ"""
        try:
            connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            return connection
        except Exception as e:
            print(f"[ERROR] Error conectando a RabbitMQ: {e}")
            return None

    def setup_exchanges_and_queues(self):
        """Configurar exchanges y colas según arquitectura"""
        print("\nConfigurando exchanges y colas...")
        
        connection = self.connect_rabbitmq()
        if not connection:
            return False
            
        try:
            channel = connection.channel()
            
            # Crear exchanges
            for exchange_name, config in self.exchanges.items():
                channel.exchange_declare(
                    exchange=exchange_name,
                    exchange_type=config["type"],
                    durable=config["durable"]
                )
                print(f"[OK] Exchange '{exchange_name}' creado")
                
            # Crear colas y bindings
            for queue_name, config in self.queues.items():
                channel.queue_declare(queue=queue_name, durable=config["durable"])
                channel.queue_bind(
                    exchange=config["exchange"],
                    queue=queue_name,
                    routing_key=config["routing_key"]
                )
                print(f"[OK] Cola '{queue_name}' creada y enlazada")
                
            self.results["queue_setup"]["status"] = "success"
            self.results["queue_setup"]["exchanges_created"] = len(self.exchanges)
            self.results["queue_setup"]["queues_created"] = len(self.queues)
            
            connection.close()
            return True
            
        except Exception as e:
            error = f"Error configurando RabbitMQ: {e}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
            connection.close()
            return False

    def test_service_endpoints(self):
        """Probar endpoints de servicios después de configurar eventos"""
        print("\nProbando endpoints de servicios...")
        
        results = {}
        
        for service_name, url in self.services.items():
            try:
                response = requests.get(url, timeout=10)
                status = "OK" if response.status_code in [200, 404, 405] else "ERROR"
                
                results[service_name] = {
                    "status": status,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
                
                print(f"  {service_name}: {status} (Status: {response.status_code})")
                
            except Exception as e:
                results[service_name] = {
                    "status": "FAILED",
                    "error": str(e)
                }
                print(f"  {service_name}: FAILED - {e}")
        
        self.results["service_connections"] = results
        return results

    def test_event_flow(self):
        """Simular flujo de eventos completo"""
        print("\nProbando flujo de eventos...")
        
        connection = self.connect_rabbitmq()
        if not connection:
            return False
            
        try:
            channel = connection.channel()
            
            # Crear mensaje de prueba
            test_message = {
                "message_id": f"test_{self.timestamp}",
                "timestamp": self.timestamp,
                "request": "What is quantum consciousness?",
                "model": "vigoleonrocks-ultra-minimal:latest",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            }
            
            # Publicar mensaje de prueba
            channel.basic_publish(
                exchange='llm_requests',
                routing_key='llm.request',
                body=json.dumps(test_message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Hacer mensaje persistente
                    content_type='application/json'
                )
            )
            
            print("[OK] Mensaje de prueba enviado a cola llm_requests")
            
            # Verificar que el mensaje llegue a la cola
            method, properties, body = channel.basic_get(queue='q_llm_requests', auto_ack=True)
            
            if method:
                received_message = json.loads(body.decode())
                print(f"[OK] Mensaje recibido de cola: {received_message['message_id']}")
                
                self.results["event_flow_test"] = {
                    "status": "success",
                    "message_sent": True,
                    "message_received": True,
                    "test_message_id": test_message["message_id"]
                }
            else:
                print("[WARNING] No se recibió mensaje de la cola")
                self.results["event_flow_test"] = {
                    "status": "partial",
                    "message_sent": True,
                    "message_received": False
                }
            
            connection.close()
            return True
            
        except Exception as e:
            error = f"Error probando flujo de eventos: {e}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
            connection.close()
            return False

    def create_service_connector_scripts(self):
        """Crear scripts para conectar servicios al bus de eventos"""
        print("\nCreando scripts de conexión de servicios...")
        
        # Script para LLM API Service
        llm_connector = '''#!/usr/bin/env python3
"""
LLM API Service - RabbitMQ Connector
"""
import pika
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class LLMServiceConnector:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
        self.channel = self.connection.channel()
    
    def publish_llm_request(self, request_data):
        message = {
            "message_id": f"llm_{int(time.time())}",
            "request": request_data.get("prompt", ""),
            "model": request_data.get("model", "vigoleonrocks:latest"),
            "parameters": request_data.get("parameters", {})
        }
        
        self.channel.basic_publish(
            exchange='llm_requests',
            routing_key='llm.request',
            body=json.dumps(message)
        )
        
        return message["message_id"]

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    connector = LLMServiceConnector()
    message_id = connector.publish_llm_request(request.json)
    
    return jsonify({
        "message_id": message_id,
        "status": "processing"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
'''
        
        with open("llm_service_connector.py", "w") as f:
            f.write(llm_connector)
            
        # Script para Quantum Core Service
        quantum_connector = '''#!/usr/bin/env python3
"""
Quantum Core Service - RabbitMQ Consumer
"""
import pika
import json
import requests

class QuantumCoreConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
        self.channel = self.connection.channel()
        
    def process_llm_request(self, ch, method, properties, body):
        try:
            message = json.loads(body.decode())
            print(f"Processing LLM request: {message['message_id']}")
            
            # Simular procesamiento con Ollama
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": message.get("model", "vigoleonrocks:latest"),
                    "prompt": message.get("request", ""),
                    "stream": False
                },
                timeout=30
            )
            
            if ollama_response.status_code == 200:
                result = ollama_response.json()
                
                # Publicar respuesta
                response_message = {
                    "message_id": message["message_id"],
                    "response": result.get("response", ""),
                    "status": "completed"
                }
                
                self.channel.basic_publish(
                    exchange='responses',
                    routing_key='llm.response',
                    body=json.dumps(response_message)
                )
                
                print(f"Response published for: {message['message_id']}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        self.channel.basic_consume(
            queue='q_llm_requests',
            on_message_callback=self.process_llm_request
        )
        
        print("Quantum Core Consumer started...")
        self.channel.start_consuming()

if __name__ == "__main__":
    consumer = QuantumCoreConsumer()
    consumer.start_consuming()
'''
        
        with open("quantum_core_consumer.py", "w") as f:
            f.write(quantum_connector)
            
        print("[OK] Scripts de conexión creados:")
        print("  - llm_service_connector.py")
        print("  - quantum_core_consumer.py")
        
        return True

    def generate_activation_report(self):
        """Generar reporte de activación del bus de eventos"""
        report_file = f"qbtc_event_bus_activation_{self.timestamp}.json"
        
        # Calcular métricas
        working_services = sum(1 for service in self.results.get("service_connections", {}).values() 
                             if service.get("status") == "OK")
        total_services = len(self.services)
        
        # Añadir resumen
        self.results["summary"] = {
            "rabbitmq_configured": self.results["queue_setup"].get("status") == "success",
            "exchanges_created": self.results["queue_setup"].get("exchanges_created", 0),
            "queues_created": self.results["queue_setup"].get("queues_created", 0),
            "event_flow_working": self.results["event_flow_test"].get("status") == "success",
            "services_responding": f"{working_services}/{total_services}",
            "total_errors": len(self.results["errors"]),
            "timestamp": self.timestamp
        }
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{'='*60}")
        print("REPORTE DE ACTIVACIÓN DEL BUS DE EVENTOS")
        print(f"{'='*60}")
        print(f"RabbitMQ configurado: {'SI' if self.results['summary']['rabbitmq_configured'] else 'NO'}")
        print(f"Exchanges creados: {self.results['summary']['exchanges_created']}")
        print(f"Colas creadas: {self.results['summary']['queues_created']}")
        print(f"Flujo de eventos: {'FUNCIONANDO' if self.results['summary']['event_flow_working'] else 'FALLO'}")
        print(f"Servicios respondiendo: {self.results['summary']['services_responding']}")
        print(f"Total errores: {self.results['summary']['total_errors']}")
        
        print(f"\n[OK] Reporte guardado en: {report_file}")
        return report_file

def main():
    """Función principal de activación"""
    print("QBTC Event Bus Activator")
    print("="*50)
    print("Implementando bus de eventos RabbitMQ según Plan de Fusión Arquitectónica")
    
    activator = QBTCEventBusActivator()
    
    # Paso 1: Verificar RabbitMQ
    if not activator.check_rabbitmq_status():
        print("[CRITICAL] No se pudo establecer conexión con RabbitMQ")
        return False
    
    # Paso 2: Configurar exchanges y colas
    if not activator.setup_exchanges_and_queues():
        print("[CRITICAL] No se pudieron configurar exchanges y colas")
        return False
    
    # Paso 3: Probar servicios
    activator.test_service_endpoints()
    
    # Paso 4: Probar flujo de eventos
    activator.test_event_flow()
    
    # Paso 5: Crear scripts de conexión
    activator.create_service_connector_scripts()
    
    # Paso 6: Generar reporte
    report_file = activator.generate_activation_report()
    
    print(f"\n[COMPLETED] Bus de eventos activado. Ver: {report_file}")
    print("\nPróximos pasos:")
    print("1. Ejecutar quantum_core_consumer.py en segundo plano")
    print("2. Reiniciar servicios con conectores de eventos")
    print("3. Probar flujo completo: Gateway → API → RabbitMQ → Quantum Core")
    
    return True

if __name__ == "__main__":
    main()