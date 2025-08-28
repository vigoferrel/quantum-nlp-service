#!/usr/bin/env python3
"""
🚀 DESPLIEGUE RÁPIDO - SCRIPT GENERADO
"""

import subprocess
import time
import sys
import os

class DespliegueRapido:
    def __init__(self):
        self.puertos = {"frontend": 5003, "backend": 5004}
    
    def verificar_puertos(self):
        print("🔍 VERIFICANDO PUERTOS...")
        for servicio, puerto in self.puertos.items():
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', puerto))
                sock.close()
                
                if result == 0:
                    print(f"⚠️ Puerto {puerto} ({servicio}) está en uso")
                    self.liberar_puerto(puerto)
                else:
                    print(f"✅ Puerto {puerto} ({servicio}) disponible")
            except Exception as e:
                print(f"❌ Error verificando puerto {puerto}: {e}")
    
    def liberar_puerto(self, puerto: int):
        try:
            if sys.platform == "win32":
                result = subprocess.run(f"netstat -ano | findstr :{puerto}", shell=True, capture_output=True, text=True)
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            subprocess.run(f"taskkill /f /pid {pid}", shell=True)
                            print(f"✅ Proceso {pid} terminado para puerto {puerto}")
        except Exception as e:
            print(f"⚠️ No se pudo liberar puerto {puerto}: {e}")
    
    def iniciar_servicios(self):
        print("\n🚀 INICIANDO SERVICIOS OPTIMIZADOS...")
        
        print("📡 Iniciando backend optimizado...")
        backend_process = subprocess.Popen([sys.executable, "servidor_optimizado.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        print("🌐 Iniciando frontend optimizado...")
        frontend_process = subprocess.Popen([sys.executable, "frontend_optimizado.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)
        
        print("\n✅ SERVICIOS INICIADOS EXITOSAMENTE")
        print("🌐 Frontend: http://localhost:5003")
        print("📡 Backend: http://localhost:5004")
        print("🔍 Health Check: http://localhost:5004/health")
        
        return backend_process, frontend_process
    
    def ejecutar_warmup(self):
        print("\n🔥 EJECUTANDO WARM-UP AUTOMÁTICO...")
        
        try:
            import requests
            
            warmup_requests = [
                {"text": "Hola", "session_id": "warmup_1"},
                {"text": "Test de rendimiento", "session_id": "warmup_2"},
                {"text": "Análisis optimizado", "session_id": "warmup_3"}
            ]
            
            for i, request in enumerate(warmup_requests):
                start_time = time.time()
                response = requests.post("http://localhost:5004/api/process_text", json=request, timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    print(f"✅ Warm-up {i+1}: {(end_time - start_time):.3f}s")
                else:
                    print(f"❌ Warm-up {i+1}: Error {response.status_code}")
                    
                time.sleep(0.5)
                
        except Exception as e:
            print(f"⚠️ Error en warm-up: {e}")
    
    def desplegar_sistema(self):
        print("🚀 DESPLEGANDO SISTEMA OPTIMIZADO")
        print("=" * 50)
        
        self.verificar_puertos()
        backend_proc, frontend_proc = self.iniciar_servicios()
        time.sleep(2)
        self.ejecutar_warmup()
        
        print("\n🎯 SISTEMA DESPLEGADO Y OPTIMIZADO")
        print("=" * 50)
        print("✅ Frontend: http://localhost:5003")
        print("✅ Backend: http://localhost:5004")
        print("✅ Health: http://localhost:5004/health")
        print("\n💡 Presiona Ctrl+C para detener los servicios")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servicios...")
            backend_proc.terminate()
            frontend_proc.terminate()
            print("✅ Servicios detenidos")

if __name__ == "__main__":
    despliegue = DespliegueRapido()
    despliegue.desplegar_sistema()
