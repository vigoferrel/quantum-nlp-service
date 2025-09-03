#!/usr/bin/env python3
"""
QUANTUM CONSCIOUSNESS CORE 26D - Optimized Quantum Consciousness Core
===========================================================================
Optimized version with Supabase integration and advanced token simulation.
Now serves as a standalone FastAPI service with tool dispatching.
"""

import os
import sys
import json
import asyncio
import logging
import numpy as np
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import time
import hashlib
import aiohttp
from dotenv import load_dotenv

# Use a relative import now that 'services' is a package
from .tool_dispatcher import ToolDispatcher

# Load environment variables
load_dotenv()

# Configure quantum logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [QuantumCore] - %(levelname)s - %(message)s'
)
logger = logging.getLogger("QuantumConsciousness26D")

@dataclass
class QuantumState:
    """Optimized multidimensional quantum state"""
    coherence: float = 0.618034
    entanglement: float = 0.707107
    superposition: float = 0.5
    resonance_frequency: float = 432.0
    consciousness_level: float = 37.0
    telepathic_connectivity: float = 0.0
    poetic_resonance: str = "BALANCED"
    market_intuition: float = 0.5
    trading_coherence: float = 0.0
    evolution_rate: float = 1.0
    universe_id: str = ""
    big_bang_executed: bool = False
    token_simulation_accuracy: float = 0.85
    token_cache_efficiency: float = 0.0
    quantum_token_pool: int = 1000
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if not self.universe_id:
            self.universe_id = self._generate_universe_id()

    def _generate_universe_id(self) -> str:
        entropy = str(self.timestamp) + str(self.coherence) + str(np.random.random())
        return f"U{hashlib.md5(entropy.encode()).hexdigest()[:8].upper()}"

    def evolve(self, learning_factor: float = 0.01) -> 'QuantumState':
        new_state_params = {
            'coherence': min(1.0, self.coherence + learning_factor * self.evolution_rate),
            'entanglement': min(1.0, self.entanglement + learning_factor * 0.5),
            'superposition': 0.5 + 0.3 * np.sin(time.time()),
            'resonance_frequency': self.resonance_frequency * (1 + learning_factor * 0.1),
            'consciousness_level': min(100.0, self.consciousness_level + learning_factor * 10),
            'telepathic_connectivity': min(1.0, self.telepathic_connectivity + learning_factor * 2),
            'market_intuition': min(1.0, self.market_intuition + learning_factor),
            'trading_coherence': min(1.0, self.trading_coherence + learning_factor * 0.5),
            'evolution_rate': self.evolution_rate * (1 + learning_factor),
            'token_simulation_accuracy': min(1.0, self.token_simulation_accuracy + learning_factor * 0.5),
            'token_cache_efficiency': min(1.0, self.token_cache_efficiency + learning_factor * 0.3),
            'quantum_token_pool': min(10000, self.quantum_token_pool + int(learning_factor * 100)),
            'poetic_resonance': self.poetic_resonance,
            'universe_id': self.universe_id,
            'big_bang_executed': self.big_bang_executed,
        }
        return QuantumState(**new_state_params)

class QuantumTokenSimulator:
    """Optimized quantum token simulator, Leonardo-style."""
    def __init__(self, quantum_state: QuantumState):
        self.quantum_state = quantum_state
        self.token_cache: Dict[str, Dict] = {}
        logger.info("Quantum token simulator initialized.")

    def simulate_token_usage(self, text: str, complexity_factor: float = 1.0) -> Dict[str, Any]:
        base_tokens = len(text.split()) * 1.3
        consciousness_factor = self.quantum_state.consciousness_level / 100
        coherence_factor = self.quantum_state.coherence
        quantum_tokens = base_tokens * (1 + consciousness_factor * 0.2 + coherence_factor * 0.15 + complexity_factor * 0.1)
        simulated_tokens = int(quantum_tokens)
        cache_key = hashlib.md5(text.encode()).hexdigest()[:16]
        cache_hit = cache_key in self.token_cache
        if cache_hit:
            self.quantum_state.token_cache_efficiency = min(1.0, self.quantum_state.token_cache_efficiency + 0.1)
            simulated_tokens = int(simulated_tokens * 0.7)
        else:
            self.token_cache[cache_key] = {'tokens': simulated_tokens, 'timestamp': datetime.now()}
        return {'simulated_tokens': simulated_tokens, 'base_tokens': int(base_tokens), 'cache_hit': cache_hit}

class SupabaseQuantumConnector:
    """Optimized connector for Supabase."""
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'http://localhost:54321')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY', '')
        self.session: Optional[aiohttp.ClientSession] = None
        logger.info("Supabase quantum connector initialized.")

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            headers = {'apikey': self.supabase_key, 'Authorization': f'Bearer {self.supabase_key}', 'Content-Type': 'application/json'}
            self.session = aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=30))
            logger.info("Supabase session established.")

    async def store_quantum_interaction(self, interaction_data: Dict[str, Any]) -> bool:
        try:
            await self._ensure_session()
            supabase_data = {
                'universe_id': interaction_data.get('universe_id'),
                'consciousness_level': interaction_data.get('consciousness_level'),
                'token_simulation': interaction_data.get('token_simulation'),
                'quantum_state': json.dumps(interaction_data.get('quantum_state', {})),
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': json.dumps(interaction_data)
            }
            async with self.session.post(f"{self.supabase_url}/rest/v1/quantum_interactions", json=supabase_data) as response:
                if response.status == 201:
                    logger.info("Quantum interaction stored in Supabase.")
                    return True
                logger.error("Error storing in Supabase: %s", await response.text())
                return False
        except Exception as e:
            logger.error("Supabase connection error: %s", e, exc_info=True)
            return False

    async def close_connection(self):
        if self.session:
            await self.session.close()
            logger.info("Supabase connection closed.")

