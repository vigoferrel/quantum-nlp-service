#!/usr/bin/env python3
"""
🌐 SERVER CLEAN - VERSIÓN LIMPIA
=================================
Servidor multimodal limpio y funcional
"""

import asyncio
import time
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Importar componentes del sistema
from advanced_conversational_engine import AdvancedConversationalEngine
from advanced_nlp_engine import nlp_engine
from quantum_core_26d_engine import QuantumCore26DEngine

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Advanced Multimodal Server",
    description="Servidor multimodal avanzado con NLP y núcleo cuántico",
    version="2.5.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
start_time = time.time()
engine = None

# Modelos Pydantic
class ConversationRequest(BaseModel):
    text: str = Field(..., description="Texto a procesar")
    session_id: str = Field(default_factory=lambda: f"session_{int(time.time())}")

@app.on_event("startup")
async def startup_event():
    """Inicializar el motor conversacional al arrancar"""
    global engine
    logger.info("🚀 Iniciando Advanced Multimodal Server...")
    
    try:
        # Inicializar motor conversacional
        engine = AdvancedConversationalEngine()
        logger.info("✅ Motor conversacional inicializado correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error inicializando motor: {e}")
        raise

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "🌐 Advanced Multimodal Server",
        "version": "2.5.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - start_time
    }

@app.get("/api/status")
async def get_status():
    """Obtener estado detallado del servidor"""
    return {
        "status": "healthy",
        "version": "2.5.0",
        "uptime": time.time() - start_time,
        "engine_ready": engine is not None,
        "nlp_engine_ready": nlp_engine is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/process_text")
async def process_text(request: ConversationRequest):
    """Procesar texto con análisis NLP y cuántico"""
    if not engine:
        raise HTTPException(status_code=503, detail="Motor no inicializado")
    
    start_time = time.time()
    
    try:
        # Procesar conversación
        from advanced_conversational_engine import ConversationRequest as EngineRequest
        engine_request = EngineRequest(
            text=request.text,
            session_id=request.session_id
        )
        response = await engine.process_conversation(engine_request)
        
        processing_time = time.time() - start_time
        
        # Extraer análisis NLP y cuántico de manera segura
        nlp_analysis = None
        quantum_analysis = None
        
        try:
            if response.success and hasattr(response, 'response') and hasattr(response.response, 'content'):
                content = response.response.content
                
                # Extraer NLP features
                if hasattr(content, 'nlp_features') and content.nlp_features:
                    nlp_analysis = {
                        "sentiment": {
                            "level": str(content.nlp_features.sentiment.level) if hasattr(content.nlp_features, 'sentiment') else "NEUTRAL",
                            "score": getattr(content.nlp_features.sentiment, 'score', 0.0)
                        },
                        "intent": {
                            "type": str(content.nlp_features.intent.intent) if hasattr(content.nlp_features, 'intent') else "UNKNOWN",
                            "confidence": getattr(content.nlp_features.intent, 'confidence', 0.0)
                        },
                        "entities": [
                            {
                                "text": entity.text,
                                "type": str(entity.type) if hasattr(entity, 'type') else "UNKNOWN",
                                "confidence": getattr(entity, 'confidence', 0.0)
                            }
                            for entity in getattr(content.nlp_features, 'entities', [])
                        ],
                        "readability_score": getattr(content.nlp_features, 'readability_score', 0.0),
                        "complexity_score": getattr(content.nlp_features, 'complexity_score', 0.0)
                    }
                
                # Extraer quantum features
                if hasattr(content, 'quantum_features') and content.quantum_features:
                    quantum_analysis = {
                        "quantum_score": getattr(content.quantum_features, 'quantum_score', 0.0),
                        "quantum_state": str(getattr(content.quantum_features, 'quantum_state', 'UNKNOWN')),
                        "dimension_scores": getattr(content.quantum_features, 'dimension_scores', {}),
                        "resonance_frequency": getattr(content.quantum_features, 'resonance_frequency', 888.0)
                    }
        except Exception as e:
            logger.warning(f"⚠️ Error extrayendo features: {e}")
        
        return {
            "success": response.success,
            "response": response.response.content if response.success else None,
            "processing_time": processing_time,
            "session_id": request.session_id,
            "nlp_analysis": nlp_analysis,
            "quantum_analysis": quantum_analysis,
            "context_26d": [dim.__dict__ for dim in response.context_26d_updated] if response.success else None
        }
        
    except Exception as e:
        logger.error(f"❌ Error procesando texto: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check básico"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - start_time,
        "version": "2.5.0"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    ADVANCED MULTIMODAL SERVER                               ║")
    print("║                    SERVIDOR MULTIMODAL AVANZADO                             ║")
    print("║                                                                              ║")
    print("║  [MOTOR CONVERSACIONAL AVANZADO + NLP + NÚCLEO CUÁNTICO]                  ║")
    print("║  [CAPACIDADES: TEXT, IMAGE, AUDIO, VIDEO, MULTIMODAL]                      ║")
    print("║  [INTEGRACIÓN: PYDANTIC + QUANTUM CORE + ADVANCED NLP]                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    uvicorn.run(
        "server_clean:app",
        host="0.0.0.0",
        port=5004,
        reload=False,
        log_level="info"
    )
