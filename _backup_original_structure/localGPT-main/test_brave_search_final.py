#!/usr/bin/env python3
"""
Test final de búsqueda con Brave para el sistema cuántico
"""

import os
import sys
from pathlib import Path

# Añadir el directorio de herramientas cuánticas al path
quantum_tools_path = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED\server\quantum-infrastructure\tools")
sys.path.insert(0, str(quantum_tools_path))

def main():
    try:
        print("Importando herramienta de busqueda de Brave...")

        # Importar base tool primero
        import importlib.util
        base_spec = importlib.util.spec_from_file_location("base", quantum_tools_path / "base.py")
        base_module = importlib.util.module_from_spec(base_spec)
        sys.modules["base"] = base_module
        base_spec.loader.exec_module(base_module)

        # Importar brave search tool
        brave_spec = importlib.util.spec_from_file_location("brave_search_tool", quantum_tools_path / "brave_search_tool.py")
        brave_module = importlib.util.module_from_spec(brave_spec)
        sys.modules["brave_search_tool"] = brave_module
        brave_spec.loader.exec_module(brave_module)

        BraveSearchTool = brave_module.BraveSearchTool
        print("Herramienta de busqueda de Brave importada correctamente")

        # Verificar si hay una clave API configurada
        brave_api_key = os.getenv("BRAVE_API_KEY")
        if not brave_api_key:
            print("No se encontro la clave API de Brave en las variables de entorno")
            print("Por favor, configura la variable BRAVE_API_KEY con tu clave de API de Brave Search")
            print("Ejemplo: set BRAVE_API_KEY=tu_clave_api_aqui (en Windows)")
            print("         export BRAVE_API_KEY=tu_clave_api_aqui (en Linux/Mac)")
            return False

        print("Clave API de Brave configurada correctamente")

        # Crear instancia de la herramienta
        brave_tool = BraveSearchTool()

        # Realizar una búsqueda de prueba
        print("Realizando busqueda de prueba: 'tecnologia cuantica'")
        result = brave_tool.execute("tecnologia cuantica")

        if result:
            print("Busqueda realizada exitosamente")
            print("Resultados:")
            print(result)
            return True
        else:
            print("No se obtuvieron resultados de la busqueda")
            return False

    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\nTest de busqueda con Brave completado exitosamente")
        print("El sistema puede realizar busquedas con Brave correctamente")
    else:
        print("\nTest de busqueda con Brave fallido")
        print("El sistema necesita configurar la clave API de Brave para funcionar")
