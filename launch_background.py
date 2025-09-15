#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Lanzador de Servidor en Segundo Plano
Utiliza el módulo subprocess de Python para un lanzamiento robusto y desacoplado.
"""

import subprocess
import sys
import os
import time

LOG_DIR = "logs"
SERVER_SCRIPT = "flask_app_fast.py"
STDOUT_LOG = os.path.join(LOG_DIR, "flask_fast.out.log")
STDERR_LOG = os.path.join(LOG_DIR, "flask_fast.err.log")

def main():
    """Lanza el servidor Flask en un proceso separado y en segundo plano."""
    # Asegurarse de que el directorio de logs existe
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Abrir los archivos de log
    # Usamos 'w' para truncar los logs en cada nuevo inicio
    stdout_log_file = open(STDOUT_LOG, 'w')
    stderr_log_file = open(STDERR_LOG, 'w')

    # La clave es usar Popen para no bloquear. El nuevo proceso se desacopla.
    # sys.executable asegura que usemos el mismo intérprete de Python.
    command = [sys.executable, "-u", SERVER_SCRIPT]

    print(f"Lanzando comando: {' '.join(command)}")
    print(f"La salida será redirigida a: {STDOUT_LOG}")
    print(f"Los errores serán redirigidos a: {STDERR_LOG}")

    # En Windows, Popen por sí solo ya es no bloqueante.
    # El proceso hijo continuará incluso si este script termina.
    process = subprocess.Popen(
        command, 
        stdout=stdout_log_file, 
        stderr=stderr_log_file, 
        text=True
    )

    print(f"✅ Servidor lanzado en segundo plano con PID: {process.pid}")
    print("El proceso continuará ejecutándose después de que este script finalice.")

if __name__ == "__main__":
    main()

