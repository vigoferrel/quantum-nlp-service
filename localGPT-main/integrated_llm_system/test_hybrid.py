#!/usr/bin/env python3
"""
TEST HYBRID GENERATION - OpenRouter + Ollama Fallback
Prueba la generación híbrida con tu API key de OpenRouter
"""

import asyncio
import sys
import os

# Agregar el directorio actual al path para importar integrate.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar las clases del sistema integrado
from integrate import LLMCore, OpenRouterClient

async def test_hybrid_generation():
    """Prueba la generación híbrida"""
    print("=" * 60)
    print("🧪 TESTING HYBRID GENERATION")
    print("OpenRouter + Ollama Fallback System")
    print("=" * 60)
    
    # Inicializar el sistema
    llm = LLMCore()
    
    # Test prompts
    test_prompts = [
        "Explica qué es la inteligencia artificial en 3 líneas",
        "Escribe un haiku sobre la tecnología",
        "¿Cuál es la diferencia entre machine learning y deep learning?",
        "Describe el futuro de la computación cuántica"
    ]
    
    print("\n🔍 Probando OpenRouter primero...")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i}: {prompt[:50]}... ---")
        
        # Probar generación híbrida con OpenRouter como principal
        result = await llm.generate_hybrid(prompt, "openrouter")
        
        if result["success"]:
            print(f"✅ Éxito ({result['provider']}):")
            print(f"   Modelo: {result['model']}")
            if result.get('usage'):
                usage = result['usage']
                print(f"   Tokens: {usage.get('total_tokens', 'N/A')}")
            print(f"   Respuesta: {result['response'][:100]}...")
            
            if result.get('original_error'):
                print(f"   ⚠️ Fallback de: {result['original_error']}")
        else:
            print(f"❌ Error: {result.get('error', 'Error desconocido')}")
    
    print("\n🔄 Probando Ollama primero...")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i}: {prompt[:50]}... ---")
        
        # Probar generación híbrida con Ollama como principal
        result = await llm.generate_hybrid(prompt, "ollama")
        
        if result["success"]:
            print(f"✅ Éxito ({result['provider']}):")
            print(f"   Modelo: {result['model']}")
            if result.get('usage'):
                usage = result['usage']
                print(f"   Tokens: {usage.get('total_tokens', 'N/A')}")
            print(f"   Respuesta: {result['response'][:100]}...")
            
            if result.get('original_error'):
                print(f"   ⚠️ Fallback de: {result['original_error']}")
        else:
            print(f"❌ Error: {result.get('error', 'Error desconocido')}")
    
    print("\n📊 Estadísticas del sistema:")
    print(f"   Modelos OpenRouter disponibles: {len(llm.list_openrouter_models())}")
    print(f"   Modelos Ollama disponibles: {len(llm.list_models())}")
    print(f"   Historial de conversaciones: {len(llm.get_conversation_history())}")
    
    # Mostrar historial reciente
    print("\n📝 Historial reciente:")
    history = llm.get_conversation_history()
    for i, conv in enumerate(history[-3:], 1):
        print(f"   {i}. {conv['timestamp']} - {conv['model']} ({conv.get('provider', 'N/A')})")
        print(f"      Q: {conv['prompt'][:50]}...")
        print(f"      A: {conv['response'][:50]}...")

async def test_openrouter_direct():
    """Prueba directa de OpenRouter"""
    print("\n" + "=" * 60)
    print("🌐 TESTING OPENROUTER DIRECT")
    print("=" * 60)
    
    openrouter = OpenRouterClient()
    
    # Listar modelos disponibles
    models = openrouter.list_models()
    print(f"📋 Modelos OpenRouter disponibles: {len(models)}")
    for i, model in enumerate(models[:5], 1):
        print(f"   {i}. {model}")
    
    # Probar generación directa
    test_prompt = "Explica brevemente qué es la computación cuántica"
    print(f"\n🧪 Probando generación directa con: {test_prompt}")
    
    result = await openrouter.generate(test_prompt)
    
    if result["success"]:
        print(f"✅ Éxito:")
        print(f"   Modelo: {result['model']}")
        print(f"   Respuesta: {result['response']}")
        if result.get('usage'):
            usage = result['usage']
            print(f"   Tokens usados: {usage.get('total_tokens', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Error desconocido')}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema híbrido...")
    
    # Ejecutar pruebas
    asyncio.run(test_hybrid_generation())
    asyncio.run(test_openrouter_direct())
    
    print("\n✅ Pruebas completadas!")
