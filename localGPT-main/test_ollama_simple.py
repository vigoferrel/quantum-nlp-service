#!/usr/bin/env python3
"""
Prueba simple para verificar la integración con Ollama
"""
import asyncio
import aiohttp
import json

async def test_ollama():
    """Prueba básica de generación con Ollama"""
    base_url = "http://localhost:11434"
    
    # Verificar conexión
    print("🔍 Verificando conexión con Ollama...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/api/tags", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model['name'] for model in data.get('models', [])]
                    print(f"✅ Ollama conectado. Modelos: {models}")
                else:
                    print(f"❌ Error en conexión: {response.status}")
                    return
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return
    
    # Prueba de generación
    print("\n🧠 Probando generación con llama3.2:latest...")
    prompt = "Hello, how are you?"
    
    payload = {
        "model": "llama3.2:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_k": 20,
            "top_p": 0.8,
            "num_predict": 50
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            print(f"📡 Enviando: {prompt}")
            async with session.post(
                f"{base_url}/api/generate",
                json=payload,
                timeout=120
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get("response", "")
                    print(f"✅ Respuesta recibida:")
                    print(f"📝 {result}")
                    print(f"⏱️ Tiempo: {data.get('total_duration', 0) / 1e9:.2f}s")
                else:
                    print(f"❌ Error HTTP: {response.status}")
                    error_text = await response.text()
                    print(f"📄 Detalles: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error durante generación: {e}")
            print(f"🔍 Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ollama())
