#!/usr/bin/env python3
"""
🧪 TEST DIRECTO GEMINI 2.5 FLASH-LITE
Verificación de conectividad y funcionalidad
"""

import asyncio
import aiohttp
import time
import json

async def test_gemini_flash_lite():
    """Test directo de Gemini 2.5 Flash-Lite"""
    
    print("🧪 TEST DIRECTO GEMINI 2.5 FLASH-LITE")
    print("=" * 50)
    
    # Configuración
    api_key = "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"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://test-gemini-flash-lite.local",
        "X-Title": "Test Gemini Flash-Lite"
    }
    
    # Test simple
    payload = {
        "model": "google/gemini-2.5-flash-lite",
        "messages": [{"role": "user", "content": "Hola, ¿cómo estás? Responde en español."}],
        "max_tokens": 100,
        "temperature": 0.1
    }
    
    print(f"🎯 Modelo: google/gemini-2.5-flash-lite")
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🌐 URL: {url}")
    print(f"📝 Query: {payload['messages'][0]['content']}")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                print(f"📊 Status Code: {response.status}")
                print(f"⏱️  Response Time: {time.time() - start_time:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    usage = data.get('usage', {})
                    
                    print(f"✅ ÉXITO!")
                    print(f"📝 Respuesta: {content}")
                    print(f"🔢 Input Tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"🔢 Output Tokens: {usage.get('completion_tokens', 'N/A')}")
                    
                    # Calcular costo
                    input_tokens = usage.get('prompt_tokens', 0)
                    output_tokens = usage.get('completion_tokens', 0)
                    cost = (input_tokens * 0.0000001) + (output_tokens * 0.0000004)
                    print(f"💰 Costo: ${cost:.8f}")
                    
                    return True, content, cost
                    
                else:
                    error_text = await response.text()
                    print(f"❌ ERROR: {response.status}")
                    print(f"📄 Error Response: {error_text}")
                    return False, error_text, 0.0
                    
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False, str(e), 0.0

async def test_multiple_queries():
    """Test con múltiples queries para verificar estabilidad"""
    
    print("\n🧪 TEST MÚLTIPLE QUERIES")
    print("=" * 50)
    
    test_queries = [
        "Explica qué es la inteligencia artificial en 2 líneas.",
        "¿Cuál es la capital de Francia?",
        "Escribe un haiku sobre la tecnología.",
        "Calcula 15 + 27.",
        "¿Qué es el machine learning?"
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🎯 Query {i}: {query}")
        success, response, cost = await test_gemini_flash_lite_single(query)
        results.append({
            "query": query,
            "success": success,
            "response": response,
            "cost": cost
        })
        
        if success:
            print(f"✅ Query {i} exitosa")
        else:
            print(f"❌ Query {i} falló")
        
        # Pausa entre queries
        await asyncio.sleep(1)
    
    # Resumen
    successful = sum(1 for r in results if r["success"])
    total_cost = sum(r["cost"] for r in results if r["success"])
    
    print(f"\n📊 RESUMEN:")
    print(f"✅ Exitosas: {successful}/{len(results)}")
    print(f"💰 Costo Total: ${total_cost:.8f}")
    print(f"📈 Tasa de Éxito: {(successful/len(results)*100):.1f}%")

async def test_gemini_flash_lite_single(query: str):
    """Test single query"""
    
    api_key = "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"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://test-gemini-flash-lite.local",
        "X-Title": "Test Gemini Flash-Lite"
    }
    
    payload = {
        "model": "google/gemini-2.5-flash-lite",
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 200,
        "temperature": 0.1
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    usage = data.get('usage', {})
                    
                    input_tokens = usage.get('prompt_tokens', 0)
                    output_tokens = usage.get('completion_tokens', 0)
                    cost = (input_tokens * 0.0000001) + (output_tokens * 0.0000004)
                    
                    return True, content, cost
                else:
                    error_text = await response.text()
                    return False, error_text, 0.0
                    
    except Exception as e:
        return False, str(e), 0.0

async def main():
    """Función principal"""
    
    # Test simple
    print("🚀 INICIANDO TESTS GEMINI 2.5 FLASH-LITE")
    print("=" * 60)
    
    # Test 1: Query simple
    success, response, cost = await test_gemini_flash_lite()
    
    if success:
        print(f"\n🎉 TEST EXITOSO!")
        print(f"✅ Gemini 2.5 Flash-Lite está funcionando")
        print(f"💰 Costo ultra-económico: ${cost:.8f}")
        
        # Test 2: Múltiples queries
        await test_multiple_queries()
        
    else:
        print(f"\n❌ TEST FALLIDO")
        print(f"🚨 Problema con Gemini 2.5 Flash-Lite")
        print(f"📄 Error: {response}")

if __name__ == "__main__":
    asyncio.run(main())
