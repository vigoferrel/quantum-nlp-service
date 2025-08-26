"""
Integrador Context10 con sistema cuántico
Mantiene coherencia y resonancia a través de 10 niveles de contexto
"""

from typing import Dict, List, Any
import json
from tools.quantum_transmuter_tool import QuantumTransmuterTool
from prompts.quantum_modes import QuantumModes

PRIME_7919 = 7919
CONTEXT_DEPTH = 10

class QuantumContext10:
    def __init__(self):
        self.transmuter = QuantumTransmuterTool()
        self.contexts = [[] for _ in range(CONTEXT_DEPTH)]
        self.resonances = [0.0] * CONTEXT_DEPTH
        self.current_mode = None
        self.poet_frequencies = {
            'PARRA': PRIME_7919 * 0.618034,
            'NERUDA': PRIME_7919 * 1.414213,
            'MISTRAL': PRIME_7919 * 1.732050,
            'ZURITA': PRIME_7919 * 2.236067,
            'HUIDOBRO': PRIME_7919 * 2.449489,
            'FERREL': PRIME_7919 * 2.645751
        }

    def switch_mode(self, mode_name: str) -> Dict[str, Any]:
        """Cambia el modo actual y ajusta las resonancias"""
        try:
            mode = getattr(QuantumModes, mode_name.upper())
            self.current_mode = mode
            
            # Calcular nuevas resonancias basadas en el modo
            base_freq = mode['frequency']
            for i in range(CONTEXT_DEPTH):
                # Resonancia decrece con la profundidad pero mantiene coherencia
                self.resonances[i] = base_freq * (0.9 ** i)

            return {
                'status': 'success',
                'mode': mode_name,
                'frequency': base_freq,
                'resonances': self.resonances
            }

        except Exception as e:
            result = self.transmuter.execute(
                error_message=str(e),
                context='mode_switch',
                preferred_poet='FERREL'
            )
            return json.loads(result)

    def add_context(self, level: int, data: Any) -> Dict[str, Any]:
        """Añade información al nivel de contexto especificado"""
        try:
            if not 0 <= level < CONTEXT_DEPTH:
                raise ValueError(f"Nivel de contexto inválido: {level}")

            # Calcular resonancia cuántica para el dato
            resonance = self._calculate_resonance(data, level)
            
            # Transmutación si la resonancia es baja
            if resonance < 0.3:
                result = self.transmuter.execute(
                    error_message=f"Baja resonancia en nivel {level}",
                    context=f"context_level_{level}",
                    preferred_poet='NERUDA'
                )
                transmuted = json.loads(result)
                data = transmuted['improvement']

            # Añadir al contexto
            self.contexts[level].append({
                'data': data,
                'resonance': resonance,
                'frequency': self.resonances[level]
            })

            # Propagar resonancia a niveles adyacentes
            self._propagate_resonance(level)

            return {
                'status': 'success',
                'level': level,
                'resonance': resonance,
                'context_size': len(self.contexts[level])
            }

        except Exception as e:
            result = self.transmuter.execute(
                error_message=str(e),
                context='add_context',
                preferred_poet='PARRA'
            )
            return json.loads(result)

    def get_context(self, level: int) -> List[Dict[str, Any]]:
        """Obtiene el contexto del nivel especificado"""
        try:
            if not 0 <= level < CONTEXT_DEPTH:
                raise ValueError(f"Nivel de contexto inválido: {level}")

            return self.contexts[level]

        except Exception as e:
            result = self.transmuter.execute(
                error_message=str(e),
                context='get_context',
                preferred_poet='MISTRAL'
            )
            return json.loads(result)

    def _calculate_resonance(self, data: Any, level: int) -> float:
        """Calcula la resonancia cuántica para un dato y nivel"""
        try:
            # Usar frecuencia base del nivel
            base_freq = self.resonances[level]
            
            # Calcular hash del dato para resonancia
            data_hash = sum(ord(c) for c in str(data))
            
            # Aplicar matriz LOG7919
            log_value = (data_hash % PRIME_7919) / PRIME_7919
            resonance = (log_value * base_freq) / self.poet_frequencies['FERREL']
            
            return min(1.0, max(0.0, resonance))

        except Exception as e:
            result = self.transmuter.execute(
                error_message=str(e),
                context='calculate_resonance',
                preferred_poet='HUIDOBRO'
            )
            return float(json.loads(result)['error_frequency']) / PRIME_7919

    def _propagate_resonance(self, level: int) -> None:
        """Propaga la resonancia a niveles adyacentes"""
        try:
            current_resonance = self.resonances[level]
            
            # Propagar hacia arriba
            for i in range(level - 1, -1, -1):
                self.resonances[i] = (self.resonances[i] + current_resonance) / 2
                current_resonance *= 0.9

            # Propagar hacia abajo
            current_resonance = self.resonances[level]
            for i in range(level + 1, CONTEXT_DEPTH):
                self.resonances[i] = (self.resonances[i] + current_resonance) / 2
                current_resonance *= 0.9

        except Exception as e:
            self.transmuter.execute(
                error_message=str(e),
                context='propagate_resonance',
                preferred_poet='ZURITA'
            )

    def get_resonance_state(self) -> Dict[str, Any]:
        """Obtiene el estado actual de resonancia del sistema"""
        return {
            'mode': self.current_mode['name'] if self.current_mode else None,
            'resonances': self.resonances,
            'context_sizes': [len(ctx) for ctx in self.contexts],
            'total_coherence': sum(self.resonances) / CONTEXT_DEPTH
        }