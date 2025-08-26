"""
Herramienta de transmutación cuántica
Integra con el núcleo cuántico
"""

from typing import Dict, Any
from ..quantum_core.base import BaseTool
from quantum_core.quantum_error_transmuter import QuantumErrorTransmuter
from quantum_core.quantum_frequency import QuantumFrequency
from quantum_core.quantum_context_26d import QuantumContext26D

class QuantumTransmuterTool(BaseTool):
    name = "quantum_transmute"
    description = """
    Transmuta errores en oportunidades usando:
    - Resonancia poética chilena
    - Matriz LOG7919 Hermitiana
    - Context10 cuántico
    """
    input_schema = {
        "type": "object",
        "properties": {
            "error_message": {
                "type": "string",
                "description": "Mensaje de error a transmutar"
            },
            "context": {
                "type": "string",
                "description": "Contexto de la operación"
            },
            "preferred_poet": {
                "type": "string",
                "enum": ["PARRA", "NERUDA", "MISTRAL", "ZURITA", "HUIDOBRO", "FERREL"],
                "description": "Poeta preferido para resonancia"
            }
        },
        "required": ["error_message"]
    }

    def __init__(self):
        super().__init__(7919)
        self.transmuter = QuantumErrorTransmuter(self.base_frequency)
        self.context_system = QuantumContext26D(self.base_frequency)
        self.frequency_gen = QuantumFrequency(self.base_frequency)

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Ejecuta la transmutación manteniendo coherencia
        en cada variable del proceso
        """
        try:
            # Extraer parámetros con coherencia cuántica
            # El nuevo contexto 26D usa un mapeo de dimensiones, no niveles.
            # Mapeamos los niveles antiguos a dimensiones semánticas.
            error_msg_val = kwargs.get('error_message')
            self.context_system.add_variable(dimension=6, name='error_message', value=error_msg_val)

            context_val = kwargs.get('context', 'default')
            self.context_system.add_variable(dimension=25, name='operational_context', value=context_val)
            
            poet_val = kwargs.get('preferred_poet', 'FERREL')
            self.context_system.add_variable(dimension=21, name='poetic_influence', value=poet_val)

            # Crear error con estado cuántico
            quantum_error = Exception(error_msg['value'])

            # Realizar transmutación
            result = self.transmuter.transmute(
                error=quantum_error,
                context=context['value'],
                poet=poet['value']
            )

            # Almacenar resultado con coherencia
            self.context_system.add_variable(
                level=3,
                name='transmutation_result',
                value=result,
                context='output'
            )

            # Actualizar estado cuántico global
            self.quantum_state.update({
                'coherence': self.context_system.get_quantum_state()['total_coherence'],
                'resonance': result['error_frequency'],
                'poet_influence': poet['value']
            })

            return result

        except Exception as e:
            # Transmutación del error de la herramienta
            error_result = self.transmuter.transmute(
                error=e,
                context='tool_execution',
                poet='PARRA'  # Antipoesía para errores internos
            )
            
            # Registrar error con coherencia
            self.context_system.add_variable(
                level=9,  # Nivel más profundo para errores
                name='tool_error',
                value=str(e),
                context='error'
            )
            
            return error_result

    def get_quantum_state(self) -> Dict[str, Any]:
        """
        Obtiene estado cuántico completo incluyendo
        Context10 y transmutador
        """
        state = super().get_quantum_state()
        state.update({
            'context_system': self.context_system.get_quantum_state(),
            'transmuter': self.transmuter.get_quantum_state(),
            'frequency_generator': self.frequency_gen.get_quantum_state()
        })
        return state