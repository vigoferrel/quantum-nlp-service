#!/usr/bin/env python3
"""
Despachador de Herramientas para el CIO (Consciousness-enabled Intelligent Orchestrator).

Este módulo proporciona la clase `ToolDispatcher` que se encarga de
comunicarse con los distintos microservicios de herramientas (extremidades)
del sistema CIO.
"""

import os
import logging
import aiohttp
from typing import Dict, Any, Optional

# Configurar logging básico para el módulo
logger = logging.getLogger(__name__)

class ToolDispatcher:
    """
    Despachador centralizado para invocar herramientas externas.
    
    Mapea nombres de herramientas a URLs de servicios y realiza llamadas
    HTTP asíncronas para ejecutarlas.
    """
    
    def __init__(self):
        """
        Inicializa el despachador con un diccionario de herramientas.
        Las URLs se obtienen de variables de entorno o tienen valores por defecto
        para facilitar el desarrollo local.
        """
        self.tool_endpoints: Dict[str, str] = {
            # Ejemplo de mapeo de herramientas a URLs de servicios
            # En un entorno real, estas URLs vendrían de un sistema de descubrimiento
            # o variables de entorno.
            "trading_hft_service": os.getenv(
                "TRADING_HFT_SERVICE_URL", 
                "http://localhost:8001"
            ),
            "brave_web_search": os.getenv(
                "BRAVE_WEB_SEARCH_SERVICE_URL", 
                "http://localhost:8002"
            ),
            # Se pueden añadir más herramientas aquí
            # "math_solver": os.getenv("MATH_SOLVER_SERVICE_URL", "http://localhost:8003"),
        }
        logger.info("ToolDispatcher inicializado con %d herramientas.", len(self.tool_endpoints))

    async def dispatch(self, tool_name: str, query: str, **kwargs) -> Dict[str, Any]:
        """
        Despacha una consulta a una herramienta específica.
        
        Args:
            tool_name: El nombre identificador de la herramienta a invocar.
            query: La consulta o instrucción a enviar a la herramienta.
            **kwargs: Argumentos adicionales que pueden ser relevantes para la herramienta.
            
        Returns:
            Un diccionario con la respuesta de la herramienta o un mensaje de error.
        """
        # 1. Validar que la herramienta exista
        if tool_name not in self.tool_endpoints:
            error_msg = f"Herramienta '{tool_name}' no registrada en el despachador."
            logger.error(error_msg)
            return {
                "error": error_msg,
                "tool_requested": tool_name,
                "available_tools": list(self.tool_endpoints.keys())
            }

        # 2. Construir la URL del endpoint de ejecución
        service_url = self.tool_endpoints[tool_name]
        execute_endpoint = f"{service_url.rstrip('/')}/execute"
        
        # 3. Preparar el payload de la solicitud
        payload = {
            "query": query,
            **kwargs  # Incluir cualquier argumento adicional
        }

        # 4. Realizar la llamada HTTP asíncrona
        try:
            logger.info("Despachando herramienta '%s' a %s", tool_name, execute_endpoint)
            async with aiohttp.ClientSession() as session:
                async with session.post(execute_endpoint, json=payload, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info("Herramienta '%s' ejecutada con éxito.", tool_name)
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(
                            "Error %d al ejecutar herramienta '%s': %s", 
                            response.status, tool_name, error_text
                        )
                        return {
                            "error": f"Error HTTP {response.status}",
                            "message": error_text,
                            "tool": tool_name,
                            "status_code": response.status
                        }
        except aiohttp.ClientError as e:
            error_msg = f"Error de red al conectar con la herramienta '{tool_name}': {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "error": "Error de conexión",
                "message": error_msg,
                "tool": tool_name
            }
        except Exception as e:
            error_msg = f"Error inesperado al ejecutar la herramienta '{tool_name}': {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "error": "Error interno del despachador",
                "message": error_msg,
                "tool": tool_name
            }

# Instancia global para facilitar su uso
dispatcher = ToolDispatcher()

if __name__ == "__main__":
    # Este bloque permite probar el módulo de forma aislada
    import asyncio
    
    async def test_dispatch():
        """Función de prueba simple."""
        print("🧪 Probando ToolDispatcher...")
        # Esta prueba fallará porque los servicios no están levantados,
        # pero nos permite verificar que el código se ejecuta.
        result = await dispatcher.dispatch("trading_hft_service", "Consulta de prueba")
        print("Resultado:", result)
        
    asyncio.run(test_dispatch())