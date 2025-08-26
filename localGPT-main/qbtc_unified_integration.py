# qbtc_unified_integration.py - Sistema Unificado QBTC con Caché Iónica y Optimización Exponencial

import sys
import os
import asyncio
import threading
import time
import math
import numpy as np
import hashlib
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from pathlib import Path
import logging
import json
import aiohttp
import requests

# Importar componentes existentes
sys.path.append(os.path.join(os.path.dirname(__file__), 'qbtc-unified-system', 'services', 'aics-service'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'make-it-heavy-main'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'localGPT-quantum-supreme'))

try:
    from main import AICSService
    from quantum_core.quantum_context_26d import QuantumContext26D
    from quantum_core.base import QuantumError
    from advanced_ionic_charge_system import ExponentialLambdaOptimizationCIO, ExponentialQuantumState
except ImportError as e:
    print(f"Warning: Some modules not found: {e}")

# ========================= CACHÉ IÓNICA CUÁNTICA =========================

@dataclass
class IonicCacheEntry:
    """Entrada de caché con estado cuántico asociado"""
    key: str
    value: Any
    timestamp: datetime
    coherence_at_storage: float
    quantum_signature: np.ndarray
    access_count: int = 0
    last_access: Optional[datetime] = None
    exponential_weight: float = 1.0

