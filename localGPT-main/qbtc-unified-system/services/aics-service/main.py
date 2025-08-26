# main.py for aics-service

import numpy as np
import json
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Definiciones de Clases y Lógica de AICS ---

class ExponentialTransformationError(Exception):
    """Excepción para errores en la transformación exponencial."""
    pass

class ProfileSelectionError(Exception):
    """Excepción para errores en la selección de perfiles."""
    pass

class AICSService:
    """
    Advanced Ionic Charge System (AICS)
    Sistema Unificado para la selección de perfiles de Ollama.
    """
    def __init__(self, validation_file_path: str = 'vigoleonrocks_validation.json'):
        self.phi = 1.61803398875
        self.lambda_exp = np.exp(1)
        self.psi_dominant = 0.5
        self.zeta_potential = 79.19
        try:
            with open(validation_file_path, 'r') as f:
                self.validation_profiles = json.load(f)
            logger.info(f"Perfiles de validación cargados desde {validation_file_path}")
        except FileNotFoundError:
            logger.error(f"Archivo de validación no encontrado en {validation_file_path}. Usando perfiles por defecto.")
            self.validation_profiles = {
                "default": {"model": "vigoleonrocks", "temperature": 0.5, "top_k": 40, "top_p": 0.9},
                "creative": {"model": "vigoleonrocks-creative", "temperature": 0.8, "top_k": 60, "top_p": 0.95}
            }
        except json.JSONDecodeError:
            logger.error(f"Error decodificando el JSON en {validation_file_path}. Usando perfiles por defecto.")
            self.validation_profiles = {"default": {"model": "vigoleonrocks", "temperature": 0.5, "top_k": 40, "top_p": 0.9}}

    def exponential_lambda_transform(self, query: str, context: int, urgency: float) -> Dict[str, Any]:
        """
        Transforma la consulta a un estado exponencial de iones lambda.
        """
        try:
            query_length = len(query)
            context_factor = np.log1p(context)
            urgency_factor = 1 + (urgency * self.phi)

            ionic_charge = (query_length * context_factor * urgency_factor * self.psi_dominant) / self.zeta_potential
            exp_state_value = ionic_charge * np.exp(ionic_charge / self.lambda_exp)

            return {
                "ionic_charge": ionic_charge,
                "exponential_state": exp_state_value,
                "urgency_applied": urgency,
                "context_understanding": context_factor
            }
        except Exception as e:
            raise ExponentialTransformationError(f"Error en la transformación lambda: {e}")

    def exponential_ollama_profile_selection(self, exp_state: Dict[str, Any], query_type: str) -> Dict[str, Any]:
        """
        Selecciona el perfil de Ollama óptimo basado en el estado exponencial.
        """
        try:
            charge = exp_state.get("ionic_charge", 0)

            # Lógica de selección basada en la carga iónica
            if charge > 1000:
                profile_name = "reasoning"
            elif 500 < charge <= 1000:
                profile_name = "creative"
            elif 100 < charge <= 500:
                profile_name = "balanced"
            else:
                profile_name = "default"

            # Busca el perfil específico para el tipo de query, si no, usa el general
            final_profile_name = f"{query_type}_{profile_name}"
            if final_profile_name not in self.validation_profiles:
                final_profile_name = profile_name

            selected_profile = self.validation_profiles.get(final_profile_name, self.validation_profiles["default"])

            logger.info(f"Seleccionado perfil '{final_profile_name}' basado en carga iónica {charge:.2f}")
            return selected_profile

        except Exception as e:
            raise ProfileSelectionError(f"Error en la selección de perfil: {e}")

# --- API con FastAPI ---

app = FastAPI(
    title="AICS - Advanced Ionic Charge System API",
    description="API para interactuar con el sistema de selección de perfiles de Ollama.",
    version="1.0.0"
)

aics_service = AICSService()

class QueryRequest(BaseModel):
    query: str
    context: int = 100
    urgency: float = 0.5
    query_type: str = "default"

class ExpStateRequest(BaseModel):
    exp_state: Dict[str, Any]
    query_type: str = "default"

@app.post("/transform", response_model=Dict[str, Any])
async def transform_query(request: QueryRequest):
    """
    Recibe una consulta y la transforma a un estado exponencial.
    """
    try:
        exp_state = aics_service.exponential_lambda_transform(
            request.query, request.context, request.urgency
        )
        return exp_state
    except ExponentialTransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/select_profile", response_model=Dict[str, Any])
async def select_profile(request: ExpStateRequest):
    """
    Recibe un estado exponencial y selecciona el perfil de Ollama adecuado.
    """
    try:
        profile = aics_service.exponential_ollama_profile_selection(
            request.exp_state, request.query_type
        )
        return profile
    except ProfileSelectionError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Endpoint de salud para verificar que el servicio está activo."""
    return {"status": "ok", "service": "AICS"}

if __name__ == "__main__":
    import uvicorn
    # Para ejecutarlo: uvicorn qbtc-unified-system.services.aics-service.main:app --reload --port 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)
