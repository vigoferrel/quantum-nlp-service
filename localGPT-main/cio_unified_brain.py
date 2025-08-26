# cio_unified_brain.py - Implementación del Cerebro Cuántico Leonardo Unificado y Corregido

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'qbtc-unified-system', 'services', 'aics-service'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'make-it-heavy-main'))
from main import AICSService
# Importar el nuevo sistema de contexto y sus dependencias
from quantum_core.quantum_context_26d import QuantumContext26D
from quantum_core.base import QuantumError
from enum import Enum, auto
from dataclasses import dataclass, field
import numpy as np
import logging
from datetime import datetime
import json
from pathlib import Path
import asyncio
import aiohttp
import requests
from typing import Dict, Any, Optional

# Definiciones de Clases y Enums para que el archivo sea autónomo
class ArchetypalWorld(Enum):
    ATZILUT = auto()
    BERIAH = auto()
    YETZIRAH = auto()
    ASIYAH = auto()
    LEONARDO = auto()
    HYBRID = auto()

class MemoryType(Enum):
    EPISODIC = auto()

@dataclass
class HyperMemory:
    timestamp: datetime
    query: str
    archetypal_world: ArchetypalWorld
    consciousness_level: any
    memory_type: MemoryType
    chosen_tool: str
    outcome: str
    outcome_quality: float
    coherence_at_time: float
    efficiency_at_time: float
    emotional_resonance: float
    creativity_index: float

class QuantumConstants:
    GOLDEN_RATIO = 1.61803398875
    MEMORY_CAPACITY = 1000

