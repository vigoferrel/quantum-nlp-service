#!/usr/bin/env python3
"""
QBTC Supabase Root Integration System
=====================================
Analiza e integra el volumen supabase_db_vigoleonrocks-ollama-model
desde la raíz del ecosistema QBTC para crear conectividad completa.
"""

import subprocess
import json
import requests
import time
import os
from pathlib import Path
from datetime import datetime

class SupabaseQBTCRootIntegrator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "timestamp": self.timestamp,
            "supabase_analysis": {},
            "docker_volumes": {},
            "service_integration": {},
            "benchmark_results": {},
            "errors": []
        }
        
    def analyze_docker_volumes(self):
        """Analizar volúmenes Docker relacionados con Supabase"""
        print("Analizando volúmenes Docker de Supabase...")
        
        try:
            # Obtener lista de volúmenes
            result = subprocess.run(['docker', 'volume', 'ls'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                volumes = result.stdout
                print(f"Volúmenes Docker encontrados:")
                
                supabase_volumes = []
                for line in volumes.split('\n'):
                    if 'supabase' in line.lower() or 'vigoleonrocks' in line.lower():
                        volume_name = line.split()[-1] if line.strip() else ""
                        if volume_name:
                            supabase_volumes.append(volume_name)
                            print(f"  - {volume_name}")
                            
                self.results["docker_volumes"]["supabase_volumes"] = supabase_volumes
                return supabase_volumes
            else:
                error = f"Error obteniendo volúmenes: {result.stderr}"
                print(f"[ERROR] {error}")
                self.results["errors"].append(error)
                return []
                
        except Exception as e:
            error = f"Error analizando volúmenes Docker: {e}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
            return []
    
    def inspect_supabase_volume(self, volume_name):
        """Inspeccionar contenido del volumen Supabase específico"""
        print(f"\nInspeccionando volumen: {volume_name}")
        
        try:
            # Inspeccionar el volumen
            result = subprocess.run(['docker', 'volume', 'inspect', volume_name],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                volume_info = json.loads(result.stdout)[0]
                mount_point = volume_info.get('Mountpoint', '')
                
                print(f"Mountpoint: {mount_point}")
                print(f"Driver: {volume_info.get('Driver', 'N/A')}")
                print(f"Created: {volume_info.get('CreatedAt', 'N/A')}")
                
                # Intentar explorar contenido usando contenedor temporal
                self.explore_volume_content(volume_name)
                
                self.results["supabase_analysis"][volume_name] = volume_info
                return volume_info
            else:
                error = f"Error inspeccionando volumen {volume_name}: {result.stderr}"
                print(f"[ERROR] {error}")
                self.results["errors"].append(error)
                return None
                
        except Exception as e:
            error = f"Error inspeccionando volumen {volume_name}: {e}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
            return None
    
    def explore_volume_content(self, volume_name):
        """Explorar contenido del volumen usando contenedor temporal"""
        print(f"Explorando contenido de {volume_name}...")
        
        try:
            # Crear contenedor temporal para explorar el volumen
            cmd = [
                'docker', 'run', '--rm', '-v', f'{volume_name}:/data',
                'alpine', 'find', '/data', '-type', 'f', '-name', '*.sql'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                print("Archivos SQL encontrados:")
                sql_files = result.stdout.strip().split('\n')
                for file in sql_files:
                    print(f"  - {file}")
                
                # Explorar algunos archivos clave
                for file in sql_files[:3]:  # Primeros 3 archivos
                    self.read_volume_file(volume_name, file.replace('/data', ''))
            else:
                print("No se encontraron archivos SQL")
                
                # Intentar buscar cualquier archivo
                cmd = [
                    'docker', 'run', '--rm', '-v', f'{volume_name}:/data',
                    'alpine', 'ls', '-la', '/data'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("Contenido del volumen:")
                    print(result.stdout)
                    
        except subprocess.TimeoutExpired:
            print("[WARNING] Timeout explorando volumen")
        except Exception as e:
            error = f"Error explorando volumen {volume_name}: {e}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
    
    def read_volume_file(self, volume_name, file_path):
        """Leer archivo específico del volumen"""
        try:
            cmd = [
                'docker', 'run', '--rm', '-v', f'{volume_name}:/data',
                'alpine', 'head', '-20', f'/data{file_path}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print(f"\nContenido de {file_path} (primeras 20 líneas):")
                print("-" * 50)
                print(result.stdout)
                print("-" * 50)
                
        except Exception as e:
            print(f"[WARNING] No se pudo leer archivo {file_path}: {e}")
    
    def check_supabase_services(self):
        """Verificar servicios de Supabase corriendo"""
        print("\nVerificando servicios de Supabase...")
        
        supabase_ports = [54321, 54322, 54323, 54324]  # Puertos comunes de Supabase
        
        for port in supabase_ports:
            try:
                response = requests.get(f"http://localhost:{port}", timeout=5)
                print(f"Puerto {port}: ACTIVO (Status: {response.status_code})")
                self.results["service_integration"][f"port_{port}"] = {
                    "status": "active",
                    "status_code": response.status_code
                }
            except requests.exceptions.ConnectionError:
                print(f"Puerto {port}: INACTIVO")
                self.results["service_integration"][f"port_{port}"] = {
                    "status": "inactive"
                }
            except Exception as e:
                print(f"Puerto {port}: ERROR - {e}")
                self.results["service_integration"][f"port_{port}"] = {
                    "status": "error",
                    "error": str(e)
                }
    
    def create_supabase_ollama_bridge(self):
        """Crear puente de integración Supabase-Ollama"""
        print("\nCreando puente de integración Supabase-Ollama...")
        
        bridge_config = {
            "supabase": {
                "url": "http://localhost:54321",
                "anon_key": "SUPABASE_ANON_KEY_PLACEHOLDER",
                "service_key": "SUPABASE_SERVICE_KEY_PLACEHOLDER"
            },
            "ollama": {
                "url": "http://localhost:11434",
                "models": [
                    "vigoleonrocks-ultra-minimal:latest",
                    "vigoleonrocks-basic:latest", 
                    "vigoleonrocks-medium:latest",
                    "vigoleonrocks-high-performance:latest",
                    "vigoleonrocks:latest",
                    "llama3.2:latest"
                ]
            },
            "endpoints": {
                "aics_service": "http://localhost:8001",
                "quantum_core": "http://localhost:8002"
            }
        }
        
        # Guardar configuración de puente
        with open("supabase_ollama_bridge.json", "w") as f:
            json.dump(bridge_config, f, indent=2)
        
        print("[OK] Configuración de puente guardada en supabase_ollama_bridge.json")
        
        # Crear script de integración
        integration_script = self.create_integration_script()
        
        with open("qbtc_supabase_integration.py", "w") as f:
            f.write(integration_script)
        
        print("[OK] Script de integración creado: qbtc_supabase_integration.py")
        
        self.results["service_integration"]["bridge_created"] = True
        
    def create_integration_script(self):
        """Crear script Python para integración"""
        return '''#!/usr/bin/env python3
"""
QBTC Supabase-Ollama Integration Bridge
======================================
"""

import requests
import json
import time

class QBTCIntegrationBridge:
    def __init__(self):
        with open("supabase_ollama_bridge.json", "r") as f:
            self.config = json.load(f)
    
    def test_ollama_connection(self):
        """Test Ollama connectivity"""
        try:
            response = requests.get(f"{self.config['ollama']['url']}/api/version")
            return response.status_code == 200
        except:
            return False
    
    def test_supabase_connection(self):
        """Test Supabase connectivity"""
        try:
            response = requests.get(f"{self.config['supabase']['url']}/rest/v1/")
            return response.status_code in [200, 401]  # 401 es OK sin auth
        except:
            return False
    
    def integrate_services(self):
        """Integrate Supabase with Ollama models"""
        print("Integrando servicios...")
        
        ollama_ok = self.test_ollama_connection()
        supabase_ok = self.test_supabase_connection()
        
        print(f"Ollama: {'OK' if ollama_ok else 'FAILED'}")
        print(f"Supabase: {'OK' if supabase_ok else 'FAILED'}")
        
        if ollama_ok and supabase_ok:
            print("[SUCCESS] Integración lista para usar")
            return True
        else:
            print("[WARNING] Algunos servicios no están disponibles")
            return False

if __name__ == "__main__":
    bridge = QBTCIntegrationBridge()
    bridge.integrate_services()
'''
    
    def test_integrated_endpoints(self):
        """Probar endpoints integrados después de las mejoras"""
        print("\nProbando endpoints integrados...")
        
        endpoints = [
            ("kong_gateway", "http://localhost:8000/"),
            ("api_server", "http://localhost:5001/"),
            ("aics_service", "http://localhost:8001/"),
            ("quantum_core", "http://localhost:8002/"),
            ("ollama", "http://localhost:11434/api/version")
        ]
        
        results = {}
        
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=10)
                status = "OK" if response.status_code in [200, 404, 405] else "ERROR"
                results[name] = {
                    "status": status,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
                print(f"  {name}: {status} (Status: {response.status_code})")
                
            except Exception as e:
                results[name] = {
                    "status": "FAILED",
                    "error": str(e)
                }
                print(f"  {name}: FAILED - {e}")
        
        self.results["benchmark_results"]["integrated_endpoints"] = results
        return results
    
    def generate_final_report(self):
        """Generar reporte final de integración"""
        print("\nGenerando reporte final...")
        
        report_file = f"qbtc_supabase_integration_report_{self.timestamp}.json"
        
        # Añadir resumen
        self.results["summary"] = {
            "total_supabase_volumes": len(self.results["docker_volumes"].get("supabase_volumes", [])),
            "integration_bridge_created": self.results["service_integration"].get("bridge_created", False),
            "total_errors": len(self.results["errors"]),
            "timestamp": self.timestamp
        }
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"[OK] Reporte guardado en: {report_file}")
        
        # Mostrar resumen en consola
        print("\n" + "="*60)
        print("RESUMEN DE INTEGRACIÓN SUPABASE-QBTC")
        print("="*60)
        print(f"Volúmenes Supabase encontrados: {self.results['summary']['total_supabase_volumes']}")
        print(f"Puente de integración creado: {'SI' if self.results['summary']['integration_bridge_created'] else 'NO'}")
        print(f"Total errores: {self.results['summary']['total_errors']}")
        
        if self.results["benchmark_results"].get("integrated_endpoints"):
            working_endpoints = sum(1 for ep in self.results["benchmark_results"]["integrated_endpoints"].values() 
                                  if ep.get("status") in ["OK"])
            total_endpoints = len(self.results["benchmark_results"]["integrated_endpoints"])
            print(f"Endpoints funcionales: {working_endpoints}/{total_endpoints}")
        
        return report_file

def main():
    """Función principal de integración"""
    print("QBTC Supabase Root Integration System")
    print("="*50)
    
    integrator = SupabaseQBTCRootIntegrator()
    
    # Paso 1: Analizar volúmenes Docker
    supabase_volumes = integrator.analyze_docker_volumes()
    
    # Paso 2: Inspeccionar volúmenes Supabase
    for volume in supabase_volumes:
        if 'vigoleonrocks-ollama-model' in volume:
            integrator.inspect_supabase_volume(volume)
    
    # Paso 3: Verificar servicios Supabase
    integrator.check_supabase_services()
    
    # Paso 4: Crear puente de integración
    integrator.create_supabase_ollama_bridge()
    
    # Paso 5: Probar endpoints integrados
    integrator.test_integrated_endpoints()
    
    # Paso 6: Generar reporte final
    report_file = integrator.generate_final_report()
    
    print(f"\n[COMPLETED] Integración finalizada. Ver: {report_file}")

if __name__ == "__main__":
    main()