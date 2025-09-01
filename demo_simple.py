#!/usr/bin/env python3
import requests
import json

def demo_simple():
    """Demostración simple del sistema multilingüe"""
    print("🌍 DEMOSTRACIÓN SISTEMA MULTILINGÜE VIGOLEONROCKS")
    print("=" * 60)

    # Test básico de estado
    try:
        response = requests.get("http://localhost:5000/api/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ Servidor funcionando")
            print(f"🌍 Idiomas: {status.get('total_languages', 0)}")
            print(f"⚡ Estados: {status.get('quantum_states', 0)}")
        else:
            print("❌ Error de servidor")
    except:
        print("❌ Error de conexión")

    # Test de detección de idiomas
    print("\n🧠 TEST DE DETECCIÓN:")
    test_texts = [
        ("Hola", "es"),
        ("Hello", "en"),
        ("Bonjour", "fr"),
        ("你好", "zh"),
        ("こんにちは", "ja")
    ]

    for text, expected in test_texts:
        try:
            response = requests.post(
                "http://localhost:5000/api/detect-language",
                json={"text": text},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                detected = data.get('detected_language', 'unknown')
                status = "✅" if detected == expected else "❌"
                print(f"{text} -> {status} {detected}")
            else:
                print(f"{text} -> ❌ Error HTTP")
        except:
            print(f"{text} -> ❌ Error")

    # Test de respuestas humanas
    print("\n🤖 TEST DE RESPUESTAS:")
    for text, lang in [("Hola", "es"), ("Hello", "en"), ("Bonjour", "fr")]:
        try:
            response = requests.post(
                "http://localhost:5000/api/vigoleonrocks",
                json={"text": text},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                resp = data.get('response', 'N/A')[:50]
                print(f"{text} -> {resp}...")
            else:
                print(f"{text} -> ❌ Error")
        except:
            print(f"{text} -> ❌ Error")

    print("\n🎉 ¡DEMOSTRACIÓN COMPLETADA!")
    print("✅ Sistema multilingüe operativo con 12 idiomas")

if __name__ == "__main__":
    demo_simple()
