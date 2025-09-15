#!/usr/bin/env python3
"""
🛡️ VIGOLEONROCKS - Supervisor de Procesos
Un demonio robusto que lanza y monitorea el servidor Flask en un subproceso.
"""

import subprocess
import sys
import os
import time
import logging
import requests

# --- Configuración ---
LOG_DIR = "logs"
SERVER_SCRIPT = "flask_app_fast.py"
SUPERVISOR_LOG = os.path.join(LOG_DIR, "supervisor.log")
SERVER_STDOUT = os.path.join(LOG_DIR, "flask_fast.out.log")
SERVER_STDERR = os.path.join(LOG_DIR, "flask_fast.err.log")
HEALTH_CHECK_URL = "http://127.0.0.1:5000/health"

# --- Configuración de Logging del Supervisor ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(SUPERVISOR_LOG, mode='w'),
        logging.StreamHandler(sys.stdout) # También imprimir en consola
    ]
)

def launch_server_process():
    """Lanza el proceso del servidor Flask y devuelve el objeto del proceso."""
    logging.info(f"Lanzando el script del servidor: {SERVER_SCRIPT}")
    command = [sys.executable, "-u", SERVER_SCRIPT]
    
    # Abrir archivos de log para el servidor
    stdout_log = open(SERVER_STDOUT, 'w')
    stderr_log = open(SERVER_STDERR, 'w')

    # Popen es la clave para un proceso hijo no bloqueante
    process = subprocess.Popen(
        command,
        stdout=stdout_log,
        stderr=stderr_log,
        text=True
    )
    logging.info(f"Servidor lanzado como subproceso con PID: {process.pid}")
    return process

def main_loop():
    """El bucle principal del supervisor."""
    logging.info("Iniciando supervisor de procesos VIGOLEONROCKS.")
    server_process = launch_server_process()
    time.sleep(5) # Dar tiempo inicial para que el servidor arranque

    while True:
        # 1. Verificar si el proceso del servidor sigue vivo
        poll_result = server_process.poll()
        if poll_result is not None:
            logging.error(f"¡FALLO DETECTADO! El proceso del servidor ha terminado inesperadamente con código de salida: {poll_result}.")
            logging.info("Reiniciando el servidor en 10 segundos...")
            time.sleep(10)
            server_process = launch_server_process()
            continue # Volver al inicio del bucle

        # 2. Verificar la salud del endpoint HTTP
        try:
            response = requests.get(HEALTH_CHECK_URL, timeout=3)
            if response.status_code == 200:
                logging.info(f"Health Check ✅: Servidor OK (PID: {server_process.pid}, Status: {response.status_code})")
            else:
                logging.warning(f"Health Check ⚠️: El servidor respondió con status {response.status_code}")
        except requests.ConnectionError:
            logging.error("Health Check ❌: Fallo de conexión. El servidor no responde en el puerto.")
        except Exception as e:
            logging.error(f"Health Check ❌: Ocurrió un error inesperado: {e}")

        # Esperar para el próximo ciclo de monitoreo
        time.sleep(15)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info("Supervisor detenido manualmente.")
        sys.exit(0)

