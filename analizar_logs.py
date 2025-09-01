#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def analizar_logs():
    """Análisis detallado de los logs del sistema VIGOLEONROCKS"""
    print("📊 ANÁLISIS DETALLADO DE LOGS - VIGOLEONROCKS")
    print("=" * 60)
    
    try:
        # 1. Estado general del sistema
        print("\n🔍 ESTADO GENERAL DEL SISTEMA:")
        print("-" * 40)
        status_response = requests.get("http://localhost:5000/api/status", timeout=5)
        if status_response.status_code == 200:
            status = status_response.json()
            
            print(f"✅ Servidor: {status.get('status', 'N/A')}")
            print(f"🏷️  Nombre: {status.get('server', 'N/A')}")
            print(f"👤 Perfil: {status.get('profile', 'N/A')}")
            print(f"🌍 Idiomas: {status.get('total_languages', 0)}")
            print(f"⚡ Estados Cuánticos: {status.get('quantum_states', 0)}")
            print(f"🎯 Supremacy Score: {status.get('supremacy_score', 0)}")
            print(f"📊 Tasa de Éxito Humana: {status.get('human_success_rate', 0) * 100:.1f}%")
            print(f"📈 Requests Procesados: {status.get('requests', 0)}")
            
            uptime = status.get('uptime', {})
            print(f"⏱️  Uptime: {uptime.get('formatted', 'N/A')}")
            
            print(f"\n🔧 Características:")
            features = status.get('features', [])
            for feature in features:
                print(f"  • {feature}")
                
            print(f"\n🌍 Idiomas Soportados:")
            languages = status.get('languages_supported', [])
            for lang in languages:
                print(f"  • {lang.upper()}")
                
        else:
            print(f"❌ Error al obtener estado: {status_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return
    
    # 2. Test de funcionalidades críticas
    print("\n🧪 TEST DE FUNCIONALIDADES CRÍTICAS:")
    print("-" * 40)
    
    # Test de detección de idiomas
    print("\n🧠 Detección de Idiomas:")
    test_cases = [
        ("Hola", "es"),
        ("Hello", "en"),
        ("Bonjour", "fr"),
        ("你好", "zh"),
        ("こんにちは", "ja"),
        ("Привет", "ru"),
        ("مرحبا", "ar")
    ]
    
    success_count = 0
    for text, expected in test_cases:
        try:
            response = requests.post(
                "http://localhost:5000/api/detect-language",
                json={"text": text},
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                detected = result.get('detected_language', 'N/A')
                if detected == expected:
                    print(f"  ✅ {text} -> {detected}")
                    success_count += 1
                else:
                    print(f"  ❌ {text} -> {detected} (esperado: {expected})")
            else:
                print(f"  ❌ {text} -> Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {text} -> Error: {str(e)[:30]}")
    
    detection_accuracy = (success_count / len(test_cases)) * 100
    print(f"\n📊 Precisión de Detección: {detection_accuracy:.1f}%")
    
    # Test de respuestas humanas
    print("\n🤖 Respuestas Humanas:")
    human_tests = [
        ("Hola", "es"),
        ("Hello", "en"),
        ("Bonjour", "fr")
    ]
    
    human_success = 0
    for query, lang in human_tests:
        try:
            response = requests.post(
                "http://localhost:5000/api/vigoleonrocks",
                json={"text": query, "language": lang},
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                human_response = result.get('human_response', 'N/A')
                if human_response != 'N/A':
                    print(f"  ✅ {query} -> {human_response[:50]}...")
                    human_success += 1
                else:
                    print(f"  ❌ {query} -> Respuesta vacía")
            else:
                print(f"  ❌ {query} -> Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {query} -> Error: {str(e)[:30]}")
    
    human_accuracy = (human_success / len(human_tests)) * 100
    print(f"\n📊 Precisión de Respuestas Humanas: {human_accuracy:.1f}%")
    
    # 3. Resumen del análisis
    print("\n📋 RESUMEN DEL ANÁLISIS:")
    print("-" * 40)
    print(f"✅ Servidor: OPERATIVO")
    print(f"✅ Detección de Idiomas: {detection_accuracy:.1f}%")
    print(f"✅ Respuestas Humanas: {human_accuracy:.1f}%")
    print(f"✅ Uptime: {uptime.get('formatted', 'N/A')}")
    print(f"✅ Requests Procesados: {status.get('requests', 0)}")
    
    # 4. Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    print("-" * 40)
    if detection_accuracy < 100:
        print("⚠️  Mejorar precisión de detección de idiomas")
    if human_accuracy < 100:
        print("⚠️  Revisar generación de respuestas humanas")
    if status.get('requests', 0) < 10:
        print("ℹ️  Sistema recién iniciado, monitorear rendimiento")
    
    print("✅ Sistema VIGOLEONROCKS operativo y funcional")

if __name__ == "__main__":
    analizar_logs()
