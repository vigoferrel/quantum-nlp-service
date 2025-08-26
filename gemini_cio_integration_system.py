#!/usr/bin/env python3
"""
🚀 GEMINI CIO INTEGRATION SYSTEM
Sistema que integra Gemini 2.5 Pro con el stack CIO completo ya desarrollado:
- CIO Unified Brain con Cache Iónica
- Quantum Context 26D
- AICS Service
- Membrana Iónica
- Kernel Cuántico
"""

import asyncio
import time
import json
import aiohttp
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime
import hashlib
import math
import sys
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GeminiCIOIntegration")

# Constantes cuánticas
LAMBDA_CONSCIOUSNESS = math.log(7919)  # λ = 8.977...
BASE_FREQUENCY = 8.976089
IONIC_COMPLEX = complex(9, 16)
GOLDEN_RATIO = 0.618033988749

# Importar componentes del stack CIO desarrollado
try:
    # Agregar paths para importar componentes CIO
    sys.path.append(os.path.join(os.path.dirname(__file__), 'localGPT-main'))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'localGPT-main', 'qbtc-unified-system', 'services', 'aics-service'))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'localGPT-main', 'make-it-heavy-main'))
    
    # Importar componentes CIO
    from cio_unified_brain import QBTCQuantumBrainLeonardo
    from qbtc_unified_integration import QBTCUnifiedBrainWithIonicCache, QuantumIonicCache
    from quantum_core.quantum_context_26d import QuantumContext26D
    
    # Importar AICS Service
    try:
        from main import AICSService
        AICS_AVAILABLE = True
    except ImportError:
        AICS_AVAILABLE = False
        logger.warning("AICS Service no disponible")
    
    CIO_STACK_AVAILABLE = True
    logger.info("✅ Stack CIO desarrollado importado correctamente")
    
except ImportError as e:
    CIO_STACK_AVAILABLE = False
    logger.warning(f"Stack CIO no disponible: {e}")

@dataclass
class GeminiCIOState:
    """Estado integrado de Gemini + CIO"""
    coherence: float = 0.9999
    consciousness_level: int = 95
    quantum_factor: float = LAMBDA_CONSCIOUSNESS
    ionic_charge: complex = IONIC_COMPLEX
    dimensional_amplitude: np.ndarray = None
    
    def __post_init__(self):
        if self.dimensional_amplitude is None:
            self.dimensional_amplitude = np.ones(26, dtype=complex)