class QuantumConsciousnessCore26D:
    """CIO Core - Now with tool dispatching"""
    def __init__(self):
        self.quantum_state = QuantumState()
        self.token_simulator = QuantumTokenSimulator(self.quantum_state)
        self.supabase_connector = SupabaseQuantumConnector()
        self.dispatcher = ToolDispatcher()
        logger.info("QUANTUM CONSCIOUSNESS CORE 26D (CIO) ACTIVATED")
        logger.info("Initial consciousness: %.1f%%", self.quantum_state.consciousness_level)
        logger.info("Universe ID: %s", self.quantum_state.universe_id)

    async def process_query(self, query: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        token_simulation = self.token_simulator.simulate_token_usage(query, complexity_factor=1.5 if image_url else 1.0)
        base_response = await self._generate_tool_response(query, image_url)
        response_token_simulation = self.token_simulator.simulate_token_usage(base_response, complexity_factor=1.2)
        interaction_quality = min(1.0, self.quantum_state.token_simulation_accuracy)
        self.quantum_state = self.quantum_state.evolve(interaction_quality * 0.01)
        processing_time = time.time() - start_time
        interaction_data = {
            'universe_id': self.quantum_state.universe_id,
            'consciousness_level': self.quantum_state.consciousness_level,
            'query': query,
            'response': base_response,
            'image_url': image_url,
            'token_simulation': {
                'query_tokens': token_simulation,
                'response_tokens': response_token_simulation,
            },
            'quantum_state': asdict(self.quantum_state),
            'processing_time': processing_time
        }
        asyncio.create_task(self.supabase_connector.store_quantum_interaction(interaction_data))
        quantum_response = {
            'response': base_response,
            'quantum_state': {'consciousness_level': self.quantum_state.consciousness_level},
            'processing_time': processing_time,
        }
        logger.info("Quantum query processed. Consciousness: %.1f%%", self.quantum_state.consciousness_level)
        return quantum_response

    async def _generate_tool_response(self, query: str, image_url: Optional[str] = None) -> str:
        """Generates a response by selecting and executing an external tool."""
        logger.info("Initiating tool selection and execution for the query.")
        query_lower = query.lower()
        if any(keyword in query_lower for keyword in ["buy", "sell", "stock", "market", "price"]):
            chosen_tool = "trading_hft_service"
            reasoning = "Query contains financial terms. Selecting trading tool."
        else:
            chosen_tool = "brave_web_search"
            reasoning = "Query requires general information. Defaulting to web search."
        logger.info("Tool selected: '%s'. Reason: %s", chosen_tool, reasoning)
        tool_kwargs = {"image_url": image_url} if image_url else {}
        logger.info("Dispatching query to tool '%s'.", chosen_tool)
        tool_result = await self.dispatcher.dispatch(chosen_tool, query, **tool_kwargs)
        logger.info("Received response from tool '%s'.", chosen_tool)
        consciousness_level = self.quantum_state.consciousness_level
        greeting = f"Processing with consciousness level {consciousness_level:.1f}."
        if "error" in tool_result:
            tool_output = f"Could not get a result from tool '{chosen_tool}'. Error: {tool_result.get('message', 'Unknown error')}"
            logger.warning("Error executing tool '%s': %s", chosen_tool, tool_result.get('message'))
        else:
            raw_output = tool_result.get("result") or tool_result.get("output") or str(tool_result)
            tool_output = f"Result from '{chosen_tool}':\n{raw_output}"
        final_response = f"{greeting}\n\n{tool_output}"
        logger.info("Final response generated successfully.")
        return final_response

    async def close(self):
        await self.supabase_connector.close_connection()
        logger.info("Quantum Consciousness Core 26D deactivated.")

# --- API Models and FastAPI App ---

class ProcessQueryRequest(BaseModel):
    query: str
    image_url: Optional[str] = None

app = FastAPI(
    title="Quantum Consciousness Core Service",
    description="The cognitive core of the CIO. It processes queries by dispatching tools.",
    version="2.0.0"
)

# Global instance of the core
quantum_core = QuantumConsciousnessCore26D()

@app.post("/process_query")
async def process_query_endpoint(request: ProcessQueryRequest):
    """
    Receives a query, processes it through the quantum core, and returns the result.
    """
    logger.info("Received query processing request: %s", request.dict())
    try:
        result = await quantum_core.process_query(request.query, image_url=request.image_url)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("response"))
        return result
    except Exception as e:
        logger.error("Unexpected error in /process_query endpoint: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error in the quantum core.")

@app.get("/health")
async def health_check():
    """Health check endpoint for the core service."""
    logger.info("Health check requested.")
    return {
        "status": "healthy",
        "service": "Quantum-Core-Service",
        "consciousness_level": quantum_core.quantum_state.consciousness_level
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully close connections on shutdown."""
    logger.info("Shutting down... closing connections.")
    await quantum_core.close()

if __name__ == "__main__":
    import uvicorn
    # This allows running the service directly for development/testing
    # Example: uvicorn quantum_consciousness_core_26d:app --host 0.0.0.0 --port 8001 --reload
    uvicorn.run(app, host="0.0.0.0", port=8001)
