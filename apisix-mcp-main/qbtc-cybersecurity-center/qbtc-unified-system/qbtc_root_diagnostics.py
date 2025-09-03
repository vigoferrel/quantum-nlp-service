#!/usr/bin/env python3
"""
QBTC Root Diagnostics
====================
Diagnóstico profundo de la raíz de problemas en el ecosistema.
Va directo al núcleo de los fallos de conectividad.
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
        
    def diagnose_rabbitmq_deep(self):
        """Diagnóstico profundo de RabbitMQ"""
        print("DIAGNÓSTICO PROFUNDO: RabbitMQ")
        print("-" * 40)
        
        issues = []
        
        # 1. Verificar proceso RabbitMQ
        rabbitmq_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'rabbitmq' in proc.info['name'].lower() or any('rabbitmq' in str(cmd).lower() for cmd in proc.info['cmdline'] or []):
                    rabbitmq_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': proc.info['cmdline']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print(f"Procesos RabbitMQ encontrados: {len(rabbitmq_processes)}")
        for proc in rabbitmq_processes:
            print(f"  PID {proc['pid']}: {proc['name']}")
        
        if not rabbitmq_processes:
            issues.append("CRITICO: No hay procesos RabbitMQ corriendo")
            self.critical_issues.append("RabbitMQ no está corriendo")
        
        # 2. Verificar contenedores Docker RabbitMQ
        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if result.returncode == 0:
                rabbitmq_containers = [line for line in result.stdout.split('\n') if 'rabbitmq' in line.lower()]
                print(f"Contenedores RabbitMQ: {len(rabbitmq_containers)}")
                for container in rabbitmq_containers:
                    print(f"  {container}")
                
                if not rabbitmq_containers:
                    issues.append("CRITICO: No hay contenedores RabbitMQ corriendo")
                    self.critical_issues.append("RabbitMQ container no está corriendo")
        except Exception as e:
            issues.append(f"Error verificando Docker: {e}")
        
        # 3. Probar conexión directa
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            print("Conexión RabbitMQ: EXITOSA")
            
            # Verificar colas específicas
            channel = connection.channel()
            
            required_queues = ['q_llm_requests', 'q_trading_requests', 'q_llm_responses', 'q_trading_signals']
            existing_queues = []
            
            for queue in required_queues:
                try:
                    result = channel.queue_declare(queue=queue, passive=True)
                    existing_queues.append(queue)
                    print(f"Cola {queue}: EXISTE")
                except:
                    print(f"Cola {queue}: NO EXISTE")
                    issues.append(f"Cola faltante: {queue}")
            
            connection.close()
            
            if len(existing_queues) < len(required_queues):
                self.critical_issues.append("Colas RabbitMQ incompletas")
                
        except Exception as e:
            print(f"Conexión RabbitMQ: FALLO ({e})")
            issues.append(f"CRITICO: No se puede conectar a RabbitMQ: {e}")
            self.critical_issues.append("RabbitMQ inaccesible")
        
        return issues
    
    def diagnose_ollama_deep(self):
        """Diagnóstico profundo de Ollama"""
        print("\nDIAGNÓSTICO PROFUNDO: Ollama")
        print("-" * 40)
        
        issues = []
        
        # 1. Verificar proceso Ollama
        ollama_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'ollama' in proc.info['name'].lower():
                    ollama_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print(f"Procesos Ollama: {len(ollama_processes)}")
        for proc in ollama_processes:
            print(f"  PID {proc['pid']}: {proc['name']}")
        
        if not ollama_processes:
            issues.append("CRITICO: Ollama no está corriendo")
            self.critical_issues.append("Ollama no está corriendo")
        
        # 2. Probar API de Ollama
        try:
            response = requests.get("http://localhost:11434/api/version", timeout=5)
            if response.status_code == 200:
                print("API Ollama: FUNCIONAL")
                version_info = response.json()
                print(f"Versión: {version_info.get('version', 'desconocida')}")
            else:
                issues.append(f"API Ollama responde pero con error: {response.status_code}")
        except Exception as e:
            print(f"API Ollama: FALLO ({e})")
            issues.append(f"CRITICO: Ollama API inaccesible: {e}")
            self.critical_issues.append("Ollama API inaccesible")
        
        # 3. Verificar modelos disponibles
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get('models', []))
                print(f"Modelos disponibles: {model_count}")
                
                vigoleonrocks_models = [m for m in models.get('models', []) if 'vigoleonrocks' in m['name']]
                print(f"Modelos vigoleonrocks: {len(vigoleonrocks_models)}")
                
                if not vigoleonrocks_models:
                    issues.append("No hay modelos vigoleonrocks disponibles")
                
            else:
                issues.append("No se pueden obtener modelos de Ollama")
        except Exception as e:
            issues.append(f"Error obteniendo modelos: {e}")
        
        return issues
    
    def diagnose_quantum_consumer_deep(self):
        """Diagnóstico profundo del Quantum Consumer"""
        print("\nDIAGNÓSTICO PROFUNDO: Quantum Consumer")
        print("-" * 40)
        
        issues = []
        
        # 1. Verificar si quantum_core_consumer.py existe
        consumer_file = "quantum_core_consumer.py"
        
        try:
            with open(consumer_file, 'r') as f:
                content = f.read()
                print(f"Script {consumer_file}: EXISTE ({len(content)} caracteres)")
                
                # Verificar imports críticos
                critical_imports = ['pika', 'requests', 'json']
                for imp in critical_imports:
                    if f"import {imp}" in content:
                        print(f"Import {imp}: OK")
                    else:
                        issues.append(f"Import faltante: {imp}")
                        
        except FileNotFoundError:
            print(f"Script {consumer_file}: NO EXISTE")
            issues.append(f"CRITICO: {consumer_file} no encontrado")
            self.critical_issues.append("Quantum consumer script faltante")
            return issues
        
        # 2. Verificar procesos consumer corriendo
        consumer_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline'] or []
                if any('quantum_core_consumer' in str(cmd) for cmd in cmdline):
                    consumer_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print(f"Procesos consumer activos: {len(consumer_processes)}")
        for proc in consumer_processes:
            print(f"  PID {proc['pid']}: {proc['name']}")
        
        if not consumer_processes:
            issues.append("Consumer no está corriendo")
        
        return issues
    
    def diagnose_message_flow(self):
        """Diagnóstico específico del flujo de mensajes"""
        print("\nDIAGNÓSTICO PROFUNDO: Flujo de Mensajes")
        print("-" * 40)
        
        issues = []
        
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
            channel = connection.channel()
            
            # 1. Verificar estado de colas
            test_queues = ['q_llm_requests', 'q_llm_responses']
            
            for queue in test_queues:
                try:
                    method = channel.queue_declare(queue=queue, passive=True)
                    message_count = method.method.message_count
                    consumer_count = method.method.consumer_count
                    
                    print(f"Cola {queue}:")
                    print(f"  Mensajes: {message_count}")
                    print(f"  Consumers: {consumer_count}")
                    
                    if queue == 'q_llm_requests' and consumer_count == 0:
                        issues.append("CRITICO: No hay consumers en q_llm_requests")
                        self.critical_issues.append("No hay consumers activos")
                    
                    if message_count > 10:
                        issues.append(f"Cola {queue} tiene {message_count} mensajes acumulados")
                    
                except Exception as e:
                    print(f"Cola {queue}: ERROR ({e})")
                    issues.append(f"Error accediendo cola {queue}: {e}")
            
            # 2. Probar envío directo de mensaje
            print("\nProbando envío directo...")
            
            test_message = {
                "message_id": f"root_test_{self.timestamp}",
                "request": "test message",
                "model": "vigoleonrocks:latest"
            }
            
            try:
                channel.basic_publish(
                    exchange='llm_requests',
                    routing_key='llm.request',
                    body=json.dumps(test_message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
                print("Mensaje de prueba enviado: OK")
                
                # Verificar si llegó a la cola
                time.sleep(2)
                method = channel.queue_declare(queue='q_llm_requests', passive=True)
                if method.method.message_count > 0:
                    print("Mensaje llegó a cola: OK")
                else:
                    issues.append("CRITICO: Mensaje no llegó a cola")
                    self.root_causes.append("Exchange o routing key mal configurado")
                    
            except Exception as e:
                issues.append(f"Error enviando mensaje: {e}")
                self.critical_issues.append("No se pueden enviar mensajes")
            
            connection.close()
            
        except Exception as e:
            issues.append(f"Error general en diagnóstico de flujo: {e}")
        
        return issues
    
    def identify_root_causes(self):
        """Identificar causas raíz de los problemas"""
        print("\nIDENTIFICACIÓN DE CAUSAS RAÍZ")
        print("=" * 50)
        
        # Análisis de causas raíz basado en issues críticos
        if "RabbitMQ no está corriendo" in self.critical_issues:
            self.root_causes.append("CAUSA RAÍZ: RabbitMQ no está iniciado - Requiere 'docker run rabbitmq:3-management'")
        
        if "RabbitMQ container no está corriendo" in self.critical_issues:
            self.root_causes.append("CAUSA RAÍZ: Container RabbitMQ no existe - Requiere inicialización de infraestructura")
        
        if "Ollama no está corriendo" in self.critical_issues:
            self.root_causes.append("CAUSA RAÍZ: Ollama no está iniciado - Requiere 'ollama serve'")
        
        if "No hay consumers activos" in self.critical_issues:
            self.root_causes.append("CAUSA RAÍZ: Quantum Consumer no se conectó a RabbitMQ - Verificar dependencias")
        
        if "RabbitMQ inaccesible