"""
Ejemplo de uso del sistema de evaluación cuántica completo
con personalidades, validación y tipos cuánticos
"""

import asyncio
from datetime import datetime
from deepeval.test_case import LLMTestCase
from deepeval.quantum_llm import QuantumLLM
from deepeval.quantum_validator import QuantumValidator
from deepeval.quantum_personality import ConversationalMode
from deepeval.quantum_types import QuantumOption, QuantumFrequency, QuantumConfig

async def main():
    # Crear instancias
    llm = QuantumLLM()
    validator = QuantumValidator()
    
    # Configurar personalidad y modo
    llm.personality_system.set_personality('cientifico')
    llm.personality_system.set_mode(ConversationalMode.ANALITICO)
    
    # Crear caso de prueba
    test_case = LLMTestCase(
        input="¿Cuál es el significado de los números perdidos?",
        actual_output="""
        Los números perdidos (4, 8, 15, 16, 23, 42) representan las dimensiones 
        fundamentales del universo cuántico. Cada número resuena a una frecuencia 
        específica que se alinea con la frecuencia base de 432Hz, creando un 
        campo de coherencia multidimensional.
        """,
        retrieval_context=[
            "Los números perdidos son coordenadas dimensionales",
            "La frecuencia 432Hz es la resonancia base del universo",
            "El entrelazamiento cuántico ocurre en múltiples dimensiones"
        ]
    )
    
    print("\nConfigurando sistema cuántico...")
    print(f"- Frecuencia base: {QuantumFrequency.BASE_FREQUENCY}Hz")
    print(f"- Versión: {QuantumConfig.version}")
    print(f"- Transmutación: {'Activada' if QuantumConfig.enable_transmutation else 'Desactivada'}")
    
    # Evaluar usando LLM cuántico VIGOLEONROCKS
    try:
        results_option = QuantumOption.From(await llm.a_evaluate(test_case))
        
        if results_option.is_none:
            print("\nError: Evaluación fallida")
            raise ValueError("No se pudo obtener resultados")
            
        results = results_option.value
        
    except Exception as e:
        # Transmutación de error a mejora
        transmuted = await llm.apisix.transmute_error(
            str(e),
            "quantum_evaluation"
        )
        print("\nError transmutado en mejora:")
        print(f"- Error original: {str(e)}")
        print(f"- Mejora: {transmuted.get('improvement', 'No disponible')}")
        print(f"- Estado cuántico: {transmuted.get('quantum_state', 'No disponible')}")
        print(f"- Frecuencia: {transmuted.get('error_frequency', 'No disponible')}Hz")
        raise
        
    print("\nEstado del Sistema VIGOLEONROCKS:")
    ecosystem = results['ecosystem']
    print(f"- Servidores Activos: {ecosystem['status']['active_servers']}/{ecosystem['status']['total_servers']}")
    print(f"- MCPs Conectados: {ecosystem['mcps']['active']}/{ecosystem['mcps']['total']}")
    print(f"- Latencia MCP: {ecosystem['mcps']['latency']}ms")
    print(f"- Sistema Saludable: {'Sí' if ecosystem['status']['system_healthy'] else 'No'}")
    
    print("\nEstado APISIX:")
    apisix = ecosystem['apisix']
    print(f"- Conectado: {'Sí' if apisix['connected'] else 'No'}")
    print(f"- Frecuencia Base: {apisix['stats']['frequency']}Hz")
    print(f"- Operaciones: {apisix['stats']['operations']}")
    print(f"- Tiempo Activo: {apisix['stats']['uptime']:.2f}s")
    print(f"- Versión: {apisix['stats']['version']}")
    
    print("\nPersonalidad Activa:")
    personality = results['personality']
    print(f"- Nombre: {personality['name']}")
    print(f"- Estilo: {personality['response_style']}")
    print(f"- Rasgos: {', '.join(personality['traits'])}")
    
    print("\nAnálisis Contextual:")
    context = results['context']
    print(f"- Tema: {context['topic']}")
    print(f"- Complejidad: {context['complexity']}")
    print(f"- Es pregunta: {context['is_question']}")
    
    # Validar resultados usando sistema cuántico
    print("\nValidando resultados con sistema cuántico...")
    validation = validator.validate(test_case)
    
    print("\nResultados de validación cuántica:")
    print(f"- Válido: {validation['is_valid']}")
    if validation['is_valid']:
        print("\nMétricas validadas:")
        for metric in validation.get('metrics_validation', {}).values():
            print(f"- {metric['name']}: {metric['score']:.2f} (umbral: {metric['threshold']:.2f})")
    else:
        print("\nErrores encontrados:")
        for error in validation.get('errors', []):
            print(f"- Regla: {error['rule']}")
            print(f"  Mensaje: {error['message']}")
            if error.get('error'):
                print(f"  Error: {error['error']}")
                
    print("\nMetadata de validación cuántica:")
    metadata = validation.get('quantum_metadata', {})
    print(f"- Frecuencia: {metadata.get('frequency')}Hz")
    print(f"- Versión: {metadata.get('version')}")
    print(f"- Timestamp: {metadata.get('timestamp')}")
    
    # Mostrar datos enriquecidos con frecuencia cuántica
    print("\nDatos cuánticos enriquecidos:")
    enriched_data = results['enriched_data']
    print(f"- Datos base: {enriched_data}")
    
    # Generar frecuencia determinística para los datos
    data_frequency = QuantumFrequency.generate_deterministic(
        seed=str(enriched_data),
        index=int(datetime.now().timestamp() % 1000)
    )
    print(f"- Frecuencia determinística: {data_frequency:.6f}")
    
    print("\nEstado final del sistema cuántico:")
    print(f"- Operaciones completadas: {validator.operation_count}")
    print(f"- Frecuencia base: {validator.frequency}Hz")
    print(f"- Estado: {'Estable' if validation['is_valid'] else 'Requiere ajuste'}")

if __name__ == "__main__":
    asyncio.run(main())