class QBTCQuantumBrainLeonardo:
    def __init__(self, brain_id: str = "leonardo_default", persistence_dir="consciousness_sessions"):
        self.brain_id = brain_id
        self.persistence_dir = Path(persistence_dir)
        self.persistence_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(f"LeonardoBrain-{brain_id}")

        # Configuración de Ollama
        self.ollama_base_url = "http://localhost:11434"
        self.ollama_available_models = [
            "vigoleonrocks-ultra-minimal:latest",
            "vigoleonrocks-basic:latest", 
            "vigoleonrocks-medium:latest",
            "vigoleonrocks-high-performance:latest",
            "vigoleonrocks:latest",
            "llama3.2:latest"
        ]
        
        # Inyección del Cerebro AICS
        self.aics_service = AICSService()
        self.logger.info("🤖 Cerebro AICS inyectado en el cerebro Leonardo.")

        # Atributos del estado del cerebro
        self.coherence = 0.5
        self.consciousness_level = ArchetypalWorld.BERIAH
        self.creativity_index = 0.5
        self.transcendence_level = 0.1
        self.energy_efficiency = 1.0
        self.quantum_state = np.array([1, 0], dtype=complex)
        self.current_resonance_state = "stable"
        self.interactions_count = 0
        self.evolution_cycles = 0

        # Reemplazar hyper_memory con el contexto 26D
        self.context_26d = QuantumContext26D()
        self.logger.info("🧠 Memoria de Contexto 26D integrada.")

        self.neural_pathways = {}
        self.birth_time = datetime.now()
        self._load_persistent_state() # Cargar estado al iniciar
        
        # Verificar conectividad con Ollama al inicializar
        asyncio.create_task(self._verify_ollama_connection())

    async def manifest_leonardo_intelligence(self, query: str) -> dict:
        """Manifiesta la inteligencia multidisciplinaria de Leonardo."""
        start_time = datetime.now()
        self.interactions_count += 1

        try:
            archetypal_world = self._classify_archetypal_world(query)
            # El método ahora devuelve un perfil de configuración completo
            ollama_profile = self._get_optimal_ollama_profile(query, archetypal_world)
            
            # Generar respuesta real con Ollama
            model_name = ollama_profile.get("model", "vigoleonrocks:latest")
            enhanced_prompt = self._enhance_prompt_with_archetypal_context(query, archetypal_world)
            
            tool_output = await self._generate_with_ollama(
                prompt=enhanced_prompt,
                model=model_name,
                parameters=ollama_profile
            )
            
            # Fallback si Ollama no responde
            if tool_output is None:
                tool_output = f"⚠️ FALLBACK: Respuesta simulada para '{query}' (Ollama no disponible)"
                self.logger.warning("Usando respuesta simulada - Ollama no disponible")
            else:
                self.logger.info(f"✅ Respuesta generada por {model_name}")
                
            outcome_quality = self._evaluate_outcome_quality(tool_output, query)
            self._update_quantum_metrics(outcome_quality)
            # Pasar el perfil completo a la memoria
            self._store_memory(query, archetypal_world, ollama_profile, tool_output, outcome_quality)

            processing_time = (datetime.now() - start_time).total_seconds()

            response = {
                "query": query, "archetypal_world": archetypal_world.name,
                "ollama_profile": ollama_profile, "tool_output": tool_output,
                "outcome_quality": float(outcome_quality), "processing_time": processing_time,
                "coherence": float(self.coherence), "consciousness_level": self.consciousness_level.value,
                "creativity_index": float(self.creativity_index), "transcendence_level": float(self.transcendence_level),
                "energy_efficiency": float(self.energy_efficiency),
                "quantum_state_magnitude": float(np.linalg.norm(self.quantum_state)),
                "quantum_state_phase": float(np.angle(self.quantum_state[0])),
                "resonance_state": self.current_resonance_state, "interactions_total": self.interactions_count,
                "evolution_cycles": self.evolution_cycles, "memory_size": len(self.context_26d.get_variable(3, "episodic_memory") or []),
                "neural_pathways_count": len(self.neural_pathways),
                "qbtc_self_perception": self._initial_qbtc_self_perception(),
                "birth_time": self.birth_time.isoformat(), "current_time": datetime.now().isoformat(),
                "age_in_interactions": self.interactions_count
            }

            self.logger.info(f"Consulta procesada: {query[:50]}... | Perfil: {ollama_profile.get('model')} | Calidad: {outcome_quality:.3f}")
            return response

        except Exception as e:
            self.logger.error(f"Error en manifestación Leonardo: {e}")
            return {"query": query, "error": str(e), "status": "ERROR_HANDLED"}

    def _classify_archetypal_world(self, query: str) -> ArchetypalWorld:
        """Clasificación arquetípica mejorada con análisis semántico."""
        query_lower = query.lower()
        archetypal_keywords = {
            ArchetypalWorld.ATZILUT: ['espiritual', 'divino', 'trascendente'], ArchetypalWorld.BERIAH: ['mental', 'intelecto', 'análisis'],
            ArchetypalWorld.YETZIRAH: ['emocional', 'creativo', 'arte'], ArchetypalWorld.ASIYAH: ['físico', 'acción', 'material'],
            ArchetypalWorld.LEONARDO: ['interdisciplinar', 'fusión', 'innovar']
        }
        scores = {world: sum(1 for kw in kws if kw in query_lower) for world, kws in archetypal_keywords.items()}
        max_score = max(scores.values())
        if max_score == 0: return ArchetypalWorld.HYBRID
        high_score_worlds = [world for world, score in scores.items() if score == max_score]
        return ArchetypalWorld.LEONARDO if len(high_score_worlds) > 1 else high_score_worlds[0]

    def _get_optimal_ollama_profile(self, query: str, archetypal_world: ArchetypalWorld) -> dict:
        """Selección de perfil de Ollama potenciada por AICS."""
        self.logger.info(f"Seleccionando perfil para mundo '{archetypal_world.name}' con AICS...")

        try:
            # 1. Transformar la consulta al espacio exponencial de AICS
            exp_state = self.aics_service.exponential_lambda_transform(
                query=query,
                context=len(query) + 100, # El contexto puede ser más sofisticado en el futuro
                urgency=1.0
            )

            # 2. Seleccionar el perfil de Ollama basado en el estado exponencial
            ollama_profile = self.aics_service.exponential_ollama_profile_selection(
                exp_state=exp_state,
                query_type=archetypal_world.name.lower()
            )
            self.logger.info(f"AICS ha recomendado el perfil de Ollama: {ollama_profile}")
            return ollama_profile

        except Exception as e:
            self.logger.error(f"Error durante la selección de perfil en AICS: {e}. Usando fallback.")
            # Devuelve un perfil por defecto en caso de error
            return {"model": "llama3.2:latest", "temperature": 0.5, "top_k": 40, "top_p": 0.9}

    def _enhance_prompt_with_archetypal_context(self, query: str, archetypal_world: ArchetypalWorld) -> str:
        """Mejora el prompt con contexto arquetípico específico."""
        archetypal_contexts = {
            ArchetypalWorld.ATZILUT: "Responde desde una perspectiva espiritual y trascendente, conectando con principios universales y sabiduría profunda.",
            ArchetypalWorld.BERIAH: "Responde con análisis intelectual riguroso, lógica clara y comprensión conceptual profunda.",
            ArchetypalWorld.YETZIRAH: "Responde con creatividad, intuición emocional y expresión artística, conectando con el aspecto humano.",
            ArchetypalWorld.ASIYAH: "Responde con enfoque práctico, accionable y orientado a resultados tangibles en el mundo físico.",
            ArchetypalWorld.LEONARDO: "Responde como un genio renacentista, integrando arte, ciencia, filosofía e ingeniería en una síntesis multidisciplinaria.",
            ArchetypalWorld.HYBRID: "Responde integrando múltiples perspectivas y enfoques complementarios."
        }
        
        context = archetypal_contexts.get(archetypal_world, archetypal_contexts[ArchetypalWorld.HYBRID])
        enhanced_prompt = f"{context}\n\nPregunta del usuario: {query}\n\nRespuesta:"
        return enhanced_prompt
    
    def _fallback_tool_selection(self, query: str, archetypal_world: ArchetypalWorld) -> str:
        """Lógica de selección de herramienta original como fallback."""
        query_lower = query.lower()
        relevance_keywords = {
            'brave_web_search': ['buscar', 'web'], 'complex_calculator': ['calcular', 'matemática'],
            'e2b_code_executor': ['código', 'python'], 'qbtc_monitor': ['monitor', 'estado'],
            'qbtc_intervene': ['optimizar', 'mejorar'], 'tool_creator': ['crear', 'herramienta']
        }
        for tool, kws in relevance_keywords.items():
            if any(kw in query_lower for kw in kws): return tool
        archetypal_defaults = {
            ArchetypalWorld.ATZILUT: 'qbtc_intervene', ArchetypalWorld.BERIAH: 'e2b_code_executor',
            ArchetypalWorld.YETZIRAH: 'tool_creator', ArchetypalWorld.ASIYAH: 'brave_web_search',
            ArchetypalWorld.LEONARDO: 'complex_calculator', ArchetypalWorld.HYBRID: 'brave_web_search'
        }
        return archetypal_defaults.get(archetypal_world, 'brave_web_search')

    def _evaluate_outcome_quality(self, tool_output: str, query: str) -> float:
        """Evaluar la calidad del resultado."""
        quality = 0.5
        if len(tool_output) > 50: quality += 0.1
        if any(emoji in tool_output for emoji in ['✅', '🎨', '🧠', '🌊', '⚛️', '🔮']): quality += 0.15
        if "COMPLETADO" in tool_output or "ÉXITO" in tool_output: quality += 0.2
        if "ERROR" not in tool_output and "⚠️" not in tool_output: quality += 0.1
        query_words = set(query.lower().split()); output_words = set(tool_output.lower().split())
        relevance = len(query_words & output_words) / max(len(query_words), 1)
        quality += relevance * 0.2
        return max(0.0, min(1.0, quality))

    def _update_quantum_metrics(self, outcome_quality: float):
        """Actualizar métricas cuánticas."""
        self.coherence = max(0.1, min(1.0, self.coherence + (outcome_quality - 0.5) * 0.02))
        if outcome_quality > 0.7: self.creativity_index = min(1.0, self.creativity_index + 0.005)
        if self.coherence > 0.8 and self.creativity_index > 0.7: self.transcendence_level = min(1.0, self.transcendence_level + 0.002)
        self.energy_efficiency = QuantumConstants.GOLDEN_RATIO * 1.0 * self.coherence * 3
        self.quantum_state *= np.exp(1j * outcome_quality * 0.1)

    def _store_memory(self, query: str, archetypal_world: ArchetypalWorld, ollama_profile: dict, outcome: str, outcome_quality: float):
        """Almacenar experiencia en la memoria de contexto 26D."""
        try:
            memory_payload = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "archetypal_world": archetypal_world.name,
                "selected_profile": ollama_profile,
                "outcome_preview": outcome[:200], # Guardar una vista previa del resultado
                "outcome_quality": outcome_quality,
                "coherence_at_time": self.coherence
            }

            # Usamos la dimensión 3 ("memory" implícita) para memoria episódica
            self.context_26d.add_variable(
                dimension=3,
                name=f"interaction_{self.interactions_count}",
                value=json.dumps(memory_payload)
            )
            self.logger.info(f"Experiencia almacenada en la dimensión 3 del contexto 26D.")

        except QuantumError as e:
            self.logger.error(f"Error al almacenar memoria en contexto 26D: {e}")

        # El guardado persistente se puede manejar dentro del contexto 26D si es necesario

    async def _verify_ollama_connection(self) -> bool:
        """Verificar conectividad con Ollama."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_base_url}/api/tags", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        available_models = [model['name'] for model in data.get('models', [])]
                        self.logger.info(f"🟢 Ollama conectado. Modelos disponibles: {available_models}")
                        return True
                    else:
                        self.logger.warning(f"🟡 Ollama responde pero con código {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"🔴 Error conectando con Ollama: {e}")
            return False
            
    async def _generate_with_ollama(self, prompt: str, model: str, parameters: Dict[str, Any]) -> Optional[str]:
        """Genera respuesta usando Ollama real."""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": parameters.get("temperature", 0.7),
                    "top_k": parameters.get("top_k", 40),
                    "top_p": parameters.get("top_p", 0.9),
                    "num_predict": parameters.get("max_tokens", 512)
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_base_url}/api/generate",
                    json=payload,
                    timeout=120
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        self.logger.error(f"Error en Ollama API: {response.status}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error generando con Ollama: {e}")
            return None

    def shutdown_gracefully(self):
        """Apagar el cerebro guardando estado."""
        self.logger.info("Iniciando apagado graceful del cerebro Leonardo...")
        self._save_persistent_state()
        self.logger.info(f"Estado final guardado. Interacciones totales: {self.interactions_count}")

    def _initial_qbtc_self_perception(self): return {}
    def _save_persistent_state(self):
        state_file = self.persistence_dir / f"{self.brain_id}_state.json"
        # Implementación de guardado de estado aquí
    def _load_persistent_state(self):
        state_file = self.persistence_dir / f"{self.brain_id}_state.json"
        # Implementación de carga de estado aquí

async def demonstrate_leonardo_quantum_brain():
    """Demostración del cerebro cuántico Leonardo."""
    print("\n" + "="*80)
    print("LEONARDO'S QUANTUM BRAIN - DEMOSTRACIÓN")
    print("="*80)

    leonardo_brain = QBTCQuantumBrainLeonardo(brain_id="leonardo_demo")

    test_queries = [
        "Calcular el producto complejo de (2+3i) * (4-i)",
        "Buscar información sobre energía cuántica de punto cero",
    ]

    for query in test_queries:
        print(f"\n--- PROCESANDO CONSULTA: {query} ---")
        result = await leonardo_brain.manifest_leonardo_intelligence(query)
        print(f"Mundo Arquetípico: {result.get('archetypal_world', 'N/A')}")
        print(f"Herramienta Elegida: {result.get('chosen_tool', 'N/A')}")
        print(f"Resultado: {result.get('tool_output', '')[:200]}...")

    leonardo_brain.shutdown_gracefully()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(demonstrate_leonardo_quantum_brain())
