#!/usr/bin/env python3
import requests
import json
import time

def verificar_sistema():
    """Verificación completa del sistema VIGOLEONROCKS"""
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA VIGOLEONROCKS")
    print("=" * 60)
    
    # URLs a verificar
    urls = {
        "Local": "http://localhost:5000",
        "Producción": "https://vigoleonrocks-frontend-bpxpc6.dokploy.app"  # URL de Dokploy
    }
    
    for nombre, base_url in urls.items():
        print(f"\n🌐 VERIFICANDO: {nombre}")
        print("-" * 40)
        
        try:
            # 1. Verificar estado del sistema
            print("📊 Estado del sistema...")
            status_response = requests.get(f"{base_url}/api/status", timeout=10)
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"✅ Servidor: {status.get('status', 'N/A')}")
                print(f"🌍 Idiomas: {status.get('total_languages', 0)}")
                print(f"⚡ Estados: {status.get('quantum_states', 0)}")
                print(f"🎯 Supremacy: {status.get('supremacy_score', 0)}")
                print(f"⏱️  Uptime: {status.get('uptime', 'N/A')}")
            else:
                print(f"❌ Error HTTP: {status_response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {str(e)[:50]}")
            continue
            
        try:
            # 2. Verificar detección de idiomas
            print("\n🧠 Test de detección de idiomas...")
            test_texts = [
                ("Hola", "es"),
                ("Hello", "en"),
                ("Bonjour", "fr"),
                ("你好", "zh"),
                ("こんにちは", "ja")
            ]
            
            for text, expected in test_texts:
                detect_response = requests.post(
                    f"{base_url}/api/detect-language",
                    json={"text": text},
                    timeout=10
                )
                if detect_response.status_code == 200:
                    result = detect_response.json()
                    detected = result.get('detected_language', 'N/A')
                    status = "✅" if detected == expected else "❌"
                    print(f"  {text} -> {status} {detected} (esperado: {expected})")
                else:
                    print(f"  {text} -> ❌ Error HTTP: {detect_response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en detección: {str(e)[:50]}")
            
        try:
            # 3. Verificar respuestas humanas
            print("\n🤖 Test de respuestas humanas...")
            test_queries = [
                ("Hola", "es"),
                ("Hello", "en"),
                ("Bonjour", "fr")
            ]
            
            for query, lang in test_queries:
                response = requests.post(
                    f"{base_url}/api/vigoleonrocks",
                    json={"text": query, "language": lang},
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    human_response = result.get('human_response', 'N/A')
                    print(f"  {query} -> ✅ {human_response[:50]}...")
                else:
                    print(f"  {query} -> ❌ Error HTTP: {response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en respuestas: {str(e)[:50]}")
            
        try:
            # 4. Verificar página principal
            print("\n🏠 Test de página principal...")
            main_response = requests.get(f"{base_url}/", timeout=10)
            if main_response.status_code == 200:
                print("✅ Página principal accesible")
            else:
                print(f"❌ Error en página principal: {main_response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en página principal: {str(e)[:50]}")
    
    print("\n" + "=" * 60)
    print("🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    verificar_sistema()
