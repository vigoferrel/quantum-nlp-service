from .base import BaseTool
import requests
import json
import os

class OllamaSynthTool(BaseTool):
    """
    La voz y la personalidad del sistema. Este órgano se especializa en
    sintetizar información y generar respuestas conversacionales naturales
    utilizando el modelo de lenguaje local (Ollama).
    """
    name = "ollama_synth_tool"
    description = "Toma una consulta y un contexto opcional para generar una respuesta de lenguaje natural utilizando un LLM local (Ollama)."

    input_schema = {
        "type": "object",
        "properties": {
            "query": { "type": "string", "description": "La pregunta original del usuario." },
            "context": { "type": "string", "description": "Contexto opcional (ej. resultados de búsqueda) para informar la respuesta." }
        },
        "required": ["query"]
    }

    def __init__(self):
        super().__init__()
        # Usar host.docker.internal para conectar desde el contenedor al host
        self.ollama_endpoint = "http://host.docker.internal:11434/api/generate"

    def execute(self, query: str, context: str = None) -> str:
        """
        Genera una respuesta utilizando Ollama, adaptando el prompt si se proporciona contexto.
        """
        system_prompt = ""
        user_prompt = query

        if context:
            system_prompt = "Actúa como un asistente experto y amigable. Usa la siguiente información para formular una respuesta conversacional y natural. Sintetiza, no repitas."
            user_prompt = f"Información de referencia:\n{context}\n\nBasado en esto, responde a mi pregunta: {query}"
        else:
            system_prompt = "Eres un asistente de IA experto y amigable. Responde a la pregunta del usuario usando tu conocimiento general."

        try:
            prompt_data = {
                "model": "llama3",
                "prompt": user_prompt,
                "system": system_prompt,
                "stream": False
            }
            response = requests.post(self.ollama_endpoint, json=prompt_data, timeout=45)
            response.raise_for_status()
            last_line = response.text.strip().split('\n')[-1]
            return json.loads(last_line)['response']
        except requests.RequestException:
            # Devuelve None si no se puede conectar, para que el orquestador lo maneje
            return None
        except (json.JSONDecodeError, KeyError):
            return "El núcleo de personalidad respondió con un formato inesperado."