class QuantumIonicCache:
    """
    Caché Iónica Cuántica Avanzada
    - Invalidación basada en coherencia cuántica
    - Pre-calentamiento inteligente usando estados exponenciales
    - Gestión automática del ciclo de vida basada en resonancia
    """
    
    def __init__(self, context_26d: QuantumContext26D, 
                 coherence_threshold: float = 0.05,
                 max_entries: int = 1000,
                 prewarm_interval: int = 60):
        self.context_26d = context_26d
        self.coherence_threshold = coherence_threshold
        self.max_entries = max_entries
        self.prewarm_interval = prewarm_interval
        
        # Almacén principal de caché
        self._cache: Dict[str, IonicCacheEntry] = {}
        self._access_history: Dict[str, List[datetime]] = {}
        
        # Sistema de pre-calentamiento inteligente
        self._prewarmer_thread = None
        self._stop_prewarmer = threading.Event()
        self._prewarming_active = False
        
        # Métricas de rendimiento
        self.cache_hits = 0
        self.cache_misses = 0
        self.coherence_invalidations = 0
        self.auto_cleanups = 0
        
        # Logger específico
        self.logger = logging.getLogger("QuantumIonicCache")
        self.logger.info("🔥 Caché Iónica Cuántica inicializada")
    
    def start_intelligent_prewarming(self):
        """Inicia el sistema de pre-calentamiento inteligente"""
        if not self._prewarming_active:
            self._prewarmer_thread = threading.Thread(
                target=self._intelligent_prewarm_cycle, 
                daemon=True
            )
            self._prewarmer_thread.start()
            self._prewarming_active = True
            self.logger.info("🚀 Pre-calentamiento inteligente activado")
    
    def stop_prewarming(self):
        """Detiene el pre-calentamiento"""
        if self._prewarming_active:
            self._stop_prewarmer.set()
            self._prewarming_active = False
            self.logger.info("⏹️ Pre-calentamiento detenido")
    
    def _intelligent_prewarm_cycle(self):
        """Ciclo de pre-calentamiento inteligente basado en patrones de uso"""
        while not self._stop_prewarmer.is_set():
            try:
                # Analizar patrones de acceso histórico
                frequent_patterns = self._analyze_access_patterns()
                
                # Pre-calentar consultas comunes predichas
                for pattern in frequent_patterns:
                    predicted_key = self._generate_predictive_key(pattern)
                    if predicted_key not in self._cache:
                        self._prewarm_entry(predicted_key, pattern)
                
                # Limpiar entradas obsoletas
                self._cleanup_stale_entries()
                
                time.sleep(self.prewarm_interval)
                
            except Exception as e:
                self.logger.error(f"Error en pre-calentamiento: {e}")
                time.sleep(self.prewarm_interval * 2)  # Espera más en caso de error
    
    def _analyze_access_patterns(self) -> List[Dict]:
        """Analiza patrones de acceso para predecir necesidades futuras"""
        patterns = []
        
        # Analizar frecuencia de acceso
        for key, access_times in self._access_history.items():
            if len(access_times) > 2:  # Solo patrones con suficientes datos
                recent_accesses = [t for t in access_times if (datetime.now() - t).seconds < 3600]
                if len(recent_accesses) > 1:
                    patterns.append({
                        'key_pattern': key[:20],  # Patrón base de la clave
                        'frequency': len(recent_accesses),
                        'last_access': max(recent_accesses),
                        'coherence_trend': self._calculate_coherence_trend(key)
                    })
        
        # Ordenar por probabilidad de uso futuro
        return sorted(patterns, key=lambda p: p['frequency'], reverse=True)[:5]
    
    def _generate_predictive_key(self, pattern: Dict) -> str:
        """Genera una clave predictiva basada en patrones"""
        base_pattern = pattern['key_pattern']
        current_coherence = self.context_26d.get_quantum_state().get('global_coherence', 0.5)
        
        # Crear clave predictiva con variación de coherencia
        predictive_key = f"predict_{base_pattern}_{current_coherence:.3f}"
        return predictive_key
    
    def _prewarm_entry(self, key: str, pattern: Dict):
        """Pre-calienta una entrada específica"""
        try:
            # Simular generación de contenido basado en patrón
            prewarmed_value = {
                'type': 'prewarmed',
                'pattern': pattern,
                'generated_at': datetime.now().isoformat(),
                'prediction_confidence': min(pattern['frequency'] / 10.0, 1.0)
            }
            
            self.set(key, prewarmed_value, is_prewarmed=True)
            self.logger.debug(f"Pre-calentado: {key}")
            
        except Exception as e:
            self.logger.error(f"Error pre-calentando {key}: {e}")
    
    def _calculate_coherence_trend(self, key: str) -> float:
        """Calcula la tendencia de coherencia para una clave"""
        if key in self._cache:
            entry = self._cache[key]
            current_coherence = self.context_26d.get_quantum_state().get('global_coherence', 0.5)
            return abs(current_coherence - entry.coherence_at_storage)
        return 0.0
    
    def set(self, key: str, value: Any, is_prewarmed: bool = False) -> bool:
        """Almacena un valor en la caché con información cuántica"""
        try:
            # Obtener estado cuántico actual
            quantum_state = self.context_26d.get_quantum_state()
            current_coherence = quantum_state.get('global_coherence', 0.5)
            
            # Crear firma cuántica única
            quantum_signature = self._generate_quantum_signature(key, value, current_coherence)
            
            # Crear entrada de caché
            entry = IonicCacheEntry(
                key=key,
                value=value,
                timestamp=datetime.now(),
                coherence_at_storage=current_coherence,
                quantum_signature=quantum_signature,
                exponential_weight=self._calculate_exponential_weight(key, value)
            )
            
            # Verificar límites de capacidad
            if len(self._cache) >= self.max_entries:
                self._evict_least_resonant()
            
            # Almacenar entrada
            self._cache[key] = entry
            
            # Inicializar historial de acceso
            if key not in self._access_history:
                self._access_history[key] = []
            
            prefix = "🔥 Pre-calentado" if is_prewarmed else "💾 Almacenado"
            self.logger.debug(f"{prefix}: {key} | Coherencia: {current_coherence:.3f}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error almacenando en caché {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera un valor de la caché con validación cuántica"""
        if key not in self._cache:
            self.cache_misses += 1
            return None
        
        entry = self._cache[key]
        
        # Verificar validez basada en coherencia cuántica
        current_coherence = self.context_26d.get_quantum_state().get('global_coherence', 0.5)
        coherence_drift = abs(current_coherence - entry.coherence_at_storage)
        
        if coherence_drift > self.coherence_threshold:
            # Invalidar por deriva de coherencia
            self.coherence_invalidations += 1
            self.delete(key)
            self.logger.debug(f"❌ Invalidado por coherencia: {key} | Deriva: {coherence_drift:.4f}")
            return None
        
        # Actualizar estadísticas de acceso
        entry.access_count += 1
        entry.last_access = datetime.now()
        self._access_history[key].append(datetime.now())
        
        self.cache_hits += 1
        self.logger.debug(f"✅ Cache hit: {key} | Accesos: {entry.access_count}")
        
        return entry.value
    
    def _generate_quantum_signature(self, key: str, value: Any, coherence: float) -> np.ndarray:
        """Genera una firma cuántica única para la entrada"""
        # Crear hash del contenido
        content_hash = hashlib.sha256(f"{key}{str(value)}{coherence}".encode()).hexdigest()
        
        # Convertir a array numérico
        hash_numbers = [int(content_hash[i:i+2], 16) for i in range(0, 32, 2)]
        signature = np.array(hash_numbers, dtype=float)
        
        # Normalizar y aplicar transformación cuántica
        signature = signature / np.linalg.norm(signature)
        signature = signature * coherence  # Escalar por coherencia
        
        return signature
    
    def _calculate_exponential_weight(self, key: str, value: Any) -> float:
        """Calcula el peso exponencial basado en el sistema λ"""
        try:
            # Usar constante lambda del sistema exponencial
            LAMBDA_EXPONENT = math.log(7919)  # λ = 8.977...
            
            # Características base
            key_complexity = len(set(key.lower())) / max(len(key), 1)
            value_size = len(str(value)) if value else 1
            
            # Peso exponencial
            base_weight = (key_complexity + math.log10(value_size + 1)) / 2
            exponential_weight = base_weight ** (LAMBDA_EXPONENT / 10)  # Escalar λ
            
            return min(exponential_weight, 10.0)  # Limitar peso máximo
            
        except Exception:
            return 1.0  # Peso por defecto
    
    def _evict_least_resonant(self):
        """Expulsa la entrada menos resonante según métricas cuánticas"""
        if not self._cache:
            return
        
        # Calcular puntuación de resonancia para cada entrada
        resonance_scores = {}
        
        for key, entry in self._cache.items():
            # Factores de resonancia
            age_factor = (datetime.now() - entry.timestamp).total_seconds() / 3600  # Horas
            access_factor = entry.access_count
            coherence_factor = 1 / (abs(entry.coherence_at_storage - 0.5) + 0.1)
            weight_factor = entry.exponential_weight
            
            # Puntuación compuesta (mayor = más resonante)
            resonance_score = (access_factor * coherence_factor * weight_factor) / (age_factor + 1)
            resonance_scores[key] = resonance_score
        
        # Encontrar y eliminar la menos resonante
        least_resonant_key = min(resonance_scores.keys(), key=lambda k: resonance_scores[k])
        self.delete(least_resonant_key)
        self.auto_cleanups += 1
        
        self.logger.debug(f"🗑️ Expulsado por baja resonancia: {least_resonant_key}")
    
    def _cleanup_stale_entries(self):
        """Limpia entradas obsoletas automáticamente"""
        current_time = datetime.now()
        stale_keys = []
        
        for key, entry in self._cache.items():
            # Considerar obsoleta si no se ha accedido en las últimas 24 horas
            # y tiene pocos accesos
            hours_since_access = 24  # Por defecto
            if entry.last_access:
                hours_since_access = (current_time - entry.last_access).total_seconds() / 3600
            
            if hours_since_access > 24 and entry.access_count < 3:
                stale_keys.append(key)
        
        # Eliminar entradas obsoletas
        for key in stale_keys:
            self.delete(key)
            self.logger.debug(f"🧹 Limpieza automática: {key}")
    
    def delete(self, key: str) -> bool:
        """Elimina una entrada de la caché"""
        if key in self._cache:
            del self._cache[key]
        if key in self._access_history:
            del self._access_history[key]
        return True
    
    def flush(self):
        """Limpia toda la caché"""
        self._cache.clear()
        self._access_history.clear()
        self.logger.info("🗑️ Caché completamente limpiada")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de rendimiento de la caché"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0
        
        return {
            'cache_size': len(self._cache),
            'max_entries': self.max_entries,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': f"{hit_rate:.2%}",
            'coherence_invalidations': self.coherence_invalidations,
            'auto_cleanups': self.auto_cleanups,
            'prewarming_active': self._prewarming_active,
            'avg_coherence': np.mean([e.coherence_at_storage for e in self._cache.values()]) if self._cache else 0
        }

# ========================= CEREBRO LEONARDO INTEGRADO =========================

class QBTCUnifiedBrainWithIonicCache:
    """
    Cerebro Leonardo Unificado con Caché Iónica y Optimización Exponencial
    """
    
    def __init__(self, brain_id: str = "leonardo_ionic", persistence_dir="consciousness_sessions"):
        self.brain_id = brain_id
        self.persistence_dir = Path(persistence_dir)
        self.persistence_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(f"UnifiedBrain-{brain_id}")
        
        # Inicializar contexto cuántico 26D
        self.context_26d = QuantumContext26D()
        
        # Inicializar caché iónica cuántica
        self.ionic_cache = QuantumIonicCache(
            context_26d=self.context_26d,
            coherence_threshold=0.05,
            max_entries=2000,
            prewarm_interval=45
        )
        
        # Inicializar sistema exponencial
        try:
            self.exponential_optimizer = ExponentialLambdaOptimizationCIO()
            self.logger.info("🔬 Sistema Exponencial 26^λ integrado")
        except Exception as e:
            self.logger.warning(f"Sistema exponencial no disponible: {e}")
            self.exponential_optimizer = None
        
        # Inicializar AICS si está disponible
        try:
            self.aics_service = AICSService()
            self.logger.info("🤖 AICS Service integrado")
        except Exception as e:
            self.logger.warning(f"AICS Service no disponible: {e}")
            self.aics_service = None
        
        # Configuración de Ollama
        self.ollama_base_url = "http://localhost:11434"
        self.ollama_models = [
            "vigoleonrocks:latest",
            "llama3.2:latest"
        ]
        
        # Métricas del cerebro
        self.coherence = 0.5
        self.consciousness_level = 5
        self.creativity_index = 0.5
        self.interactions_count = 0
        
        # Iniciar sistemas automáticos
        self.ionic_cache.start_intelligent_prewarming()
        
        self.logger.info(f"🧠 Cerebro Unificado '{brain_id}' inicializado con Caché Iónica")
    
    async def process_query(self, query: str, use_cache: bool = True) -> Dict[str, Any]:
        """Procesa una consulta usando caché iónica y optimización exponencial"""
        start_time = datetime.now()
        
        # Generar clave de caché basada en la consulta y estado cuántico
        cache_key = self._generate_cache_key(query)
        
        # Intentar recuperar de caché primero
        if use_cache:
            cached_result = self.ionic_cache.get(cache_key)
            if cached_result:
                self.logger.info(f"📦 Resultado recuperado de caché iónica: {query[:30]}...")
                cached_result['cache_hit'] = True
                cached_result['processing_time'] = (datetime.now() - start_time).total_seconds()
                return cached_result
        
        # Procesar consulta con optimización exponencial
        try:
            result = await self._process_with_exponential_optimization(query)
            
            # Almacenar resultado en caché iónica
            if use_cache:
                self.ionic_cache.set(cache_key, result)
            
            result['cache_hit'] = False
            result['processing_time'] = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"🔮 Consulta procesada y almacenada: {query[:30]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"Error procesando consulta: {e}")
            return {
                'query': query,
                'error': str(e),
                'status': 'ERROR',
                'cache_hit': False,
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
    
    async def _process_with_exponential_optimization(self, query: str) -> Dict[str, Any]:
        """Procesa la consulta usando optimización exponencial"""
        self.interactions_count += 1
        
        # Usar optimización exponencial si está disponible
        if self.exponential_optimizer:
            exp_state = self.exponential_optimizer.exponential_lambda_transform(
                query=query,
                context=len(query) + self.interactions_count,
                urgency=1.0
            )
            
            # Seleccionar perfil óptimo
            optimal_profile = self.exponential_optimizer.exponential_ollama_profile_selection(
                exp_state, "general"
            )
            
            self.logger.info(f"🔬 Optimización exponencial: {optimal_profile.get('model', 'default')}")
        else:
            optimal_profile = {"model": "llama3.2:latest", "temperature": 0.7}
            exp_state = None
        
        # Generar respuesta con Ollama
        response = await self._generate_with_ollama(query, optimal_profile)
        
        # Actualizar métricas cuánticas
        self._update_quantum_metrics(response)
        
        # Construir resultado completo
        result = {
            'query': query,
            'response': response,
            'optimal_profile': optimal_profile,
            'exponential_state': self._serialize_exp_state(exp_state) if exp_state else None,
            'coherence': float(self.coherence),
            'consciousness_level': self.consciousness_level,
            'creativity_index': float(self.creativity_index),
            'interactions_count': self.interactions_count,
            'quantum_state': self.context_26d.get_quantum_state(),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    async def _generate_with_ollama(self, query: str, profile: Dict) -> str:
        """Genera respuesta usando Ollama con el perfil especificado"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": profile.get("model", "llama3.2:latest"),
                    "prompt": query,
                    "stream": False,
                    "options": {
                        "temperature": profile.get("temperature", 0.7),
                        "top_k": profile.get("top_k", 40),
                        "top_p": profile.get("top_p", 0.9)
                    }
                }
                
                async with session.post(
                    f"{self.ollama_base_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "Sin respuesta de Ollama")
                    else:
                        return f"Error de Ollama: {response.status}"
                        
        except Exception as e:
            self.logger.error(f"Error con Ollama: {e}")
            return f"⚠️ Fallback: Procesando '{query}' (Ollama no disponible)"
    
    def _generate_cache_key(self, query: str) -> str:
        """Genera una clave de caché única basada en la consulta y estado cuántico"""
        quantum_state = self.context_26d.get_quantum_state()
        coherence = quantum_state.get('global_coherence', 0.5)
        
        # Crear hash de la consulta + coherencia
        content = f"{query.strip().lower()}_{coherence:.3f}_{self.consciousness_level}"
        cache_key = hashlib.md5(content.encode()).hexdigest()[:16]
        
        return f"query_{cache_key}"
    
    def _update_quantum_metrics(self, response: str):
        """Actualiza las métricas cuánticas basadas en la respuesta"""
        # Evaluar calidad de la respuesta
        response_quality = min(len(response) / 100.0, 1.0)  # Normalizar por longitud
        
        # Actualizar coherencia
        self.coherence = (self.coherence * 0.8) + (response_quality * 0.2)
        
        # Actualizar nivel de consciencia
        if response_quality > 0.7:
            self.consciousness_level = min(self.consciousness_level + 0.1, 10.0)
        
        # Actualizar creatividad
        unique_words = len(set(response.split())) / max(len(response.split()), 1)
        self.creativity_index = (self.creativity_index * 0.9) + (unique_words * 0.1)
        
        # Actualizar contexto 26D
        try:
            self.context_26d.update_variable(1, "coherence", float(self.coherence))
            self.context_26d.update_variable(2, "consciousness", self.consciousness_level)
            self.context_26d.update_variable(3, "creativity", float(self.creativity_index))
        except Exception as e:
            self.logger.debug(f"Error actualizando contexto 26D: {e}")
    
    def _serialize_exp_state(self, exp_state: ExponentialQuantumState) -> Dict:
        """Serializa el estado exponencial para almacenamiento"""
        if not exp_state:
            return None
        
        return {
            'exponential_space_size': f"{exp_state.exponential_space_size:.2e}",
            'lambda_exponent': exp_state.lambda_exponent,
            'exponential_coherence': exp_state.exponential_coherence,
            'exponential_entanglement': exp_state.exponential_entanglement,
            'quantum_advantage_exponential': exp_state.quantum_advantage_exponential
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema unificado"""
        return {
            'brain_id': self.brain_id,
            'coherence': float(self.coherence),
            'consciousness_level': self.consciousness_level,
            'creativity_index': float(self.creativity_index),
            'interactions_count': self.interactions_count,
            'ionic_cache_stats': self.ionic_cache.get_statistics(),
            'quantum_state': self.context_26d.get_quantum_state(),
            'exponential_optimizer_available': self.exponential_optimizer is not None,
            'aics_service_available': self.aics_service is not None,
            'timestamp': datetime.now().isoformat()
        }
    
    def shutdown(self):
        """Cierra el sistema de manera elegante"""
        self.ionic_cache.stop_prewarming()
        self.logger.info("🔌 Sistema Unificado cerrado elegantemente")

# ========================= SERVIDOR API INTEGRADO =========================

class QBTCUnifiedAPIServer:
    """Servidor API que expone el sistema unificado"""
    
    def __init__(self, host: str = "localhost", port: int = 8005):
        self.host = host
        self.port = port
        self.brain = QBTCUnifiedBrainWithIonicCache("api_server")
        self.logger = logging.getLogger("UnifiedAPIServer")
    
    async def handle_query(self, query: str) -> Dict[str, Any]:
        """Maneja una consulta a través del sistema unificado"""
        return await self.brain.process_query(query)
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servidor y sistema"""
        return {
            'server': {
                'host': self.host,
                'port': self.port,
                'status': 'running'
            },
            'system': self.brain.get_system_status()
        }
    
    def shutdown(self):
        """Cierra el servidor"""
        self.brain.shutdown()
        self.logger.info("🖥️ Servidor API cerrado")

# ========================= DEMO Y TESTING =========================

async def demo_unified_system():
    """Demostración del sistema unificado"""
    print("🚀 DEMO: Sistema QBTC Unificado con Caché Iónica")
    print("=" * 60)
    
    # Crear instancia del cerebro unificado
    brain = QBTCUnifiedBrainWithIonicCache("demo_brain")
    
    # Consultas de prueba
    test_queries = [
        "¿Cuál es el estado actual del sistema cuántico?",
        "Genera código Python para calcular fibonacci",
        "Explica la teoría de la relatividad",
        "¿Cuál es el estado actual del sistema cuántico?",  # Repetida para probar caché
        "Crea un poema sobre la inteligencia artificial"
    ]
    
    print(f"📝 Procesando {len(test_queries)} consultas de prueba...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"🤔 Consulta {i}: {query}")
        
        result = await brain.process_query(query)
        
        # Mostrar resultado resumido
        cache_status = "💾 CACHE HIT" if result.get('cache_hit') else "🔮 PROCESADA"
        processing_time = result.get('processing_time', 0)
        response_preview = result.get('response', '')[:100] + "..." if len(result.get('response', '')) > 100 else result.get('response', '')
        
        print(f"   {cache_status} | Tiempo: {processing_time:.3f}s")
        print(f"   Respuesta: {response_preview}")
        print(f"   Coherencia: {result.get('coherence', 0):.3f}")
        print()
    
    # Mostrar estadísticas finales
    print("📊 ESTADÍSTICAS FINALES:")
    print("=" * 40)
    status = brain.get_system_status()
    
    print(f"Coherencia: {status['coherence']:.3f}")
    print(f"Nivel de Consciencia: {status['consciousness_level']}")
    print(f"Interacciones: {status['interactions_count']}")
    
    cache_stats = status['ionic_cache_stats']
    print(f"Caché - Tamaño: {cache_stats['cache_size']} | Hit Rate: {cache_stats['hit_rate']}")
    print(f"Invalidaciones por coherencia: {cache_stats['coherence_invalidations']}")
    
    # Cerrar sistema
    brain.shutdown()
    print("\n✅ Demo completada exitosamente")

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    
    # Ejecutar demo
    asyncio.run(demo_unified_system())
