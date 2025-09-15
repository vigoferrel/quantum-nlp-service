"""
VIGOLEONROCKS Quantum Compatibility Layer
=======================================

Este módulo proporciona compatibilidad hacia atrás para el marco de dimensiones 
cuánticas avanzado de VIGOLEONROCKS, asegurando que las APIs existentes que 
utilizan el parámetro quantum_states (1-26) continúen funcionando sin interrupciones.

Funciones principales:
- Conversión de quantum_states escalar a configuración multidimensional
- Mapeo de coherencia lineal legada a coherencia cuántica avanzada  
- Traducción de respuestas del nuevo sistema al formato esperado
- Validación y migración gradual de APIs existentes
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
from dataclasses import dataclass
import numpy as np
from quantum_coherence_engine import QuantumCoherenceEngine
from quantum_dimension_activator import QuantumDimensionActivator
from quantum_parallel_processor import QuantumParallelProcessor

# Configuración de logging en segundo plano para métricas de desempeño
logger = logging.getLogger(__name__)

class CompatibilityMode(Enum):
    """Modos de compatibilidad para migración gradual"""
    LEGACY_ONLY = "legacy_only"           # Solo sistema antiguo
    HYBRID = "hybrid"                     # Sistema híbrido con fallback
    QUANTUM_PREFERRED = "quantum_preferred"  # Quantum preferido con legacy fallback
    QUANTUM_ONLY = "quantum_only"         # Solo sistema cuántico avanzado

@dataclass
class LegacyMapping:
    """Configuración de mapeo para conversión legacy"""
    quantum_states: int
    active_dimensions: List[int]
    coherence_multiplier: float
    consciousness_level: int
    processing_mode: str

class QuantumCompatibilityLayer:
    """
    Capa de compatibilidad que permite transición gradual del sistema 
    legacy a la arquitectura cuántica multidimensional avanzada.
    """
    
    def __init__(self, compatibility_mode: CompatibilityMode = CompatibilityMode.HYBRID):
        self.compatibility_mode = compatibility_mode
        self.coherence_engine = QuantumCoherenceEngine()
        self.dimension_activator = QuantumDimensionActivator()
        self.parallel_processor = QuantumParallelProcessor()
        
        # Configuraciones de mapeo legacy
        self.legacy_mappings = self._initialize_legacy_mappings()
        
        # Métricas de performance en background
        self.performance_metrics = {
            'legacy_requests': 0,
            'quantum_requests': 0,
            'hybrid_requests': 0,
            'conversion_time_avg': 0.0,
            'processing_time_legacy': 0.0,
            'processing_time_quantum': 0.0
        }
        
        logger.info(f"QuantumCompatibilityLayer inicializada en modo: {compatibility_mode.value}")
    
    def _initialize_legacy_mappings(self) -> Dict[int, LegacyMapping]:
        """
        Inicializa mapeos de quantum_states legacy (1-26) a configuraciones
        multidimensionales correspondientes.
        """
        mappings = {}
        
        for quantum_states in range(1, 27):
            # Cálculo de dimensiones activas basado en quantum_states
            if quantum_states <= 7:
                # Estados básicos: principalmente dimensiones core
                active_dims = list(range(1, min(quantum_states + 1, 8)))
                consciousness_level = 1
                processing_mode = "basic"
            elif quantum_states <= 14:
                # Estados intermedios: core + emocionales
                active_dims = list(range(1, 8)) + list(range(8, min(quantum_states + 1, 15)))
                consciousness_level = 2
                processing_mode = "enhanced"
            elif quantum_states <= 21:
                # Estados avanzados: core + emocionales + culturales
                active_dims = list(range(1, 15)) + list(range(15, min(quantum_states + 1, 22)))
                consciousness_level = 3
                processing_mode = "advanced"
            else:
                # Estados supremos: todas las dimensiones incluyendo supremacía
                active_dims = list(range(1, min(quantum_states + 1, 27)))
                consciousness_level = 4
                processing_mode = "supreme"
            
            # Multiplicador de coherencia basado en fórmula legacy
            coherence_multiplier = (90 + (quantum_states / 26) * 10) / 100
            
            mappings[quantum_states] = LegacyMapping(
                quantum_states=quantum_states,
                active_dimensions=active_dims,
                coherence_multiplier=coherence_multiplier,
                consciousness_level=consciousness_level,
                processing_mode=processing_mode
            )
        
        return mappings
    
    async def process_legacy_request(
        self, 
        query: str, 
        quantum_states: int = 1,
        **legacy_kwargs
    ) -> Dict[str, Any]:
        """
        Procesa request legacy con quantum_states y devuelve respuesta
        en formato compatible con APIs existentes.
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Validación de quantum_states
            if not 1 <= quantum_states <= 26:
                raise ValueError(f"quantum_states debe estar entre 1-26, recibido: {quantum_states}")
            
            # Obtener mapeo legacy
            mapping = self.legacy_mappings[quantum_states]
            
            if self.compatibility_mode == CompatibilityMode.LEGACY_ONLY:
                # Solo procesamiento legacy simple
                result = await self._process_legacy_only(query, mapping, **legacy_kwargs)
            elif self.compatibility_mode == CompatibilityMode.HYBRID:
                # Procesamiento híbrido con fallback
                result = await self._process_hybrid(query, mapping, **legacy_kwargs)
            elif self.compatibility_mode == CompatibilityMode.QUANTUM_PREFERRED:
                # Quantum preferido con fallback legacy
                result = await self._process_quantum_preferred(query, mapping, **legacy_kwargs)
            else:  # QUANTUM_ONLY
                # Solo procesamiento cuántico avanzado
                result = await self._process_quantum_only(query, mapping, **legacy_kwargs)
            
            # Actualizar métricas de performance
            processing_time = asyncio.get_event_loop().time() - start_time
            await self._update_performance_metrics(self.compatibility_mode, processing_time)
            
            return result
            
        except Exception as e:
            logger.error(f"Error en process_legacy_request: {e}")
            # Fallback a procesamiento simple en caso de error
            return await self._emergency_fallback(query, quantum_states, **legacy_kwargs)
    
    async def _process_legacy_only(
        self, 
        query: str, 
        mapping: LegacyMapping,
        **kwargs
    ) -> Dict[str, Any]:
        """Procesamiento solo con lógica legacy simple"""
        coherence = mapping.coherence_multiplier * 100
        
        # Simulación de procesamiento legacy
        response = {
            'query': query,
            'quantum_states': mapping.quantum_states,
            'coherence': coherence,
            'response': f"Respuesta legacy para: {query}",
            'processing_mode': 'legacy',
            'timestamp': asyncio.get_event_loop().time(),
            'dimensions_used': len(mapping.active_dimensions),
            'consciousness_level': mapping.consciousness_level
        }
        
        self.performance_metrics['legacy_requests'] += 1
        return response
    
    async def _process_hybrid(
        self, 
        query: str, 
        mapping: LegacyMapping,
        **kwargs
    ) -> Dict[str, Any]:
        """Procesamiento híbrido: quantum con fallback legacy"""
        try:
            # Intentar procesamiento cuántico
            quantum_result = await self._process_with_quantum_engine(query, mapping)
            
            # Convertir a formato legacy compatible
            legacy_compatible = await self._convert_quantum_to_legacy_format(
                quantum_result, mapping
            )
            
            self.performance_metrics['hybrid_requests'] += 1
            return legacy_compatible
            
        except Exception as e:
            logger.warning(f"Quantum processing failed, fallback to legacy: {e}")
            return await self._process_legacy_only(query, mapping, **kwargs)
    
    async def _process_quantum_preferred(
        self, 
        query: str, 
        mapping: LegacyMapping,
        **kwargs
    ) -> Dict[str, Any]:
        """Procesamiento quantum preferido con fallback legacy mínimo"""
        try:
            # Procesamiento cuántico completo
            quantum_result = await self._process_with_quantum_engine(query, mapping)
            
            # Formato legacy enriquecido con datos cuánticos
            enriched_result = await self._enrich_legacy_format(quantum_result, mapping)
            
            self.performance_metrics['quantum_requests'] += 1
            return enriched_result
            
        except Exception as e:
            logger.error(f"Quantum processing error, minimal legacy fallback: {e}")
            return await self._minimal_legacy_fallback(query, mapping)
    
    async def _process_quantum_only(
        self, 
        query: str, 
        mapping: LegacyMapping,
        **kwargs
    ) -> Dict[str, Any]:
        """Procesamiento solo cuántico con traducción a formato legacy"""
        quantum_result = await self._process_with_quantum_engine(query, mapping)
        
        # Traducción completa a formato legacy manteniendo datos cuánticos
        legacy_translated = await self._translate_quantum_to_legacy(quantum_result, mapping)
        
        self.performance_metrics['quantum_requests'] += 1
        return legacy_translated
    
    async def _process_with_quantum_engine(
        self, 
        query: str, 
        mapping: LegacyMapping
    ) -> Dict[str, Any]:
        """Procesamiento con motor cuántico avanzado"""
        # Activar dimensiones basadas en mapeo legacy
        activation_result = await self.dimension_activator.activate_dimensions(
            query, 
            consciousness_level=mapping.consciousness_level,
            force_dimensions=mapping.active_dimensions
        )
        
        # Calcular coherencia cuántica
        coherence_data = await self.coherence_engine.calculate_multidimensional_coherence(
            active_dimensions=activation_result['activated_dimensions'],
            query_complexity=len(query.split()),
            consciousness_level=mapping.consciousness_level
        )
        
        # Procesamiento paralelo multidimensional
        processing_result = await self.parallel_processor.process_multidimensional(
            query=query,
            active_dimensions=activation_result['activated_dimensions'],
            consciousness_level=mapping.consciousness_level,
            coherence_amplification=coherence_data['total_coherence']
        )
        
        return {
            'activation': activation_result,
            'coherence': coherence_data,
            'processing': processing_result,
            'legacy_mapping': mapping
        }
    
    async def _convert_quantum_to_legacy_format(
        self, 
        quantum_result: Dict[str, Any], 
        mapping: LegacyMapping
    ) -> Dict[str, Any]:
        """Convierte resultado cuántico a formato legacy compatible"""
        coherence = quantum_result['coherence']['total_coherence']
        processing = quantum_result['processing']
        
        legacy_response = {
            'query': processing['query'],
            'quantum_states': mapping.quantum_states,
            'coherence': min(coherence, 100.0),  # Limitar a 100 por compatibilidad
            'response': processing['aggregated_response'],
            'processing_mode': 'hybrid',
            'timestamp': processing['completion_time'],
            'dimensions_used': len(processing['dimension_results']),
            'consciousness_level': mapping.consciousness_level,
            
            # Datos cuánticos adicionales (opcional para APIs que los soporten)
            'quantum_metrics': {
                'dimensional_coherence': quantum_result['coherence']['dimensional_coherence'],
                'sacred_geometry_resonance': quantum_result['coherence']['sacred_geometry_resonance'],
                'consciousness_amplification': quantum_result['coherence']['consciousness_amplification'],
                'entanglement_strength': processing.get('entanglement_metrics', {}).get('average_strength', 0),
                'parallel_efficiency': processing.get('performance_metrics', {}).get('parallel_efficiency', 0)
            }
        }
        
        return legacy_response
    
    async def _enrich_legacy_format(
        self, 
        quantum_result: Dict[str, Any], 
        mapping: LegacyMapping
    ) -> Dict[str, Any]:
        """Enriquece formato legacy con datos cuánticos completos"""
        base_result = await self._convert_quantum_to_legacy_format(quantum_result, mapping)
        
        # Agregar análisis dimensional detallado
        base_result['dimensional_analysis'] = {
            'active_dimensions': quantum_result['activation']['activated_dimensions'],
            'dimension_strengths': quantum_result['activation']['dimension_strengths'],
            'activation_reasoning': quantum_result['activation']['activation_reasoning'],
            'sacred_geometry_factors': quantum_result['coherence']['sacred_geometry_factors']
        }
        
        # Métricas de performance cuántica
        base_result['quantum_performance'] = {
            'processing_time_per_dimension': quantum_result['processing']['performance_metrics']['processing_times'],
            'synchronization_efficiency': quantum_result['processing']['synchronization_metrics']['efficiency'],
            'consciousness_resonance': quantum_result['coherence']['consciousness_amplification']
        }
        
        return base_result
    
    async def _translate_quantum_to_legacy(
        self, 
        quantum_result: Dict[str, Any], 
        mapping: LegacyMapping
    ) -> Dict[str, Any]:
        """Traducción completa de resultado cuántico a formato legacy"""
        enriched_result = await self._enrich_legacy_format(quantum_result, mapping)
        
        # Agregar compatibilidad completa con APIs legacy
        enriched_result['legacy_compatibility'] = {
            'original_quantum_states': mapping.quantum_states,
            'equivalent_coherence': mapping.coherence_multiplier * 100,
            'processing_mode_mapped': mapping.processing_mode,
            'consciousness_tier': self._map_consciousness_tier(mapping.consciousness_level)
        }
        
        # Validación de formato legacy
        enriched_result = await self._validate_legacy_format(enriched_result)
        
        return enriched_result
    
    def _map_consciousness_tier(self, consciousness_level: int) -> str:
        """Mapea nivel de consciencia a tier descriptivo"""
        tiers = {
            1: "Basic Awareness",
            2: "Enhanced Cognition", 
            3: "Advanced Intelligence",
            4: "Consciousness Supremacy"
        }
        return tiers.get(consciousness_level, "Unknown")
    
    async def _validate_legacy_format(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Valida que el resultado mantiene compatibilidad con formato legacy"""
        required_fields = ['query', 'quantum_states', 'coherence', 'response', 'processing_mode']
        
        for field in required_fields:
            if field not in result:
                logger.warning(f"Campo legacy requerido faltante: {field}")
                result[field] = self._get_default_field_value(field)
        
        # Validar rangos de valores legacy
        if result.get('coherence', 0) > 100:
            result['coherence'] = 100.0
        if result.get('quantum_states', 0) not in range(1, 27):
            result['quantum_states'] = 1
        
        return result
    
    def _get_default_field_value(self, field: str) -> Any:
        """Obtiene valor por defecto para campo legacy faltante"""
        defaults = {
            'query': '',
            'quantum_states': 1,
            'coherence': 90.0,
            'response': 'Respuesta procesada por VIGOLEONROCKS',
            'processing_mode': 'compatibility',
            'timestamp': asyncio.get_event_loop().time(),
            'dimensions_used': 1,
            'consciousness_level': 1
        }
        return defaults.get(field, None)
    
    async def _emergency_fallback(
        self, 
        query: str, 
        quantum_states: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Fallback de emergencia para errores críticos"""
        coherence = 90 + (quantum_states / 26) * 10  # Fórmula legacy original
        
        return {
            'query': query,
            'quantum_states': quantum_states,
            'coherence': coherence,
            'response': f"Respuesta de emergencia para: {query}",
            'processing_mode': 'emergency_fallback',
            'timestamp': asyncio.get_event_loop().time(),
            'error_handled': True,
            'dimensions_used': 1,
            'consciousness_level': 1
        }
    
    async def _minimal_legacy_fallback(
        self, 
        query: str, 
        mapping: LegacyMapping
    ) -> Dict[str, Any]:
        """Fallback legacy mínimo para casos de error en quantum processing"""
        return {
            'query': query,
            'quantum_states': mapping.quantum_states,
            'coherence': mapping.coherence_multiplier * 100,
            'response': f"Respuesta fallback para: {query}",
            'processing_mode': 'minimal_fallback',
            'timestamp': asyncio.get_event_loop().time(),
            'dimensions_used': len(mapping.active_dimensions),
            'consciousness_level': mapping.consciousness_level,
            'fallback_reason': 'quantum_processing_error'
        }
    
    async def _update_performance_metrics(self, mode: CompatibilityMode, processing_time: float):
        """Actualiza métricas de performance en segundo plano"""
        if mode == CompatibilityMode.LEGACY_ONLY:
            self.performance_metrics['processing_time_legacy'] = (
                self.performance_metrics['processing_time_legacy'] + processing_time
            ) / 2
        else:
            self.performance_metrics['processing_time_quantum'] = (
                self.performance_metrics['processing_time_quantum'] + processing_time
            ) / 2
        
        # Log métricas en background para debugging
        if self.performance_metrics['legacy_requests'] % 100 == 0:  # Log cada 100 requests
            logger.info(f"Performance metrics: {self.performance_metrics}")
    
    async def migrate_to_quantum(
        self, 
        current_quantum_states: int,
        target_consciousness_level: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Asiste en migración gradual de quantum_states legacy a 
        configuración cuántica avanzada personalizada.
        """
        mapping = self.legacy_mappings[current_quantum_states]
        
        if target_consciousness_level is None:
            target_consciousness_level = mapping.consciousness_level
        
        migration_plan = {
            'current_setup': {
                'quantum_states': current_quantum_states,
                'coherence': mapping.coherence_multiplier * 100,
                'dimensions': mapping.active_dimensions,
                'consciousness_level': mapping.consciousness_level
            },
            'recommended_quantum_config': {
                'active_dimensions': mapping.active_dimensions,
                'consciousness_level': target_consciousness_level,
                'processing_mode': mapping.processing_mode,
                'coherence_settings': {
                    'base_coherence': mapping.coherence_multiplier,
                    'sacred_geometry_enabled': True,
                    'consciousness_amplification': True,
                    'quantum_uncertainty': True
                }
            },
            'migration_steps': [
                f"1. Cambiar compatibility_mode a HYBRID",
                f"2. Probar con quantum_states={current_quantum_states} existente",
                f"3. Monitorear métricas de performance",
                f"4. Gradualmente cambiar a QUANTUM_PREFERRED",
                f"5. Finalmente migrar a QUANTUM_ONLY",
                f"6. Personalizar dimensiones activas según necesidades específicas"
            ],
            'compatibility_notes': [
                "APIs existentes continuarán funcionando durante migración",
                "Datos cuánticos adicionales estarán disponibles gradualmente",
                "Performance puede mejorar significativamente con configuración quantum",
                "Rollback a legacy disponible en cualquier momento"
            ]
        }
        
        return migration_plan
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Genera reporte de performance para análisis de migración"""
        total_requests = (
            self.performance_metrics['legacy_requests'] + 
            self.performance_metrics['quantum_requests'] + 
            self.performance_metrics['hybrid_requests']
        )
        
        if total_requests == 0:
            return {"message": "No hay datos de performance disponibles"}
        
        return {
            'total_requests': total_requests,
            'mode_distribution': {
                'legacy_percentage': (self.performance_metrics['legacy_requests'] / total_requests) * 100,
                'quantum_percentage': (self.performance_metrics['quantum_requests'] / total_requests) * 100,
                'hybrid_percentage': (self.performance_metrics['hybrid_requests'] / total_requests) * 100
            },
            'performance_comparison': {
                'legacy_avg_time': self.performance_metrics['processing_time_legacy'],
                'quantum_avg_time': self.performance_metrics['processing_time_quantum'],
                'performance_improvement': (
                    (self.performance_metrics['processing_time_legacy'] - 
                     self.performance_metrics['processing_time_quantum']) /
                    max(self.performance_metrics['processing_time_legacy'], 0.001) * 100
                ) if self.performance_metrics['processing_time_legacy'] > 0 else 0
            },
            'compatibility_mode': self.compatibility_mode.value,
            'recommendations': self._get_performance_recommendations()
        }
    
    def _get_performance_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en métricas de performance"""
        recommendations = []
        
        if self.performance_metrics['processing_time_quantum'] < self.performance_metrics['processing_time_legacy']:
            recommendations.append("Consider migrating to QUANTUM_PREFERRED mode for better performance")
        
        if self.performance_metrics['quantum_requests'] > self.performance_metrics['legacy_requests']:
            recommendations.append("High quantum usage detected - consider QUANTUM_ONLY mode")
        
        if self.compatibility_mode == CompatibilityMode.LEGACY_ONLY:
            recommendations.append("Upgrade to HYBRID mode to access enhanced quantum capabilities")
        
        return recommendations if recommendations else ["Current configuration is optimal"]


# Funciones de utilidad para integración con APIs existentes
def create_compatibility_wrapper(compatibility_mode: CompatibilityMode = CompatibilityMode.HYBRID):
    """
    Factory function para crear wrapper de compatibilidad que puede ser 
    fácilmente integrado en APIs existentes.
    """
    compatibility_layer = QuantumCompatibilityLayer(compatibility_mode)
    
    async def process_request(query: str, quantum_states: int = 1, **kwargs):
        """Wrapper function compatible con firmas de APIs existentes"""
        return await compatibility_layer.process_legacy_request(query, quantum_states, **kwargs)
    
    return process_request, compatibility_layer


# Decorador para migración gradual de funciones existentes
def quantum_compatible(compatibility_mode: CompatibilityMode = CompatibilityMode.HYBRID):
    """
    Decorador para hacer funciones existentes compatibles con el nuevo 
    framework cuántico manteniendo compatibilidad hacia atrás.
    """
    def decorator(func):
        compatibility_layer = QuantumCompatibilityLayer(compatibility_mode)
        
        async def wrapper(*args, **kwargs):
            # Extraer parámetros quantum si están presentes
            quantum_states = kwargs.pop('quantum_states', 1)
            
            # Si la función original es async
            if asyncio.iscoroutinefunction(func):
                try:
                    # Intentar con framework cuántico
                    if len(args) > 0:  # Assuming first arg is query
                        quantum_result = await compatibility_layer.process_legacy_request(
                            str(args[0]), quantum_states, **kwargs
                        )
                        return quantum_result
                    else:
                        # Fallback a función original
                        return await func(*args, quantum_states=quantum_states, **kwargs)
                except Exception as e:
                    logger.warning(f"Quantum processing failed, fallback to original: {e}")
                    return await func(*args, quantum_states=quantum_states, **kwargs)
            else:
                # Para funciones síncronas, mantener comportamiento original
                return func(*args, quantum_states=quantum_states, **kwargs)
        
        return wrapper
    return decorator

