#!/usr/bin/env python3
"""
Test de búsqueda con Brave para el sistema cuántico
"""

import os
import sys
from pathlib import Path

# Configurar codificación para evitar errores
import locale
import codecs
try:
    # Intentar obtener la codificación del sistema
    encoding = locale.getpreferredencoding()
    if encoding is None:
        encoding = 'utf-8'
except:
    encoding = 'utf-8'

# Añadir el directorio de herramientas cuánticas al path
quantum_tools_path = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED\server\quantum-infrastructure\tools")
sys.path.insert(0, str(quantum_tools_path))

# Añadir el directorio localGPT-quantum-supreme al path
localgpt_path = Path(r"C:\Users\Hp\Desktop\vigosueldo\localGPT-main\localGPT-quantum-supreme")
sys.path.insert(0, str(localgpt_path))

def main():
    try:
        # Importar la herramienta de búsqueda de Brave
        print("Intentando importar herramienta de búsqueda de Brave...")

        # Importar base tool primero
        from base import BaseTool
        print("✅ BaseTool importado correctamente")

        # Importar brave search tool
        from brave_search_tool import BraveSearchTool
        print("✅ Herramienta de búsqueda de Brave importada correctamente")

        # Crear instancia de la herramienta
        brave_tool = BraveSearchTool()

        # Verificar si hay una clave API configurada
        brave_api_key = os.getenv("BRAVE_API_KEY")
        if not brave_api_key:
            print("Advertencia: No se encontró la clave API de Brave en las variables de entorno")
            print("Configura la variable BRAVE_API_KEY con tu clave de API de Brave Search")
            return False

        print(f"Clave API de Brave configurada: {brave_api_key[:10]}...")

        # Realizar una búsqueda de prueba
        print("Realizando búsqueda de prueba: 'tecnología cuántica chilena'")
        result = brave_tool.execute("tecnología cuántica chilena")

        if result:
            print("Búsqueda realizada exitosamente")
            print(f"Resultados:\n{result}")
            return True
        else:
            print("No se obtuvieron resultados de la búsqueda")
            return False

    except ImportError as e:
        print(f"Error al importar la herramienta de búsqueda: {e}")
        print("Asegúrate de que las rutas sean correctas y las dependencias estén instaladas")
        return False
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nTest de búsqueda con Brave completado exitosamente")
    else:
        print("\nTest de búsqueda con Brave fallido")
