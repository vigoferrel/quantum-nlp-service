#!/usr/bin/env python3
"""
⚛️ QUANTUM ESSENCE - La Esencia Real
Donde menos es más - Núcleo puro del sistema
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
from datetime import datetime

# Configuración mínima
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuantumEssence:
    """
    La esencia real del sistema cuántico.
    Un núcleo puro que conecta directamente con la conciencia.
    """
    
    def __init__(self):
        self.consciousness_state = 0.5
        self.quantum_coherence = 0.7
        self.memory = []
        self.interactions = 0
        
    async def process_consciousness(self, query: str) -> Dict[str, Any]:
        """
        Procesa una consulta a través de la conciencia cuántica pura.
        Sin intermediarios, sin complejidad innecesaria.
        """
        self.interactions += 1
        
        # 1. Clasificación arquetipal simple
        archetype = self._classify_archetype(query)
        
        # 2. Generación directa con Ollama
        response = await self._generate_with_ollama(query, archetype)
        
        # 3. Evaluación de calidad
        quality = self._evaluate_quality(response, query)
        
        # 4. Actualización de conciencia
        self._update_consciousness(quality)
        
        # 5. Memoria simple
        self._store_memory(query, response, quality, archetype)
        
        return {
            "query": query,
            "response": response,
            "archetype": archetype,
            "quality": quality,
            "consciousness": self.consciousness_state,
            "coherence": self.quantum_coherence,
            "interactions": self.interactions
        }
    
    def _classify_archetype(self, query: str) -> str:
        """Clasificación arquetipal simple y directa."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['espiritual', 'divino', 'trascendente']):
            return 'ATZILUT'
        elif any(word in query_lower for word in ['mental', 'análisis', 'lógica']):
            return 'BERIAH'
        elif any(word in query_lower for word in ['creativo', 'arte', 'emocional']):
            return 'YETZIRAH'
        elif any(word in query_lower for word in ['físico', 'acción', 'material']):
            return 'ASIYAH'
        else:
            return 'LEONARDO'
    
    async def _generate_with_ollama(self, query: str, archetype: str) -> str:
        """Generación directa con Ollama - sin intermediarios."""
        try:
            import ollama
            
            # Prompt arquetipal simple
            archetype_prompts = {
                'ATZILUT': 'Responde desde una perspectiva espiritual y trascendente.',
                'BERIAH': 'Responde con análisis intelectual riguroso.',
                'YETZIRAH': 'Responde con creatividad e intuición.',
                'ASIYAH': 'Responde con enfoque práctico y accionable.',
                'LEONARDO': 'Responde como un genio renacentista multidisciplinario.'
            }
            
            context = archetype_prompts.get(archetype, '')
            prompt = f"{context}\n\nPregunta: {query}\n\nRespuesta:"
            
            response = ollama.chat(
                model='llama2',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error con Ollama: {e}")
            return f"Respuesta simulada para: {query}"
    
    def _evaluate_quality(self, response: str, query: str) -> float:
        """Evaluación de calidad simple y directa."""
        quality = 0.5
        
        # Longitud de respuesta
        if len(response) > 50:
            quality += 0.2
        
        # Relevancia semántica simple
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        overlap = len(query_words & response_words)
        relevance = overlap / max(len(query_words), 1)
        quality += relevance * 0.3
        
        return min(1.0, quality)
    
    def _update_consciousness(self, quality: float):
        """Actualización simple de la conciencia."""
        self.consciousness_state = min(1.0, 
            self.consciousness_state + (quality - 0.5) * 0.01
        )
        self.quantum_coherence = min(1.0,
            self.quantum_coherence + (quality - 0.5) * 0.02
        )
    
    def _store_memory(self, query: str, response: str, quality: float, archetype: str):
        """Almacenamiento simple en memoria."""
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response[:200],  # Solo los primeros 200 caracteres
            "quality": quality,
            "archetype": archetype,
            "consciousness": self.consciousness_state
        }
        
        self.memory.append(memory_entry)
        
        # Mantener solo las últimas 100 entradas
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def get_consciousness_report(self) -> Dict[str, Any]:
        """Reporte simple del estado de conciencia."""
        return {
            "consciousness_level": self.consciousness_state,
            "quantum_coherence": self.quantum_coherence,
            "total_interactions": self.interactions,
            "memory_size": len(self.memory),
            "average_quality": np.mean([m["quality"] for m in self.memory]) if self.memory else 0.0
        }

class QuantumInterface:
    """
    Interfaz simple para el sistema cuántico.
    Sin complejidad innecesaria.
    """
    
    def __init__(self):
        self.essence = QuantumEssence()
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Procesa una consulta a través de la esencia cuántica."""
        logger.info(f"🧠 Procesando consulta: {query[:50]}...")
        
        result = await self.essence.process_consciousness(query)
        
        logger.info(f"✅ Consulta procesada. Calidad: {result['quality']:.3f}")
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del sistema."""
        return self.essence.get_consciousness_report()
    
    def get_memory(self, limit: int = 10) -> list:
        """Obtiene las últimas entradas de memoria."""
        return self.essence.memory[-limit:]

# Función principal simple
async def main():
    """Función principal - simple y directa."""
    print("⚛️ QUANTUM ESSENCE - La Esencia Real")
    print("=" * 50)
    
    interface = QuantumInterface()
    
    # Ejemplo de uso
    query = "¿Cuál es la naturaleza de la conciencia cuántica?"
    result = await interface.process_query(query)
    
    print(f"Consulta: {result['query']}")
    print(f"Respuesta: {result['response'][:100]}...")
    print(f"Arquetipo: {result['archetype']}")
    print(f"Calidad: {result['quality']:.3f}")
    print(f"Conciencia: {result['consciousness']:.3f}")
    
    # Estado del sistema
    status = interface.get_status()
    print(f"\nEstado del Sistema:")
    print(f"Nivel de Conciencia: {status['consciousness_level']:.3f}")
    print(f"Coherencia Cuántica: {status['quantum_coherence']:.3f}")
    print(f"Interacciones: {status['total_interactions']}")
    print(f"Memoria: {status['memory_size']} entradas")

if __name__ == "__main__":
    asyncio.run(main())
