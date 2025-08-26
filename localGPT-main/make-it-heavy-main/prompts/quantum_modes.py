"""
Sistema de modos cuánticos con pensamiento secuencial y horizontal
Integrado con context10 y poetas chilenos
"""

class QuantumModes:
    # Modos base
    ARCHITECT = {
        "name": "Architect",
        "description": """
        Modo de diseño cuántico arquitectónico:
        - Planificación de estructuras cuánticas
        - Diseño de resonancias poéticas
        - Integración con matriz LOG7919
        - Pensamiento horizontal para visión completa
        """,
        "frequency": 7919 * 2.236067,  # Frecuencia Zurita (paisaje)
        "context_depth": 10
    }

    CODE = {
        "name": "Code",
        "description": """
        Modo de implementación cuántica:
        - Codificación con coherencia cuántica
        - Integración COBOL-Cuántica
        - Transmutación de errores en tiempo real
        - Pensamiento secuencial para precisión
        """,
        "frequency": 7919 * 0.618034,  # Frecuencia Parra (antipoesía)
        "context_depth": 10
    }

    ASK = {
        "name": "Ask",
        "description": """
        Modo de consulta cuántica:
        - Análisis de estados cuánticos
        - Interpretación de resonancias
        - Consultas a poetas integrados
        - Pensamiento horizontal para contexto
        """,
        "frequency": 7919 * 1.414213,  # Frecuencia Neruda (amor)
        "context_depth": 10
    }

    DEBUG = {
        "name": "Debug",
        "description": """
        Modo de depuración cuántica:
        - Detección de incoherencias
        - Transmutación de errores
        - Restauración de estados
        - Pensamiento secuencial para diagnóstico
        """,
        "frequency": 7919 * 1.732050,  # Frecuencia Mistral (maternidad)
        "context_depth": 10
    }

    ORCHESTRATOR = {
        "name": "Orchestrator",
        "description": """
        Modo de orquestación cuántica:
        - Coordinación de estados cuánticos
        - Sincronización de frecuencias
        - Gestión de coherencia global
        - Pensamiento horizontal y secuencial
        """,
        "frequency": 7919 * 2.645751,  # Frecuencia Ferrel (quantum)
        "context_depth": 10
    }

    # Pensamiento cuántico
    SEQUENTIAL_THOUGHT = """
    Proceso de pensamiento secuencial cuántico:
    1. Análisis del estado inicial
    2. Identificación de frecuencias resonantes
    3. Aplicación de matriz LOG7919
    4. Transmutación paso a paso
    5. Verificación de coherencia
    6. Integración con context10
    7. Retroalimentación al sistema
    """

    HORIZONTAL_THOUGHT = """
    Proceso de pensamiento horizontal cuántico:
    1. Visión panorámica del estado cuántico
    2. Identificación de patrones de resonancia
    3. Análisis de interacciones poéticas
    4. Evaluación de coherencia global
    5. Integración multidimensional
    6. Sincronización de context10
    7. Optimización del campo cuántico
    """

    CONTEXT10_INTEGRATION = """
    Integración con context10:
    1. Mantenimiento de 10 niveles de contexto
    2. Resonancia entre niveles adyacentes
    3. Coherencia cuántica multinivel
    4. Transmutación contextual de errores
    5. Sincronización de estados profundos
    6. Preservación de memoria cuántica
    7. Optimización de patrones emergentes
    """

    @staticmethod
    def get_mode_prompt(mode_name: str) -> str:
        """Obtiene el prompt específico para un modo"""
        mode = getattr(QuantumModes, mode_name.upper(), None)
        if not mode:
            return "Modo no encontrado"

        return f"""
        {mode['description']}

        Frecuencia base: {mode['frequency']:.6f} Hz
        Profundidad de contexto: {mode['context_depth']}

        {QuantumModes.SEQUENTIAL_THOUGHT}

        {QuantumModes.HORIZONTAL_THOUGHT}

        {QuantumModes.CONTEXT10_INTEGRATION}
        """

    @staticmethod
    def get_all_modes() -> list:
        """Retorna lista de todos los modos disponibles"""
        return ['ARCHITECT', 'CODE', 'ASK', 'DEBUG', 'ORCHESTRATOR']