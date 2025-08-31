#!/usr/bin/env python3
"""
Test de búsqueda con Brave usando la clave API configurada
"""

import os
import sys
import json
from pathlib import Path

# Configurar la clave API de Brave desde el archivo de configuración MCP
mcp_config_path = Path(r"C:\Users\Hp\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\mcp_settings.json")

try:
    with open(mcp_config_path, 'r') as f:
        mcp_config = json.load(f)

    brave_api_key = mcp_config.get('mcpServers', {}).get('brave-search', {}).get('env', {}).get('BRAVE_API_KEY')

    if brave_api_key:
        os.environ['BRAVE_API_KEY'] = brave_api_key
        print("Clave API de Brave configurada correctamente desde MCP")
    else:
        print("No se encontró la clave API de Brave en la configuración MCP")
        sys.exit(1)

except Exception as e:
    print(f"Error al leer la configuración MCP: {e}")
    sys.exit(1)

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
            return False

        print("Clave API de Brave configurada correctamente")

        # Crear instancia de la herramienta
        brave_tool = BraveSearchTool()

        # Realizar una búsqueda de prueba
        print("Realizando busqueda de prueba: 'tecnologia cuantica chilena'")
        result = brave_tool.execute("tecnologia cuantica chilena")

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