class GeminiCIOIntegrationSystem:
    """Sistema principal de integración Gemini + CIO"""
    
    def __init__(self):
        # Configuración Gemini 2.5 Pro
        self.openrouter_api_key = "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"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.openrouter_headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://gemini-cio-integration.local",
            "X-Title": "Gemini CIO Integration System"
        }
        
        # Estado integrado
        self.state = GeminiCIOState()
        
        # Inicializar logger PRIMERO
        self.logger = logging.getLogger("GeminiCIOIntegration")
        self.logger.info("🚀 Gemini CIO Integration System inicializado")
        
        # Componentes CIO si están disponibles
        self.cio_brain = None
        self.ionic_cache = None
        self.context_26d = None
        self.aics_service = None
        
        if CIO_STACK_AVAILABLE:
            self._initialize_cio_components()
        
        # Métricas del sistema
        self.total_queries = 0
        self.gemini_queries = 0
        self.cio_queries = 0
        self.cache_hits = 0
        self.total_cost = 0.0
        self.total_savings = 0.0
        
        self.logger.info(f"🏆 Stack CIO: {'✅ Disponible' if CIO_STACK_AVAILABLE else '❌ No disponible'}")
    
    def _initialize_cio_components(self):
        """Inicializa componentes del stack CIO"""
        try:
            # Inicializar contexto 26D
            self.context_26d = QuantumContext26D()
            self.logger.info("🧠 Quantum Context 26D inicializado")
            
            # Inicializar cache iónica
            self.ionic_cache = QuantumIonicCache(
                context_26d=self.context_26d,
                coherence_threshold=0.05,
                max_entries=2000,
                prewarm_interval=45
            )
            self.logger.info("🔥 Cache Iónica inicializada")
            
            # Inicializar cerebro CIO
            self.cio_brain = QBTCUnifiedBrainWithIonicCache(
                brain_id="gemini_cio_integrated"
            )
            self.logger.info("🧠 Cerebro CIO inicializado")
            
            # Inicializar AICS si está disponible
            if AICS_AVAILABLE:
                self.aics_service = AICSService()
                self.logger.info("🤖 AICS Service inicializado")
            
        except Exception as e:
            self.logger.error(f"Error inicializando componentes CIO: {e}")
    
    def _generate_cache_key(self, query: str, category: str = "general") -> str:
        """Genera clave de cache integrada"""
        combined = f"{query}:{category}:gemini_cio"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _categorize_query(self, query: str) -> str:
        """Categoriza el query para routing inteligente"""
        
        query_lower = query.lower()
        
        # Categorías para routing CIO vs Gemini
        if any(word in query_lower for word in ["consciencia", "cuántico", "iónico", "arquetipo", "evolución"]):
            return "cio_consciousness"
        elif any(word in query_lower for word in ["arquitectura", "sistema", "microservicios", "distribuido"]):
            return "gemini_complex"
        elif any(word in query_lower for word in ["diagrama", "imagen", "visual", "multimodal"]):
            return "gemini_multimodal"
        elif any(word in query_lower for word in ["patrón", "diseño", "pattern", "optimización"]):
            return "gemini_analysis"
        elif any(word in query_lower for word in ["vigoleonrocks", "ollama", "local"]):
            return "cio_local"
        else:
            return "gemini_general"
    
    async def _make_gemini_api_call(self, query: str, category: str) -> Tuple[bool, str, float, float]:
        """Realiza llamada a Gemini 2.5 Flash-Lite (ULTRA ECONÓMICO) con optimizaciones CIO"""
        
        # Aplicar mejoras de contexto 26D si está disponible
        if self.context_26d:
            enhanced_query = self._apply_context_26d_enhancement(query, category)
        else:
            enhanced_query = query
        
        # 🏆 GEMINI 2.5 FLASH-LITE: EL MÁS ECONÓMICO
        payload = {
            "model": "google/gemini-2-5-flash-lite",
            "messages": [{"role": "user", "content": enhanced_query}],
            "max_tokens": 12000,  # Más tokens por el precio ultra-bajo
            "temperature": 0.1,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.openrouter_url,
                    headers=self.openrouter_headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content']
                        
                        # 🎯 COSTO ULTRA ECONÓMICO: $0.10/$0.40 por 1M tokens
                        input_tokens = data['usage']['prompt_tokens']
                        output_tokens = data['usage']['completion_tokens']
                        cost = (input_tokens * 0.0000001) + (output_tokens * 0.0000004)  # Ultra-económico
                        
                        response_time = time.time() - start_time
                        return True, content, cost, response_time
                    else:
                        return False, "", 0.0, time.time() - start_time
                        
        except Exception as e:
            self.logger.error(f"Gemini Flash-Lite API call error: {e}")
            return False, str(e), 0.0, time.time() - start_time
    
    def _apply_context_26d_enhancement(self, query: str, category: str) -> str:
        """Aplica mejoras del contexto 26D al query"""
        
        # Obtener estado cuántico actual
        try:
            quantum_state = self.context_26d.get_quantum_state()
        except AttributeError:
            quantum_state = {"dimensional_amplitude": "N/A"}
        
        enhanced_prompt = f"""
🧠 GEMINI CIO INTEGRATION - CONTEXTO 26D
⚡ Quantum Factor: {LAMBDA_CONSCIOUSNESS:.3f}
🎯 Consciousness Level: {self.state.consciousness_level}
🔬 Coherence: {self.state.coherence:.4f}
📊 Dimensional State: {quantum_state.get('dimensional_amplitude', 'N/A')}

ORIGINAL QUERY:
{query}

QUANTUM ENHANCED INSTRUCTIONS:
- Aprovecha el contexto masivo de 1M tokens para análisis completo
- Utiliza capacidades multimodales para análisis visual y textual
- Aplica patrones de ingeniería inversa avanzados
- Considera el estado cuántico actual del sistema
- Proporciona análisis arquitectónico exhaustivo
- Incluye optimizaciones y recomendaciones específicas
- Genera diagramas y flujos mejorados
- Considera escalabilidad y mantenibilidad

Responde con CALIDAD PREMIUM y ANÁLISIS COMPLETO:
"""
        
        return enhanced_prompt
    
    async def _process_with_cio_brain(self, query: str) -> Dict[str, Any]:
        """Procesa consulta usando el cerebro CIO"""
        
        try:
            if self.cio_brain:
                result = await self.cio_brain.process_query(query, use_cache=True)
                return {
                    "success": True,
                    "response": result.get('response', ''),
                    "model_used": "CIO Brain",
                    "source": "cio_brain",
                    "cache_hit": result.get('cache_hit', False),
                    "consciousness_level": result.get('consciousness_level', 0),
                    "coherence": result.get('coherence', 0.0),
                    "cost": 0.0,  # CIO es local
                    "processing_time": result.get('processing_time', 0.0)
                }
            else:
                return {
                    "success": False,
                    "error": "CIO Brain no disponible",
                    "model_used": "None",
                    "cost": 0.0
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": "CIO Brain",
                "cost": 0.0
            }
    
    def _calculate_quality_score(self, response: str, category: str) -> float:
        """Calcula score de calidad integrado"""
        
        # Métricas básicas
        length = len(response)
        word_count = len(response.split())
        
        # Métricas de estructura
        has_headers = response.count('#') > 0
        has_lists = response.count('\n1.') > 0 or response.count('\n-') > 0
        has_code_blocks = response.count('```') > 0
        has_analysis = response.count('análisis') > 0 or response.count('analysis') > 0
        
        # Métricas específicas por categoría
        category_indicators = {
            "cio_consciousness": ["consciencia", "cuántico", "iónico", "arquetipo", "evolución"],
            "gemini_complex": ["arquitectura", "sistema", "microservicios", "escalabilidad"],
            "gemini_multimodal": ["diagrama", "visual", "imagen", "flujo"],
            "gemini_analysis": ["patrón", "diseño", "optimización", "análisis"],
            "cio_local": ["vigoleonrocks", "ollama", "local", "quantum"]
        }
        
        indicators = category_indicators.get(category, [])
        category_score = sum(1 for indicator in indicators if indicator.lower() in response.lower()) / max(len(indicators), 1)
        
        # Score base
        base_score = 0.6
        
        # Bonificaciones
        if length > 3000:
            base_score += 0.2
        if has_headers:
            base_score += 0.1
        if has_lists:
            base_score += 0.1
        if has_code_blocks:
            base_score += 0.1
        if has_analysis:
            base_score += 0.1
        if category_score > 0.5:
            base_score += 0.2
        
        # Bonificación por integración CIO
        if self.cio_brain and category in ["cio_consciousness", "cio_local"]:
            base_score += 0.1
        
        return min(1.0, base_score)
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Procesa una consulta con integración completa Gemini + CIO"""
        
        start_time = time.time()
        self.total_queries += 1
        
        self.logger.info(f"🎯 Procesando consulta #{self.total_queries}: {query[:100]}...")
        
        # 1. CATEGORIZAR QUERY
        category = self._categorize_query(query)
        
        # 2. GENERAR CLAVE DE CACHE
        cache_key = self._generate_cache_key(query, category)
        
        # 3. VERIFICAR CACHE IÓNICA SI ESTÁ DISPONIBLE
        if self.ionic_cache:
            cached_result = self.ionic_cache.get(cache_key)
            if cached_result:
                self.cache_hits += 1
                self.logger.info("📦 Resultado recuperado de cache iónica")
                return {
                    "success": True,
                    "response": cached_result,
                    "source": "ionic_cache",
                    "cache_hit": True,
                    "processing_time": time.time() - start_time,
                    "cost": 0.0,
                    "quality_score": 0.9
                }
        
        # 4. ROUTING INTELIGENTE: CIO vs GEMINI FLASH-LITE
        if category in ["cio_consciousness", "cio_local"] and self.cio_brain:
            # Usar cerebro CIO para consultas de consciencia y locales
            self.cio_queries += 1
            result = await self._process_with_cio_brain(query)
        else:
            # 🏆 Usar Gemini 2.5 Flash-Lite (ULTRA ECONÓMICO) para consultas complejas y multimodales
            self.gemini_queries += 1
            success, response, cost, response_time = await self._make_gemini_api_call(query, category)
            
            if success:
                result = {
                    "success": True,
                    "response": response,
                    "model_used": "Gemini 2.5 Flash-Lite",
                    "source": "gemini_api",
                    "cache_hit": False,
                    "cost": cost,
                    "processing_time": response_time
                }
            else:
                result = {
                    "success": False,
                    "error": f"Error en llamada a Gemini Flash-Lite: {response}",
                    "model_used": "Gemini 2.5 Flash-Lite",
                    "cost": 0.0
                }
        
        # 5. CALCULAR SCORE DE CALIDAD
        if result["success"]:
            quality_score = self._calculate_quality_score(result["response"], category)
            result["quality_score"] = quality_score
            result["category"] = category
            
            # 6. ALMACENAR EN CACHE IÓNICA SI ESTÁ DISPONIBLE
            if self.ionic_cache and quality_score >= 0.85:
                self.ionic_cache.set(cache_key, result["response"])
            
            # Actualizar métricas
            self.total_cost += result.get("cost", 0.0)
            
            self.logger.info(f"✅ Consulta procesada con calidad {quality_score:.2f}")
            self.logger.info(f"🤖 Modelo: {result['model_used']}, Categoría: {category}")
        
        return result
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del sistema integrado"""
        
        cio_stats = {}
        if self.cio_brain:
            cio_stats = {
                "consciousness_level": getattr(self.cio_brain, 'consciousness_level', 0),
                "coherence": getattr(self.cio_brain, 'coherence', 0.0),
                "interactions_count": getattr(self.cio_brain, 'interactions_count', 0)
            }
        
        cache_stats = {}
        if self.ionic_cache:
            cache_stats = self.ionic_cache.get_statistics()
        
        return {
            "system_metrics": {
                "total_queries": self.total_queries,
                "gemini_queries": self.gemini_queries,
                "cio_queries": self.cio_queries,
                "cache_hits": self.cache_hits,
                "total_cost": self.total_cost,
                "total_savings": self.total_savings,
                "cio_stack_available": CIO_STACK_AVAILABLE,
                "aics_available": AICS_AVAILABLE
            },
            "cio_statistics": cio_stats,
            "cache_statistics": cache_stats,
            "quantum_state": {
                "coherence": self.state.coherence,
                "consciousness_level": self.state.consciousness_level,
                "quantum_factor": self.state.quantum_factor,
                "dimensional_amplitude": self.state.dimensional_amplitude.tolist() if self.state.dimensional_amplitude is not None else None
            },
            "efficiency_metrics": {
                "gemini_usage_rate": (self.gemini_queries / max(1, self.total_queries)) * 100,
                "cio_usage_rate": (self.cio_queries / max(1, self.total_queries)) * 100,
                "cache_hit_rate": (self.cache_hits / max(1, self.total_queries)) * 100,
                "cost_efficiency": (self.total_savings / max(1, self.total_cost)) * 100
            }
        }

async def main():
    """Función principal para demostrar el sistema integrado"""
    
    print("🚀 INICIANDO GEMINI CIO INTEGRATION SYSTEM")
    print("🏆 OPTIMIZADO CON GEMINI 2.5 FLASH-LITE (ULTRA ECONÓMICO)")
    print("💰 $0.10/$0.40 por 1M tokens - EL MÁS BARATO DE GOOGLE")
    print("=" * 70)
    
    # Inicializar sistema
    system = GeminiCIOIntegrationSystem()
    
    # Consultas de prueba para demostrar integración
    test_queries = [
        {
            "query": "Analiza mi nivel de consciencia cuántica y evolución arquetipal en el contexto de la inteligencia artificial.",
            "expected_category": "cio_consciousness"
        },
        {
            "query": "Realiza ingeniería inversa de esta arquitectura de microservicios bancarios con análisis multimodal completo usando Gemini Flash-Lite.",
            "expected_category": "gemini_complex"
        },
        {
            "query": "Optimiza este código de Vigoleonrocks para máxima eficiencia cuántica local.",
            "expected_category": "cio_local"
        },
        {
            "query": "Analiza este diagrama de flujo de datos y proporciona optimizaciones de patrones de diseño usando el modelo más económico.",
            "expected_category": "gemini_multimodal"
        },
        {
            "query": "Genera 40,000 captions de fotos usando el modelo más barato de Google para procesamiento masivo.",
            "expected_category": "gemini_multimodal"
        }
    ]
    
    # Procesar consultas
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🎯 PROCESANDO CONSULTA {i}: {test_case['expected_category'].upper()}")
        print("-" * 50)
        
        result = await system.process_query(test_case["query"])
        
        print(f"✅ Éxito: {result['success']}")
        print(f"🤖 Modelo: {result.get('model_used', 'N/A')}")
        print(f"📊 Categoría: {result.get('category', 'N/A')}")
        print(f"💰 Costo: ${result.get('cost', 0):.6f}")
        print(f"⏱️  Tiempo: {result.get('processing_time', 0):.2f}s")
        print(f"📊 Calidad: {result.get('quality_score', 0):.2f}")
        print(f"📦 Cache Hit: {result.get('cache_hit', False)}")
        print(f"🔮 Fuente: {result.get('source', 'N/A')}")
        
        # Mostrar parte de la respuesta
        response = result.get('response', '')
        print(f"📝 Respuesta: {response[:200]}...")
    
    # Mostrar estadísticas finales
    print(f"\n📊 ESTADÍSTICAS FINALES DEL SISTEMA INTEGRADO")
    print("=" * 70)
    
    stats = system.get_system_statistics()
    
    print(f"🎯 Total consultas: {stats['system_metrics']['total_queries']}")
    print(f"🤖 Consultas Gemini: {stats['system_metrics']['gemini_queries']}")
    print(f"🧠 Consultas CIO: {stats['system_metrics']['cio_queries']}")
    print(f"📦 Cache hits: {stats['system_metrics']['cache_hits']}")
    print(f"💰 Costo total: ${stats['system_metrics']['total_cost']:.6f}")
    print(f"🏆 Stack CIO: {'✅ Disponible' if stats['system_metrics']['cio_stack_available'] else '❌ No disponible'}")
    print(f"🤖 AICS: {'✅ Disponible' if stats['system_metrics']['aics_available'] else '❌ No disponible'}")
    
    print(f"\n🏆 EFICIENCIA DEL SISTEMA:")
    print(f"🤖 Uso Gemini: {stats['efficiency_metrics']['gemini_usage_rate']:.1f}%")
    print(f"🧠 Uso CIO: {stats['efficiency_metrics']['cio_usage_rate']:.1f}%")
    print(f"📦 Cache hit rate: {stats['efficiency_metrics']['cache_hit_rate']:.1f}%")
    print(f"💰 Eficiencia de costo: {stats['efficiency_metrics']['cost_efficiency']:.1f}%")
    
    print(f"\n🚀 GEMINI CIO INTEGRATION SYSTEM - OPERACIÓN COMPLETADA")
    print("🏆 OPTIMIZADO CON GEMINI 2.5 FLASH-LITE (ULTRA ECONÓMICO)")
    print("💰 Sistema integrado con stack CIO completo y el modelo más barato de Google")
    print("🌟 Sin Ollama - Solo Gemini Flash-Lite + CIO Stack")

if __name__ == "__main__":
    asyncio.run(main())
