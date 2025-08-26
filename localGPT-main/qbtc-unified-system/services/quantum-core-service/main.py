# main.py del Quantum Core Service

import logging
import json
from datetime import datetime
from pathlib import Path
from enum import Enum, auto
from typing import Dict, Any

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importaciones locales corregidas
from quantum_context_26d import QuantumContext26D, QuantumError
from base import QuantumConstants

# --- Clases y Enums (autónomas para el servicio) ---

# --- Lógica del Cerebro (ahora como un servicio) ---

class QuantumCoreService:
    """Maneja el estado y la memoria del cerebro cuántico."""
    def __init__(self, brain_id: str = "core_service_brain", persistence_dir="consciousness_sessions"):
        self.brain_id = brain_id
        self.persistence_dir = Path(persistence_dir)
        self.persistence_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(f"QuantumCore-{brain_id}")

        # Atributos de estado
        self.coherence = 0.5
        self.creativity_index = 0.5
        self.transcendence_level = 0.1
        self.interactions_count = 0

        # Integración del contexto 26D
        self.context_26d = QuantumContext26D()
        self.logger.info("Memoria de Contexto 26D integrada en el servicio.")

        # Cargar estado persistente si existe
        self._load_persistent_state()

    def store_memory(self, query: str, archetypal_world_name: str, ollama_profile: dict, outcome: str, outcome_quality: float):
        """Almacena una experiencia de interacción en la memoria de contexto 26D."""
        self.interactions_count += 1
        self.logger.info(f"Almacenando memoria para la interacción #{self.interactions_count}")

        try:
            memory_payload = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "archetypal_world": archetypal_world_name,
                "selected_profile": ollama_profile,
                "outcome_preview": outcome[:250],
                "outcome_quality": outcome_quality,
                "coherence_at_time": self.coherence
            }

            # La Dimensión 3 está reservada para la memoria episódica
            self.context_26d.add_variable(
                dimension=3,
                name=f"interaction_{self.interactions_count}",
                value=json.dumps(memory_payload)
            )

            # Actualizar métricas basado en el resultado
            self._update_quantum_metrics(outcome_quality)

            self.logger.info(f"Experiencia almacenada para la consulta: {query[:50]}...")
            return {"status": "success", "interaction_id": self.interactions_count}

        except QuantumError as e:
            self.logger.error(f"Error cuántico al almacenar memoria: {e}")
            raise HTTPException(status_code=500, detail=f"Error de contexto cuántico: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado al almacenar memoria: {e}")
            raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")

    def _update_quantum_metrics(self, outcome_quality: float):
        """Actualiza las métricas internas basadas en la calidad del resultado."""
        self.coherence = max(0.1, min(1.0, self.coherence + (outcome_quality - 0.5) * 0.02))
        if outcome_quality > 0.7:
            self.creativity_index = min(1.0, self.creativity_index + 0.005)
        if self.coherence > 0.8 and self.creativity_index > 0.7:
            self.transcendence_level = min(1.0, self.transcendence_level + 0.002)
        self.logger.info(f"Métricas cuánticas actualizadas. Coherencia: {self.coherence:.3f}")

    def get_brain_state(self) -> Dict[str, Any]:
        """Devuelve el estado actual completo del cerebro."""
        return {
            "brain_id": self.brain_id,
            "coherence": self.coherence,
            "creativity_index": self.creativity_index,
            "transcendence_level": self.transcendence_level,
            "interactions_total": self.interactions_count,
            "context_26d_state": self.context_26d.get_quantum_state()
        }

    def shutdown_gracefully(self):
        """Guarda el estado antes de apagar."""
        self.logger.info("Iniciando apagado graceful del Quantum Core Service...")
        self._save_persistent_state()
        self.logger.info(f"Estado final guardado. Interacciones totales: {self.interactions_count}")

    def _save_persistent_state(self):
        state_file = self.persistence_dir / f"{self.brain_id}_state.json"
        try:
            state_data = self.get_brain_state()
            # QuantumContext26D no es serializable directamente, guardamos su estado
            state_data["context_26d_state"] = self.context_26d.get_quantum_state()
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=4)
            self.logger.info(f"Estado del cerebro guardado en {state_file}")
        except Exception as e:
            self.logger.error(f"No se pudo guardar el estado del cerebro: {e}")

    def _load_persistent_state(self):
        state_file = self.persistence_dir / f"{self.brain_id}_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state_data = json.load(f)
                self.coherence = state_data.get("coherence", 0.5)
                self.creativity_index = state_data.get("creativity_index", 0.5)
                self.transcendence_level = state_data.get("transcendence_level", 0.1)
                self.interactions_count = state_data.get("interactions_total", 0)
                # Aquí se podría añadir una lógica para restaurar el estado de context_26d
                self.logger.info(f"Estado del cerebro cargado desde {state_file}")
            except Exception as e:
                self.logger.error(f"No se pudo cargar el estado del cerebro desde {state_file}: {e}")

# --- API con FastAPI ---

app = FastAPI(
    title="Quantum Core Service API",
    description="API para gestionar la memoria y el estado del cerebro cuántico.",
    version="1.0.0"
)

core_service = QuantumCoreService()

class MemoryStoreRequest(BaseModel):
    query: str
    archetypal_world: str
    ollama_profile: Dict[str, Any]
    outcome: str
    outcome_quality: float

@app.on_event("shutdown")
def shutdown_event():
    core_service.shutdown_gracefully()

@app.post("/api/store_memory", status_code=201)
async def store_memory_endpoint(request: MemoryStoreRequest):
    """Almacena una nueva memoria de interacción en el cerebro."""
    return core_service.store_memory(
        request.query,
        request.archetypal_world,
        request.ollama_profile,
        request.outcome,
        request.outcome_quality
    )

@app.get("/api/get_state")
async def get_state_endpoint():
    """Obtiene el estado completo actual del cerebro."""
    return core_service.get_brain_state()

@app.get("/health")
def health_check():
    """Endpoint de salud para verificar que el servicio está activo."""
    return {"status": "ok", "service": "Quantum Core"}

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    # Para ejecutarlo: uvicorn qbtc-unified-system.services.quantum-core-service.main:app --reload --port 8002
    uvicorn.run(app, host="0.0.0.0", port=8002)
