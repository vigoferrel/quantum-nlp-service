from .base import BaseTool
import requests
import json
import os
import re

class UniversalOrchestratorTool(BaseTool):
    """
    Una herramienta maestra que orquesta otras herramientas y modelos de IA 
    para resolver consultas complejas usando una lógica de cascada.
    """
    name = "universal_orchestrator"
    description = "Resuelve una consulta del usuario utilizando una cascada de recursos: primero la búsqueda web de Brave, luego un LLM local (Ollama) si es necesario. Ideal para preguntas de conocimiento general y problemas de razonamiento."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "La pregunta o problema a resolver."
            }
        },
        "required": ["query"]
    }

    def __init__(self):
        super().__init__()
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.ollama_endpoint = "http://localhost:11434/api/generate"

    def execute(self, query: str) -> str:
        """Ejecuta la cascada de resolución."""
        
        # 1. Intentar con Brave Search API para conocimiento rápido
        if self.brave_api_key:
            try:
                headers = {'Accept': 'application/json', 'X-Subscription-Token': self.brave_api_key}
                params = {'q': query}
                response = requests.get('https://api.search.brave.com/res/v1/web/search', headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('web', {}).get('results', [])
                    if results:
                        # Para preguntas simples, un snippet puede ser suficiente
                        first_result = results[0]
                        return f"Respuesta de Brave: {first_result.get('title', '')} - {first_result.get('description', 'Sin descripción.')}"
            except requests.RequestException as e:
                # No es un error fatal, simplemente pasamos al siguiente paso
                pass

        # 2. Si Brave falla o no es concluyente, intentar con LLM Local (Ollama)
        try:
            prompt = {
                "model": "llama3",
                "prompt": f"Resuelve de forma concisa: {query}",
                "stream": False
            }
            response = requests.post(self.ollama_endpoint, json=prompt, timeout=30)
            if response.status_code == 200:
                full_response = response.text.strip().split('\n')
                final_data = json.loads(full_response[-1])
                return f"Respuesta del Núcleo Local (Ollama): {final_data['response']}"
        except requests.RequestException:
            # Fallback si Ollama no está disponible
            pass

        # 3. Fallback final si todas las capas fallan
        return "El orquestador universal no pudo resolver la consulta con los recursos disponibles."