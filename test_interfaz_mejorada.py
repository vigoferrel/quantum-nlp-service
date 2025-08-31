#!/usr/bin/env python3
import requests
import json
import time

def test_interfaz_mejorada():
    print("🎨 PROBANDO INTERFAZ WEB MEJORADA")
    print("=" * 50)
    
    # Probar página principal
    print("\n🌐 PROBANDO PÁGINA PRINCIPAL:")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Página principal cargada correctamente")
            print(f"📄 Tamaño: {len(response.text)} caracteres")
            if "VIGOLEONROCKS" in response.text:
                print("✅ Título VIGOLEONROCKS encontrado")
            if "IA Humana Avanzada" in response.text:
                print("✅ Subtítulo mejorado encontrado")
            if "Supremacy Score" in response.text:
                print("✅ Estadísticas encontradas")
            if "APIs Disponibles" in response.text:
                print("✅ Sección de APIs encontrada")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando: {e}")
    
    # Probar estado del sistema mejorado
    print("\n📊 PROBANDO ESTADO DEL SISTEMA MEJORADO:")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:5000/api/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estado del sistema obtenido")
            print(f"🖥️  Servidor: {data.get('server', 'N/A')}")
            print(f"📈 Estado: {data.get('status', 'N/A')}")
            print(f"⏱️  Uptime: {data.get('uptime', {}).get('formatted', 'N/A')}")
            print(f"📊 Requests: {data.get('requests', 'N/A')}")
            print(f"🎯 Perfil: {data.get('profile', 'N/A')}")
            print(f"⚛️  Estados cuánticos: {data.get('quantum_states', 'N/A')}")
            print(f"⭐ Supremacy Score: {data.get('supremacy_score', 'N/A')}")
            print(f"🌍 Idiomas: {data.get('languages_supported', 'N/A')}")
            print(f"✨ Características: {len(data.get('features', []))} funciones")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Probar funcionalidad principal
    print("\n🧠 PROBANDO FUNCIONALIDAD PRINCIPAL:")
    print("-" * 35)
    
    test_cases = [
        {"text": "Hola, ¿cómo estás?", "lang": "es"},
        {"text": "Hello, what can you do?", "lang": "en"},
        {"text": "Olá, quem é você?", "lang": "pt"}
    ]
    
    for i, test in enumerate(test_cases, 1):
        try:
            response = requests.post(
                "http://localhost:5000/api/vigoleonrocks",
                json={"text": test["text"]},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Test {i}: {test['text'][:20]}...")
                print(f"   🌍 Idioma: {data.get('language', 'N/A')}")
                print(f"   ⚡ Tiempo: {data.get('processing_time', 'N/A')}ms")
                print(f"   🎯 Método: {data.get('method', 'N/A')}")
            else:
                print(f"❌ Test {i}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ Test {i}: Error - {e}")
    
    print("\n🎉 PRUEBA DE INTERFAZ COMPLETADA")
    print("=" * 50)

if __name__ == "__main__":
    test_interfaz_mejorada()
