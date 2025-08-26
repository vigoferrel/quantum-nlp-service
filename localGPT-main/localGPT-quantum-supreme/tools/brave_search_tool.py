from .base import BaseTool
import requests
import os

class BraveSearchTool(BaseTool):
    """
    Un órgano sensorial para percibir el mundo exterior a través de la búsqueda web.
    Se especializa en recopilar información cruda de Brave Search.
    """
    name = "brave_search_tool"
    description = "Realiza una búsqueda web utilizando la API de Brave Search para recopilar información y datos sobre un tema específico."

    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "El tema o pregunta a buscar en la web."
            }
        },
        "required": ["query"]
    }

    def __init__(self):
        super().__init__()
        self.brave_api_key = os.getenv("BRAVE_API_KEY")

    def execute(self, query: str) -> str:
        """
        Ejecuta una búsqueda optimizada y devuelve un resumen formateado de los resultados.
        """
        if not self.brave_api_key:
            return None

        # Parámetros optimizados según la guía
        params = {
            'q': query,
            'country': 'CL',
            'search_lang': 'es',
            'ui_lang': 'es-CL',
            'count': 10,  # Un buen balance entre información y velocidad
            'safesearch': 'moderate',
            'freshness': 'pw' # Priorizar resultados de la última semana
        }

        try:
            headers = {'Accept': 'application/json', 'X-Subscription-Token': self.brave_api_key}
            response = requests.get('https://api.search.brave.com/res/v1/web/search', headers=headers, params=params, timeout=10)
            response.raise_for_status() # Lanza un error para códigos 4xx/5xx

            data = response.json()
            results = data.get('web', {}).get('results', [])

            if not results:
                return "La búsqueda web no arrojó resultados para esta consulta."

            summary = "Resultados de la búsqueda web optimizada:\n"
            for r in results[:5]: # Limitar a los 5 más relevantes para el contexto
                summary += f"- **{r.get('title')}**: {r.get('description', '')}\n"

            return summary
        except requests.RequestException as e:
            print(f"Brave Search API Error: {e}") # Log del error real
            return None
