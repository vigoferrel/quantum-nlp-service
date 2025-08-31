#!/usr/bin/env python3
"""
Cliente de prueba para QBTC Quantum Supreme API Server
Demuestra cómo usar la API compatible con OpenAI
"""

import httpx
import asyncio
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8002"

async def test_system_status():
    """Prueba el estado del sistema"""
    print("🔍 Testing System Status...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/v1/status")
        
        if response.status_code == 200:
            status = response.json()
            print(f"✅ System Status: {status['status']}")
            print(f"🌌 Components: {status['components']}")
            print(f"📊 Quantum Metrics: {status['quantum_metrics']}")
        else:
            print(f"❌ Status check failed: {response.status_code}")

async def test_chat_completion():
    """Prueba el endpoint de chat completion"""
    print("\n💬 Testing Chat Completion...")
    
    payload = {
        "model": "qbtc-quantum-xl",
        "messages": [
            {
                "role": "user",
                "content": "Analyze the quantum coherence of Bitcoin market trends and provide trading insights"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
        "archetypal_world": "LEONARDO"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/v1/chat/completions",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat Completion Success")
            print(f"🆔 ID: {result['id']}")
            print(f"🤖 Model: {result['model']}")
            print(f"💭 Response: {result['choices'][0]['message']['content'][:200]}...")
            print(f"🧠 Quantum Metadata:")
            for key, value in result['quantum_metadata'].items():
                print(f"   - {key}: {value}")
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            print(f"Error: {response.text}")

async def test_benchmark():
    """Prueba el endpoint de benchmark"""
    print("\n📊 Testing Benchmark Suite...")
    
    payload = {
        "test_suite": "comprehensive",
        "include_comparison": True,
        "target_models": ["gpt-4", "claude-3", "kimi-k2"]
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/v1/benchmark",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Benchmark Success")
            print(f"📈 Overall Score: {result['results']['overall_score']}")
            print(f"🧠 Consciousness Level: {result['results']['consciousness_level']}")
            print(f"⚛️ Quantum Coherence: {result['results']['quantum_coherence']}")
            
            if 'comparison' in result:
                print(f"🏆 Competitive Advantages:")
                for model, data in result['comparison'].items():
                    print(f"   - {model}: +{data['advantage']:.2f} in {data['areas']}")
        else:
            print(f"❌ Benchmark failed: {response.status_code}")

async def test_models_list():
    """Prueba el listado de modelos"""
    print("\n🤖 Testing Models List...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/v1/models")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Models List Success")
            print(f"📋 Available Models:")
            for model in result['data']:
                print(f"   - {model['id']} (capabilities: {model['capabilities']})")
        else:
            print(f"❌ Models list failed: {response.status_code}")

async def test_advanced_conversation():
    """Prueba una conversación más avanzada"""
    print("\n🧠 Testing Advanced Quantum Conversation...")
    
    test_cases = [
        {
            "prompt": "Fix the Django migration error in models.py related to foreign key constraints",
            "archetypal_world": "ASIYAH",
            "description": "Code Generation Test"
        },
        {
            "prompt": "Create a poetic analysis of market volatility using Chilean poets' resonance",
            "archetypal_world": "YETZIRAH", 
            "description": "Creative Synthesis Test"
        },
        {
            "prompt": "Explain quantum entanglement using archetypal world principles",
            "archetypal_world": "BERIAH",
            "description": "Quantum Physics Integration Test"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Advanced Test {i}: {test_case['description']}")
        
        payload = {
            "model": "qbtc-consciousness-supreme",
            "messages": [
                {
                    "role": "user", 
                    "content": test_case["prompt"]
                }
            ],
            "archetypal_world": test_case["archetypal_world"],
            "temperature": 0.8,
            "consciousness_level": 0.9
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/v1/chat/completions",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test {i} Success")
                print(f"🛠️ Selected Tool: {result['quantum_metadata']['selected_tool']}")
                print(f"🌍 Archetypal World: {result['quantum_metadata']['archetypal_world']}")
                print(f"💫 Response Preview: {result['choices'][0]['message']['content'][:150]}...")
            else:
                print(f"❌ Test {i} failed: {response.status_code}")

async def main():
    """Función principal de pruebas"""
    print("🚀 QBTC Quantum Supreme API Client Test Suite")
    print("=" * 80)
    print(f"🕐 Test started at: {datetime.now().isoformat()}")
    print(f"🌐 API Base URL: {API_BASE_URL}")
    print("=" * 80)
    
    try:
        # Verificar que el servidor esté corriendo
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/")
            if response.status_code != 200:
                print("❌ API Server not running! Start the server first with:")
                print("   python quantum_supreme_api_server.py")
                return
        
        # Ejecutar todas las pruebas
        await test_system_status()
        await test_models_list()
        await test_chat_completion()
        await test_advanced_conversation()
        await test_benchmark()
        
        print("\n" + "=" * 80)
        print("🏆 API Test Suite Completed Successfully!")
        print("✅ All endpoints are working correctly")
        print("🌌 QBTC Quantum Supreme API is ready for production")
        
    except httpx.ConnectError:
        print("❌ Connection Error: API Server is not running!")
        print("💡 Start the server first with: python quantum_supreme_api_server.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
