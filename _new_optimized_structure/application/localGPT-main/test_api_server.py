from fastapi import FastAPI
from pydantic import BaseModel
import sys
from pathlib import Path

# --- Carga dinámica del QuantumCoreService ---
try:
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))
    from api_server import QuantumCoreService
except ImportError as e:
    print(f"Error: No se pudo importar QuantumCoreService. Asegúrate de que api_server.py esté en el mismo directorio.")
    print(f"Detalle del error: {e}")
    sys.exit(1)

# --- Definición del Modelo de Datos de la API ---
class QueryRequest(BaseModel):
    query: str

# --- Inicialización del Servidor y Servicio ---
app = FastAPI()
quantum_service = QuantumCoreService()

# --- Definición del Endpoint ---
@app.post("/api/quantum_query")
async def quantum_query(request: QueryRequest):
    """
    Endpoint que recibe una consulta, la procesa a través del Núcleo Cuántico
    y devuelve la solución en el formato esperado por el EvaluationRunner.
    """
    # Procesar la consulta a través del nuevo servicio del núcleo
    core_result = await quantum_service.process_query(request.query)

    if "error" in core_result:
        return {"solution": f"Error en el núcleo: {core_result['error']}"}

    # El runner espera la clave 'solution'. Mapeamos el campo 'response' del núcleo.
    # La 'response' contendrá el parche diff generado por la `code_generator_tool`.
    solution_text = core_result.get("response", "")
    return {"solution": solution_text}

@app.get("/")
def read_root():
    return {"status": "Servidor de prueba para QuantumConsciousnessCore26D está activo."}
