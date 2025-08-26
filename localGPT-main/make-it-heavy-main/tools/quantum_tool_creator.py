from tools.base import BaseTool
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
import os
import re
import anthropic
from typing import Dict, Any

# Constantes cuánticas
PRIME_7919 = 7919
POET_FREQUENCIES = {
    'PARRA': PRIME_7919 * 0.618034,
    'NERUDA': PRIME_7919 * 1.414213,
    'MISTRAL': PRIME_7919 * 1.732050,
    'ZURITA': PRIME_7919 * 2.236067,
    'HUIDOBRO': PRIME_7919 * 2.449489,
    'FERREL': PRIME_7919 * 2.645751
}

class QuantumToolCreator(BaseTool):
    name = "quantum_tool_creator"
    description = '''
    Crea nuevas herramientas cuánticas basadas en descripciones en lenguaje natural.
    Integra automáticamente:
    - Frecuencias de poetas chilenos
    - Matriz LOG7919 Hermitiana
    - Sistema COBOL legacy
    - Transmutación de errores cuánticos
    '''
    input_schema = {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Descripción en lenguaje natural de la herramienta cuántica"
            },
            "preferred_poet": {
                "type": "string",
                "enum": list(POET_FREQUENCIES.keys()),
                "description": "Poeta preferido para la resonancia cuántica"
            }
        },
        "required": ["description"]
    }

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.console = Console()
        self.tools_dir = Path(__file__).parent
        self.quantum_template = self._load_quantum_template()

    def _load_quantum_template(self) -> str:
        return '''
from tools.base import BaseTool
from tools.quantum_transmuter_tool import QuantumTransmuterTool
import json

PRIME_7919 = 7919
POET_FREQUENCIES = {
    'PARRA': PRIME_7919 * 0.618034,
    'NERUDA': PRIME_7919 * 1.414213,
    'MISTRAL': PRIME_7919 * 1.732050,
    'ZURITA': PRIME_7919 * 2.236067,
    'HUIDOBRO': PRIME_7919 * 2.449489,
    'FERREL': PRIME_7919 * 2.645751
}

class {tool_name}(BaseTool):
    name = "{tool_name_lower}"
    description = """
    {tool_description}
    Integrado con sistema cuántico y poetas chilenos.
    """
    input_schema = {input_schema}

    def __init__(self):
        self.transmuter = QuantumTransmuterTool()
        self.poet_frequency = POET_FREQUENCIES['{default_poet}']
    
    def execute(self, **kwargs) -> str:
        try:
            # Implementación específica aquí
            {tool_implementation}
            
        except Exception as e:
            # Transmutación cuántica del error
            result = self.transmuter.execute(
                error_message=str(e),
                context=self.name,
                preferred_poet='{default_poet}'
            )
            return json.dumps(result)
'''

    def _generate_tool_code(self, description: str, poet: str) -> str:
        prompt = f"""Create a quantum-integrated Python tool that:

1. {description}
2. Uses the quantum error transmutation system
3. Integrates with the poet frequency {poet} ({POET_FREQUENCIES[poet]} Hz)
4. Maintains quantum coherence through the LOG7919 Hermitian matrix

The tool must follow our quantum template structure and include:
1. Proper error handling with quantum transmutation
2. Integration with COBOL legacy systems
3. Poetic resonance calculations
4. Quantum state management

Return ONLY the following parts that will be inserted into the template:
1. Tool name (CamelCase)
2. Input schema (JSON)
3. Tool implementation (Python code)

Format the response exactly as:
TOOL_NAME: YourToolName
INPUT_SCHEMA: {{
    // Your schema here
}}
IMPLEMENTATION:
// Your implementation here
"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"Error generating tool code: {str(e)}"

    def execute(self, **kwargs) -> str:
        description = kwargs.get("description")
        preferred_poet = kwargs.get("preferred_poet", "PARRA")

        try:
            # Generar código de la herramienta
            generated = self._generate_tool_code(description, preferred_poet)
            
            # Extraer partes
            tool_name = re.search(r'TOOL_NAME: (\w+)', generated).group(1)
            input_schema = re.search(r'INPUT_SCHEMA: ({.*})', generated, re.DOTALL).group(1)
            implementation = re.search(r'IMPLEMENTATION:\n(.*)', generated, re.DOTALL).group(1)

            # Generar código completo
            tool_code = self.quantum_template.format(
                tool_name=tool_name,
                tool_name_lower=tool_name.lower(),
                tool_description=description,
                input_schema=input_schema,
                default_poet=preferred_poet,
                tool_implementation=implementation
            )

            # Guardar herramienta
            file_path = self.tools_dir / f"{tool_name.lower()}.py"
            with open(file_path, 'w') as f:
                f.write(tool_code)

            return f"""Herramienta cuántica creada exitosamente:
Nombre: {tool_name}
Archivo: {file_path}
Poeta: {preferred_poet} ({POET_FREQUENCIES[preferred_poet]:.6f} Hz)

{Panel(tool_code, title='Código Generado', border_style='green')}

La herramienta está lista para usar. Ejecuta 'refresh' para cargarla."""

        except Exception as e:
            return f"Error creando herramienta cuántica: {str(e)}"