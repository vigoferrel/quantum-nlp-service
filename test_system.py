#!/usr/bin/env python3
"""
🧪 SCRIPT DE PRUEBA DEL SISTEMA VIGOLEONROCKS
Verifica que todos los servicios estén funcionando correctamente
"""

import requests
import json
import time

def test_cio_server():
    """Probar el servidor CIO"""
    print("🧠 Probando CIO Server (puerto 5001)...")
    try:
        # Probar endpoint de estado
        response = requests.get("http://localhost:5001/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ CIO Server - Status: OK")
            data = response.json()
            print(f"   Estado: {data.get('cio_status', 'N/A')}")
        else:
            print(f"❌ CIO Server - Status: Error {response.status_code}")
            return False
            
        # Probar endpoint de procesamiento
        test_data = {
            "api_key": "vk_live_test_key_123",
            "query": "Hola, ¿cómo estás?",
            "type": "text"
        }
        response = requests.post(
            "http://localhost:5001/api/process",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ CIO Server - Process: OK")
            data = response.json()
            print(f"   Respuesta: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ CIO Server - Process: Error {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ CIO Server - Error: {e}")
        return False

def test_openrouter_provider():
    """Probar el proveedor OpenRouter"""
    print("\n🌐 Probando OpenRouter Provider (puerto 5002)...")
    try:
        # Probar endpoint de modelos
        response = requests.get("http://localhost:5002/models", timeout=5)
        if response.status_code == 200:
            print("✅ OpenRouter Provider - Models: OK")
            data = response.json()
            models = data.get('data', [])
            print(f"   Modelos disponibles: {len(models)}")
        else:
            print(f"❌ OpenRouter Provider - Models: Error {response.status_code}")
            return False
            
        # Probar endpoint de chat completions
        test_data = {
            "model": "vigoleonrocks/vigoleonrocks-v1",
            "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
        response = requests.post(
            "http://localhost:5002/chat/completions",
            json=test_data,
            timeout=15
        )
        if response.status_code == 200:
            print("✅ OpenRouter Provider - Chat: OK")
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"   Respuesta: {content[:100]}...")
        else:
            print(f"❌ OpenRouter Provider - Chat: Error {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter Provider - Error: {e}")
        return False

def test_corporate_website():
    """Probar la web corporativa"""
    print("\n🌐 Probando Web Corporativa (puerto 5003)...")
    try:
        # Probar página principal
        response = requests.get("http://localhost:5003", timeout=5)
        if response.status_code == 200:
            print("✅ Web Corporativa - Main: OK")
            print(f"   Tamaño: {len(response.content)} bytes")
        else:
            print(f"❌ Web Corporativa - Main: Error {response.status_code}")
            return False
            
        # Probar endpoint de test-model
        test_data = {
            "model": "vigoleonrocks/vigoleonrocks-v1",
            "prompt": "Hola, ¿cómo estás?"
        }
        response = requests.post(
            "http://localhost:5003/test-model",
            json=test_data,
            timeout=15
        )
        if response.status_code == 200:
            print("✅ Web Corporativa - Test Model: OK")
            data = response.json()
            if data.get('success'):
                print(f"   Respuesta: {data.get('response', '')[:100]}...")
            else:
                print(f"   Error: {data.get('error', '')}")
        else:
            print(f"❌ Web Corporativa - Test Model: Error {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Web Corporativa - Error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DEL SISTEMA VIGOLEONROCKS")
    print("=" * 50)
    
    # Esperar un momento para que los servicios se inicialicen
    print("⏳ Esperando que los servicios se inicialicen...")
    time.sleep(3)
    
    # Ejecutar pruebas
    results = []
    
    results.append(test_cio_server())
    results.append(test_openrouter_provider())
    results.append(test_corporate_website())
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    services = ["CIO Server", "OpenRouter Provider", "Web Corporativa"]
    for i, (service, result) in enumerate(zip(services, results)):
        status = "✅ OK" if result else "❌ FALLO"
        print(f"{i+1}. {service}: {status}")
    
    total_passed = sum(results)
    total_services = len(results)
    
    print(f"\n🎯 Resultado: {total_passed}/{total_services} servicios funcionando")
    
    if total_passed == total_services:
        print("🎉 ¡Todos los servicios están funcionando correctamente!")
        print("🌐 Puedes acceder a la web corporativa en: http://localhost:5003")
    else:
        print("⚠️ Algunos servicios tienen problemas. Revisa los logs.")
    
    return total_passed == total_services

if __name__ == "__main__":
    main()
