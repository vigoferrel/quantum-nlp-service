"""
Sistema de validación cuántica para evaluaciones LLM
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from .test_case import LLMTestCase
from .quantum_llm import QuantumLLM
from .quantum_types import QuantumOption, QuantumValidation, QuantumFrequency, QuantumConfig
from .metrics.quantum_metrics.quantum_cache import QuantumCache

class QuantumValidator:
    """
    Validador cuántico que asegura la calidad y coherencia
    de las evaluaciones usando Lost Numbers.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.llm = QuantumLLM(config)
        self.cache = QuantumCache()
        self.frequency = QuantumFrequency.BASE_FREQUENCY
        self.quantum_config = QuantumConfig()
        
        # Umbrales de validación
        self.thresholds = {
            'coherence_min': 0.95,
            'entanglement_min': 0.90,
            'resonance_min': 0.90,
            'dimensional_min': 0.85,
            'global_min': 0.92
        }
        
        # Estado de validación
        self.validation_state = {
            'total_validations': 0,
            'successful_validations': 0,
            'failed_validations': 0,
            'validation_history': []
        }
        
    def validate(self, test_case: LLMTestCase) -> Dict[str, Any]:
        """
        Valida un caso de prueba usando el sistema cuántico completo
        """
        try:
            # Evaluar usando LLM cuántico
            results_option = QuantumOption.From(self.llm.evaluate(test_case))
            
            if results_option.is_none:
                return self._create_error_result("Evaluación LLM fallida")
                
            results = results_option.value
            
            # Reglas de validación cuántica
            validation_rules = [
                {
                    'name': 'coherence_check',
                    'validator': lambda r: r['coherence'] >= 0.95,
                    'message': 'Coherencia cuántica insuficiente'
                },
                {
                    'name': 'resonance_check',
                    'validator': lambda r: r['resonance'] >= 0.90,
                    'message': 'Resonancia cuántica baja'
                },
                {
                    'name': 'entanglement_check',
                    'validator': lambda r: r['entanglement'] >= 0.90,
                    'message': 'Entrelazamiento cuántico débil'
                },
                {
                    'name': 'frequency_check',
                    'validator': lambda r: abs(r.get('frequency', 0) - self.frequency) < 10,
                    'message': 'Desviación de frecuencia cuántica'
                }
            ]
            
            # Validar usando el sistema cuántico
            validation_results = QuantumValidation.validate(results, validation_rules)
            
            # Verificar coherencia dimensional
            dimensional_coherence = self._check_dimensional_coherence(results)
            validation_results['dimensional_coherence'] = dimensional_coherence
            
            # Validar estado cuántico
            quantum_state = self.llm.get_quantum_state()
            state_validation = self._validate_quantum_state(quantum_state)
            validation_results['quantum_state_valid'] = state_validation
            
            # Agregar metadata cuántica
            validation_results['quantum_metadata'] = QuantumConfig.get_metadata()
            
            # Actualizar estado de validación
            self._update_validation_state(validation_results)
            
            # Guardar en caché si es válido usando Option
            if validation_results['is_valid']:
                cache_key = f"validation_{test_case.input}_{test_case.actual_output}"
                cache_option = QuantumOption.From(validation_results)
                if cache_option.is_some:
                    self.cache.set(cache_key, cache_option.value)
            
            return validation_results
            
        except Exception as e:
            # Transmutación de error a mejora
            error_result = self._create_error_result(str(e))
            error_result['quantum_enhancement'] = {
                'original_error': str(e),
                'transmuted_frequency': QuantumFrequency.generate_deterministic('ERROR', int(datetime.now().timestamp())),
                'improvement_potential': 'Error transmutado para aprendizaje cuántico'
            }
            return error_result
            
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Crea un resultado de error con metadata cuántica"""
        return {
            'error': error_message,
            'is_valid': False,
            'quantum_metadata': QuantumConfig.get_metadata(),
            'error_frequency': QuantumFrequency.generate_deterministic('ERROR', int(datetime.now().timestamp()))
        }
        
    def _check_dimensional_coherence(self, results: Dict[str, float]) -> Dict[str, bool]:
        """
        Verifica coherencia entre dimensiones
        """
        coherence = {}
        quantum_state = self.llm.get_quantum_state()
        
        for dim in quantum_state['active_dimensions']:
            # Verificar coherencia dimensional
            dim_key = f'dim_{dim}'
            if dim_key in results:
                is_coherent = results[dim_key] >= self.thresholds['dimensional_min']
                coherence[dim] = is_coherent
                
        return coherence
        
    def _validate_quantum_state(self, state: Dict[str, Any]) -> bool:
        """
        Valida el estado cuántico global
        """
        # Verificar coherencia total
        if state['total_coherence'] < self.thresholds['coherence_min']:
            return False
            
        # Verificar entrelazamiento
        if state['total_entanglement'] < self.thresholds['entanglement_min']:
            return False
            
        # Verificar estado dimensional
        for dim_state in state['dimensional_state'].values():
            if dim_state < self.thresholds['dimensional_min']:
                return False
                
        return True
        
    def _update_validation_state(self, results: Dict[str, Any]):
        """
        Actualiza estado de validación
        """
        self.validation_state['total_validations'] += 1
        
        if results['is_valid']:
            self.validation_state['successful_validations'] += 1
        else:
            self.validation_state['failed_validations'] += 1
            
        # Mantener historial de últimas 100 validaciones
        self.validation_state['validation_history'].append({
            'timestamp': datetime.now().timestamp(),
            'is_valid': results['is_valid'],
            'metrics_validation': results['metrics_validation']
        })
        
        if len(self.validation_state['validation_history']) > 100:
            self.validation_state['validation_history'].pop(0)
            
    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de validación
        """
        total = self.validation_state['total_validations']
        if total == 0:
            return {
                'success_rate': 0.0,
                'total_validations': 0,
                'successful_validations': 0,
                'failed_validations': 0
            }
            
        return {
            'success_rate': self.validation_state['successful_validations'] / total,
            'total_validations': total,
            'successful_validations': self.validation_state['successful_validations'],
            'failed_validations': self.validation_state['failed_validations']
        }
        
    def reset_validation_state(self):
        """
        Reinicia estado de validación
        """
        self.validation_state = {
            'total_validations': 0,
            'successful_validations': 0,
            'failed_validations': 0,
            'validation_history': []
        }