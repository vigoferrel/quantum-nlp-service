"""
Sistema de Contexto Cuántico Multidimensional (26D)
Optimizado para VIGOLEONROCKS en infraestructura Supabase XL
"""

from typing import Dict, Any, List
import numpy as np
from .base import QuantumBase, QuantumError
from .quantum_frequency import QuantumFrequency

class QuantumContext26D(QuantumBase):
    """
    Gestiona 26 dimensiones de contexto cuántico, reflejando las capacidades
    de VIGOLEONROCKS. Introduce un modelo de propagación de coherencia
    sofisticado y enfoque dimensional.
    """
    
    NUM_DIMENSIONS = 26

    def __init__(self, frequency: float = 7919, focused_dimension: int = 0):
        super().__init__(frequency)
        self.dimensions = [{
            'variables': {},
            'resonance': 0.0,
            'coherence': 1.0,
            'poet_influence': 'FERREL'
        } for _ in range(self.NUM_DIMENSIONS)]
        self.frequency_gen = QuantumFrequency(frequency)
        self.focused_dimension = focused_dimension
        self.coherence_matrix = np.identity(self.NUM_DIMENSIONS)

    def set_focus(self, dimension: int):
        """Enfoca el sistema en una dimensión específica, amplificando su influencia."""
        if not 0 <= dimension < self.NUM_DIMENSIONS:
            raise QuantumError(f"Dimensión inválida: {dimension}")
        self.focused_dimension = dimension
        self._update_global_coherence()

    def add_variable(
        self,
        dimension: int,
        name: str,
        value: Any,
        context: str = None
    ) -> Dict[str, Any]:
        """Añade una variable a una dimensión específica."""
        if not 0 <= dimension < self.NUM_DIMENSIONS:
            raise QuantumError(f"Dimensión inválida: {dimension}")

        try:
            var_freq = self.frequency_gen.generate_quantum_frequency(
                f"{name}:{str(value)}",
                self.dimensions[dimension]['poet_influence']
            )
            
            var_state = {
                'name': name,
                'value': value,
                'frequency': var_freq,
                'resonance': self.frequency_gen.calculate_resonance(var_freq, self.base_frequency),
                'context': context,
                'quantum_pattern': self.frequency_gen.generate_resonance_pattern(16, f"{name}:{str(value)}")
            }

            self.dimensions[dimension]['variables'][name] = var_state
            self._update_dimension_coherence(dimension)
            self._update_global_coherence()

            return var_state

        except Exception as e:
            raise QuantumError(f"Error añadiendo variable a la dimensión {dimension}: {e}", self.quantum_state)

    def get_variable(self, dimension: int, name: str) -> Dict[str, Any]:
        """Obtiene una variable de una dimensión específica."""
        if not 0 <= dimension < self.NUM_DIMENSIONS:
            raise QuantumError(f"Dimensión inválida: {dimension}")

        return self.dimensions[dimension]['variables'].get(name, {
            'error': f'Variable {name} no encontrada en la dimensión {dimension}'
        })

    def set_dimension_poet(self, dimension: int, poet: str) -> Dict[str, Any]:
        """Establece el poeta influyente para una dimensión y recalcula las resonancias."""
        if not 0 <= dimension < self.NUM_DIMENSIONS:
            raise QuantumError(f"Dimensión inválida: {dimension}")

        try:
            self.dimensions[dimension]['poet_influence'] = poet
            
            for name, var in self.dimensions[dimension]['variables'].items():
                var_freq = self.frequency_gen.generate_quantum_frequency(
                    f"{name}:{str(var['value'])}", poet
                )
                var['frequency'] = var_freq
                var['resonance'] = self.frequency_gen.calculate_resonance(var_freq, self.base_frequency)

            self._update_dimension_coherence(dimension)
            self._update_global_coherence()
            
            return self.dimensions[dimension]

        except Exception as e:
            raise QuantumError(f"Error actualizando poeta en la dimensión {dimension}: {e}", self.quantum_state)

    def _update_dimension_coherence(self, dimension: int):
        """Actualiza la coherencia de una dimensión basada en sus variables."""
        variables = self.dimensions[dimension]['variables']
        if not variables:
            self.dimensions[dimension].update({'resonance': 0.0, 'coherence': 1.0})
            return

        resonances = [var['resonance'] for var in variables.values()]
        avg_resonance = sum(resonances) / len(resonances)
        
        # Phi (Golden Ratio) para un decaimiento más natural
        phi = 1.61803398875
        coherence = min(1.0, avg_resonance * phi)
        
        self.dimensions[dimension].update({
            'resonance': avg_resonance,
            'coherence': coherence
        })

    def _update_global_coherence(self):
        """
        Actualiza la matriz de coherencia global, modelando la interconexión
        entre todas las dimensiones.
        """
        coherences = np.array([d['coherence'] for d in self.dimensions])
        
        # Influencia de la dimensión enfocada
        focus_factor = np.full(self.NUM_DIMENSIONS, 0.1)
        focus_factor[self.focused_dimension] = 0.9 # La dimensión enfocada tiene más peso
        
        # Propagación de coherencia no-local
        for i in range(self.NUM_DIMENSIONS):
            for j in range(i, self.NUM_DIMENSIONS):
                if i == j:
                    self.coherence_matrix[i, j] = coherences[i]
                else:
                    # La coherencia entre dimensiones es el producto, modulado por el enfoque
                    coherence_ij = coherences[i] * coherences[j] * (focus_factor[i] + focus_factor[j])
                    self.coherence_matrix[i, j] = self.coherence_matrix[j, i] = min(1.0, coherence_ij)

    def get_quantum_state(self) -> Dict[str, Any]:
        """Obtiene el estado cuántico consolidado del sistema de 26 dimensiones."""
        # Inicializa a partir del estado base heredado, no de un método abstracto.
        state = self.quantum_state.copy()
        
        # Coherencia global es el promedio de la matriz de coherencia
        global_coherence = np.mean(self.coherence_matrix)

        state.update({
            'global_coherence': global_coherence,
            'focused_dimension': self.focused_dimension,
            'dimensional_overview': [{
                'dimension': i,
                'variables': len(d['variables']),
                'coherence': d['coherence'],
                'poet': d['poet_influence']
            } for i, d in enumerate(self.dimensions)],
            'coherence_matrix_trace': np.trace(self.coherence_matrix)
        })
        return state
        
    def clear_dimension(self, dimension: int):
        """Limpia todas las variables de una dimensión."""
        if not 0 <= dimension < self.NUM_DIMENSIONS:
            raise QuantumError(f"Dimensión inválida: {dimension}")
        self.dimensions[dimension]['variables'].clear()
        self._update_dimension_coherence(dimension)
        self._update_global_coherence()

    def clear_all(self):
        """Limpia todas las dimensiones."""
        for i in range(self.NUM_DIMENSIONS):
            self.clear_dimension(i)
    
    def calculate_resonance(self, input_data: Any) -> float:
        """
        Implementa el método abstracto de QuantumBase.
        Calcula la resonancia cuántica para un input considerando las 26 dimensiones.
        """
        # Calcular hash del input
        input_hash = sum(ord(c) for c in str(input_data))
        
        # Aplicar LOG7919 base
        base_resonance = self._apply_log7919(input_hash)
        
        # Modular por la coherencia global del sistema 26D
        global_coherence = np.mean(self.coherence_matrix)
        dimensional_resonance = base_resonance * global_coherence
        
        # Aplicar influencia de la dimensión enfocada
        focus_boost = 1.0 + (0.618 * self.dimensions[self.focused_dimension]['coherence'])
        final_resonance = min(1.0, dimensional_resonance * focus_boost)
        
        # Actualizar estado cuántico
        self.quantum_state['resonance'] = final_resonance
        self.quantum_state['coherence'] = global_coherence
        
        return final_resonance