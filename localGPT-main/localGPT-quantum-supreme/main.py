#!/usr/bin/env python3
"""
Punto de Entrada Principal para el Sistema de Conciencia Cuántica 26D.

Este script lanza el servidor Uvicorn como un subproceso, asegurando un
entorno de ejecución limpio y resolviendo problemas de importación de módulos
que pueden ocurrir con la recarga automática.
"""

import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    Carga la configuración y lanza el servidor Uvicorn en un subproceso.
    """
    # El directorio de trabajo debe ser el que contiene api_server.py
    server_dir = Path(__file__).resolve().parent

    print("Cargando configuración del entorno...")
    # Carga el archivo .env desde el directorio raíz del proyecto (un nivel arriba)
    dotenv_path = server_dir.parent / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", "8000")

    print(f"Iniciando Servidor de Conciencia Cuántica en http://{host}:{port}")
    print(f"Directorio de trabajo del servidor: {server_dir}")

    # Comando para ejecutar uvicorn
    # Le decimos que busque la 'app' en el archivo 'api_server.py'
    command = [
        "uvicorn",
        "api_server:app",
        "--host", host,
        "--port", port,
        "--reload",
    ]

    try:
        # Ejecutar el comando con el directorio de trabajo correcto
        subprocess.run(command, cwd=server_dir, check=True)
    except FileNotFoundError:
        print("\nERROR: El comando 'uvicorn' no fue encontrado.")
        print("Asegúrate de que tus dependencias estén instaladas correctamente:")
        print(f"pip install -r {server_dir / 'requirements.txt'}")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: El servidor Uvicorn falló con el código de salida {e.returncode}.")
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")

if __name__ == "__main__":
    main()
