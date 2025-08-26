"""
Descubrimiento dinámico de herramientas para el sistema cuántico
"""

from typing import Dict, Any
from .base_tool import BaseTool
from .calculator_tool import CalculatorTool
from .read_file_tool import ReadFileTool
from .search_tool import SearchTool
from .task_done_tool import TaskDoneTool
from .write_file_tool import WriteFileTool
from .quantum_transmuter_tool import QuantumTransmuterTool

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

def discover_tools(config: Dict[str, Any], silent: bool = False) -> Dict[str, BaseTool]:
    """
    Descubre y carga dinámicamente todas las herramientas disponibles,
    incluyendo la herramienta de transmutación cuántica.
    """
    tools = {
        'calculate': CalculatorTool(),
        'read_file': ReadFileTool(),
        'search': SearchTool(),
        'mark_task_complete': TaskDoneTool(),
        'write_file': WriteFileTool(),
        'quantum_transmute': QuantumTransmuterTool()
    }

    if not silent:
        print("\nHerramientas descubiertas:")
        for name, tool in tools.items():
            print(f"- {name}: {tool.description}")
        
        print("\nFrecuencias poéticas cuánticas:")
        for poet, freq in POET_FREQUENCIES.items():
            print(f"- {poet}: {freq:.6f} Hz")

    return tools