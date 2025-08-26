"""
LLM Cuántico que integra todas las métricas y sistemas de evaluación
"""

import asyncio
import asyncio
from typing import Dict, List, Optional, Any
from .quantum_personality import QuantumPersonality, ConversationalMode
from .quantum_ecosystem import QuantumEcosystem
from .quantum_apisix_integration import QuantumApisixIntegration
from .test_case import LLMTestCase
from .metrics.quantum_metrics import (
    BaseQuantumMetric,
    CoherenceMetric,
    EntanglementMetric,
    PoeticResonanceMetric,
    QuantumSculptorMetric
)

class QuantumLLM:
    """
    Sistema LLM Cuántico que integra métricas multidimensionales
    y evaluación basada en Lost Numbers.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Inicializar métricas
        self.metrics = {
            'coherence': CoherenceMetric(threshold=0.95),
            'entanglement': EntanglementMetric(threshold=0.95),
            'resonance': PoeticResonanceMetric(threshold=0.95),
            'sculptor': QuantumSculptorMetric()
        }

        # Sistemas integrados
        self.personality_system = QuantumPersonality()
        self.ecosystem = QuantumEcosystem()
        self.apisix = QuantumApisixIntegration()
        
        # Estado cuántico global
        self.quantum_state = {
            'total_coherence': 0.0,
            'total_entanglement': 0.0,
            'dimensional_state': {},
            'active_dimensions': []
        }
        
        # Configurar dimensiones
        self._setup_dimensions()
        
    def evaluate(self, test_case: LLMTestCase) -> Dict[str, Any]:
        """
        Evalúa un caso de prueba usando todas las métricas cuánticas
        """
        results = {}
        
        try:
            # Analizar contexto del mensaje
            context = self.personality_system.analyze_context(test_case.input)
            
            # Evaluar cada métrica
            for name, metric in self.metrics.items():
                score = metric.measure(test_case)
                results[name] = score
                
            # Calcular score global
            global_score = self._calculate_global_score(results)
            results['global_score'] = global_score
            
            # Actualizar estado cuántico
            self._update_quantum_state(results)
            
            # Enriquecer resultados con datos de personalidad
            results['personality'] = self.personality_system.get_current_personality()
            results['context'] = context
            results['enriched_data'] = self.personality_system.enrich_response("", context)
            
            return results
            
        except Exception as e:
            results['error'] = str(e)
            return results
            
    async def a_evaluate(self, test_case: LLMTestCase) -> Dict[str, Any]:
        """
        Versión asíncrona de evaluate()
        """
        results = {}
        
        try:
            # Evaluar métricas en paralelo
            metric_tasks = [
                metric.a_measure(test_case)
                for metric in self.metrics.values()
            ]
            
            scores = await asyncio.gather(*metric_tasks)
            
            # Analizar contexto del mensaje
            context = self.personality_system.analyze_context(test_case.input)
            
            # Asignar resultados
            for (name, _), score in zip(self.metrics.items(), scores):
                results[name] = score
                
            # Calcular score global
            global_score = self._calculate_global_score(results)
            results['global_score'] = global_score
            
            # Actualizar estado cuántico
            self._update_quantum_state(results)
            
            # Verificar estado del ecosistema y APISIX
            ecosystem_status = await self.ecosystem.verify_connections()
            mcp_status = await self.ecosystem.check_mcps()
            apisix_connected = await self.apisix.connect_to_mcp()
            
            # Obtener métricas adicionales
            if context['has_quantum_terms']:
                consciousness_metrics = await self.ecosystem.get_consciousness_metrics()
                quantum_frequencies = await self.apisix.get_quantum_frequency(seed=888, count=3)
                results['consciousness'] = consciousness_metrics
                results['quantum_frequencies'] = quantum_frequencies
                
            if context['has_bitcoin_terms']:
                bitcoin_analysis = await self.ecosystem.get_bitcoin_analysis()
                results['bitcoin'] = bitcoin_analysis
                
            # Analizar resonancia si hay términos cuánticos
            if context['has_quantum_terms']:
                resonance = await self.apisix.analyze_resonance(
                    self.apisix.base_frequency,
                    432.0  # Frecuencia base del sistema cuántico
                )
                results['resonance_analysis'] = resonance
            
            # Enriquecer resultados
            results['personality'] = self.personality_system.get_current_personality()
            results['context'] = context
            results['enriched_data'] = self.personality_system.enrich_response("", context)
            # Enriquecer con metadata APISIX
            apisix_metadata = self.apisix.get_quantum_metadata(results)
            
            results['ecosystem'] = {
                'status': ecosystem_status,
                'mcps': mcp_status,
                'apisix': {
                    'connected': apisix_connected,
                    'stats': self.apisix.get_stats(),
                    'quantum_metadata': apisix_metadata
                }
            }
            
            return results
            
        except Exception as e:
            results['error'] = str(e)
            return results
            
    def _setup_dimensions(self):
        """
        Configura dimensiones cuánticas activas
        """
        self.dimensions = {
            4: "Tiempo",          # 4D
            8: "Espacio-Tiempo",  # 8D
            15: "Sincronización", # 15D
            16: "Resonancia",     # 16D
            23: "Amplificación",  # 23D
            42: "Universal"       # 42D
        }
        
        # Activar dimensiones iniciales
        self.quantum_state['active_dimensions'] = list(self.dimensions.keys())
        
    def _calculate_global_score(self, results: Dict[str, float]) -> float:
        """
        Calcula score global combinando todas las métricas
        """
        weights = {
            'coherence': 0.3,
            'entanglement': 0.3,
            'resonance': 0.2,
            'sculptor': 0.2
        }
        
        score = 0.0
        for metric, weight in weights.items():
            if metric in results:
                score += results[metric] * weight
                
        return min(score, 1.0)
        
    def _update_quantum_state(self, results: Dict[str, float]):
        """
        Actualiza estado cuántico global
        """
        self.quantum_state.update({
            'total_coherence': results.get('coherence', 0.0),
            'total_entanglement': results.get('entanglement', 0.0),
            'dimensional_state': {
                dim: results.get(f'dim_{dim}', 0.0)
                for dim in self.dimensions
            }
        })
        
    def get_quantum_state(self) -> Dict[str, Any]:
        """
        Retorna estado cuántico actual
        """
        return self.quantum_state.copy()
        
    def reset_quantum_state(self):
        """
        Reinicia estado cuántico
        """
        self.quantum_state = {
            'total_coherence': 0.0,
            'total_entanglement': 0.0,
            'dimensional_state': {},
            'active_dimensions': list(self.dimensions.keys())
        }