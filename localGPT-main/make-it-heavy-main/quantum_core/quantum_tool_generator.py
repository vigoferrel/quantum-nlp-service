"""
Generador de herramientas cuánticas
Entrelaza componentes de manera secuencial y elegante
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import importlib.util
import inspect

class QuantumToolGenerator:
    """
    Generador elegante de herramientas cuánticas
    que entrelaza componentes secuencialmente
    """

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent
        self.tools_path = self.base_path.parent / 'tools'
        self.template_path = self.base_path / 'templates'
        
        # Crear directorios necesarios
        self.tools_path.mkdir(exist_ok=True)
        self.template_path.mkdir(exist_ok=True)

    def generate_quantum_tool(
        self,
        tool_name: str,
        description: str,
        components: List[str]
    ) -> bool:
        """
        Genera una nueva herramienta cuántica
        entrelazando los componentes especificados
        """
        try:
            # 1. Validar componentes
            validated = self._validate_components(components)
            if not validated:
                return False

            # 2. Generar código de la herramienta
            tool_code = self._generate_tool_code(
                tool_name,
                description,
                components
            )

            # 3. Escribir archivo
            tool_path = self.tools_path / f"{tool_name.lower()}.py"
            with open(tool_path, 'w') as f:
                f.write(tool_code)

            # 4. Verificar sintaxis
            if not self._verify_syntax(tool_path):
                os.remove(tool_path)
                return False

            # 5. Generar __init__.py si no existe
            self._ensure_init_file()

            return True

        except Exception as e:
            print(f"Error generando herramienta: {str(e)}")
            return False

    def _validate_components(self, components: List[str]) -> bool:
        """Valida que los componentes existan y sean importables"""
        for component in components:
            # Construir path del componente
            component_path = self.base_path / f"{component}.py"
            
            # Verificar existencia
            if not component_path.exists():
                print(f"Componente no encontrado: {component}")
                return False
                
            # Verificar importabilidad
            try:
                spec = importlib.util.spec_from_file_location(
                    component,
                    component_path
                )
                if not spec or not spec.loader:
                    print(f"No se puede importar: {component}")
                    return False
                    
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
            except Exception as e:
                print(f"Error importando {component}: {str(e)}")
                return False

        return True

    def _generate_tool_code(
        self,
        name: str,
        description: str,
        components: List[str]
    ) -> str:
        """Genera el código de la herramienta"""
        # 1. Imports
        imports = [
            'from typing import Dict, Any, Optional, List',
            'from pathlib import Path',
            'import sys',
            '',
            '# Añadir quantum_core al path',
            'quantum_core_path = Path(__file__).parent.parent / "quantum_core"',
            'if str(quantum_core_path) not in sys.path:',
            '    sys.path.append(str(quantum_core_path))',
            ''
        ]

        # 2. Imports de componentes
        for component in components:
            imports.append(f'from {component} import *')

        # 3. Clase de la herramienta
        tool_class = [
            '',
            f'class {name}Tool(BaseTool):',
            f'    name = "{name.lower()}"',
            '    description = """',
            f'    {description}',
            '    """',
            '    input_schema = {',
            '        "type": "object",',
            '        "properties": {',
            '            "input_data": {',
            '                "type": "string",',
            '                "description": "Datos de entrada"',
            '            }',
            '        },',
            '        "required": ["input_data"]',
            '    }',
            '',
            '    def __init__(self):',
            '        super().__init__(7919)',
            '        self.components = {}'
        ]

        # 4. Inicialización de componentes
        for component in components:
            class_name = component.split('.')[-1]
            tool_class.append(
                f'        self.components["{class_name}"] = {class_name}()'
            )

        # 5. Método execute
        execute_method = [
            '',
            '    def execute(self, **kwargs) -> Dict[str, Any]:',
            '        """',
            '        Ejecuta la herramienta entrelazando',
            '        todos los componentes cuánticos',
            '        """',
            '        try:',
            '            # Procesar entrada',
            '            input_data = kwargs.get("input_data")',
            '            if not input_data:',
            '                raise ValueError("Datos de entrada requeridos")',
            '',
            '            results = {}',
            '            quantum_state = {',
            '                "coherence": 1.0,',
            '                "resonance": self.base_frequency,',
            '                "components": {}',
            '            }',
            '',
            '            # Ejecutar componentes secuencialmente',
            '            for name, component in self.components.items():',
            '                result = component.process(input_data)',
            '                results[name] = result',
            '                ',
            '                # Actualizar estado cuántico',
            '                if hasattr(component, "get_quantum_state"):',
            '                    quantum_state["components"][name] = component.get_quantum_state()',
            '',
            '            return {',
            '                "status": "success",',
            '                "results": results,',
            '                "quantum_state": quantum_state',
            '            }',
            '',
            '        except Exception as e:',
            '            return {',
            '                "status": "error",',
            '                "error": str(e),',
            '                "quantum_state": self.get_quantum_state()',
            '            }',
            ''
        ]

        # Unir todo el código
        code = '\n'.join(imports + tool_class + execute_method)
        return code

    def _verify_syntax(self, file_path: Path) -> bool:
        """Verifica la sintaxis del archivo generado"""
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            return True
        except Exception as e:
            print(f"Error de sintaxis: {str(e)}")
            return False

    def _ensure_init_file(self):
        """Asegura que existe un __init__.py"""
        init_path = self.tools_path / '__init__.py'
        if not init_path.exists():
            with open(init_path, 'w') as f:
                f.write('"""Herramientas cuánticas generadas"""\n\n')

# Instancia global del generador
quantum_tool_generator = QuantumToolGenerator()

def generate_tool(
    name: str,
    description: str,
    components: List[str]
) -> bool:
    """Función helper para generar herramientas"""
    return quantum_tool_generator.generate_quantum_tool(
        name,
        description,
        components
    )