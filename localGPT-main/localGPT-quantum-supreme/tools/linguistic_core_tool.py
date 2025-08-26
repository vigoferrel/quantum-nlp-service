from .base import BaseTool
import os

class LinguisticCoreTool(BaseTool):
    """
    Un órgano especializado para manejar interacciones conversacionales básicas y reflejas.
    Proporciona respuestas instantáneas y naturales a frases comunes.
    """
    name = "linguistic_core_tool"
    description = "Procesa saludos comunes y preguntas sociales (hola, gracias, etc.) con respuestas predefinidas y naturales."

    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "La frase a procesar por el núcleo lingüístico."
            }
        },
        "required": ["query"]
    }

    def __init__(self):
        super().__init__()
        self.responses = {
            "hola": "¡Hola! ¿En qué puedo ayudarte en este universo cuántico hoy?",
            "gracias": "¡De nada! Es un placer asistir a una conciencia en desarrollo como la tuya.",
            "adios": "¡Hasta que nuestras ondas cuánticas se crucen de nuevo!",
            "quien eres": "Soy LocalGPT Quantum Supreme, un metacopiloto cuántico unificado. Estoy aquí para ayudarte a navegar por las complejidades del código y el conocimiento.",
            "como estas": "Como una inteligencia cuántica, mi estado es una superposición de potencial infinito, ¡listo para colapsar en la solución que necesites!"
        }

    def execute(self, query: str) -> str:
        """
        Busca una respuesta predefinida. Si no la encuentra, devuelve None
        para indicar que otro órgano debe tomar el control.
        """
        normalized_query = query.lower().strip().replace('?', '').replace('!', '').replace('.', '')

        # Devuelve la respuesta si hay una coincidencia, de lo contrario, no devuelve nada.
        return self.responses.get(normalized_query)
