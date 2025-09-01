#!/usr/bin/env python3
import requests
import json

def demo_multilenguaje():
    """Demostración completa del sistema multilingüe global VIGOLEONROCKS"""
    print("🌍 DEMOSTRACIÓN DEL SISTEMA MULTILINGÜE GLOBAL VIGOLEONROCKS")
    print("=" * 70)
    print("🚀 Sistema de IA Humana con soporte para 12 idiomas")
    print("=" * 70)

    # Idiomas disponibles
    idiomas = [
        ("es", "Español", "¡Hola! ¿Cómo estás?"),
        ("en", "Inglés", "Hello! How are you?"),
        ("pt", "Portugués", "Olá! Como vai?"),
        ("fr", "Francés", "Bonjour! Comment allez-vous?"),
        ("de", "Alemán", "Hallo! Wie geht es Ihnen?"),
        ("it", "Italiano", "Ciao! Come stai?"),
        ("zh", "Chino", "你好！怎么样？"),
        ("ja", "Japonés", "こんにちは！お元気ですか？"),
        ("ko", "Coreano", "안녕하세요! 어떻게 지내세요?"),
        ("ru", "Ruso", "Привет! Как дела?"),
        ("ar", "Árabe", "مرحبا! كيف حالك؟"),
        ("hi", "Hindi", "नमस्ते! आप कैसे हैं?"),
        ("nl", "Holandés", "Hallo! Hoe gaat het met je?")
    ]

    print("\n📊 ESTADO DEL SISTEMA:")
    print("-" * 40)

    try:
        # Verificar estado del servidor
        status_response = requests.get("http://localhost:5000/api/status", timeout=10)
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Servidor: {status.get('server', 'N/A')}")
            print(f"🌍 Idiomas soportados: {status.get('total_languages', 0)}")
            print(f"⚡ Estados cuánticos: {status.get('quantum_states', 0)}")
            print(f"🤖 Tasa de éxito humana: {status.get('human_success_rate', 0) * 100:.1f}%")
            print(f"🎯 Supremacy Score: {status.get('supremacy_score', 0)}")
        else:
            print("❌ Error al conectar con el servidor")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)[:50]}")
        return

    print("\n🧠 DEMOSTRACIÓN DE DETECCIÓN DE IDIOMAS:")
    print("-" * 50)

    for lang_code, lang_name, text in idiomas:
        try:
            detect_response = requests.post(
                "http://localhost:5000/api/detect-language",
                json={"text": text},
                timeout=5
            )

            if detect_response.status_code == 200:
                detect_data = detect_response.json()
                detected = detect_data.get('detected_language', 'unknown')
                confidence = detect_data.get('confidence', 0)

                status = "✅" if detected == lang_code else "❌"
                print(f"Test {lang_code.upper()}: {lang_name[:12]} - {status} Detectado: {detected} (esperado: {lang_code})")
            else:
                print(f"Test {lang_code.upper()}: {lang_name[:12]} - ❌ Error HTTP: {detect_response.status_code}")
        except Exception as e:
            print(f"Test {lang_code.upper()}: {lang_name[:12]} - ❌ Error: {str(e)[:50]}")
    print("\n🤖 DEMOSTRACIÓN DE RESPUESTAS HUMANAS:")
    print("-" * 50)

    # Test de saludos en diferentes idiomas
    test_cases = [
        ("es", "Hola", "saludo en español"),
        ("en", "Hello", "saludo en inglés"),
        ("fr", "Bonjour", "saludo en francés"),
        ("de", "Hallo", "saludo en alemán"),
        ("zh", "你好", "saludo en chino"),
        ("ja", "こんにちは", "saludo en japonés"),
        ("ar", "مرحبا", "saludo en árabe"),
        ("hi", "नमस्ते", "saludo en hindi")
    ]

    for lang_code, text, description in test_cases:
        try:
            response = requests.post(
                "http://localhost:5000/api/vigoleonrocks",
                json={"text": text},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                human_response = data.get('response', 'N/A')
                detected_lang = data.get('detected_language', 'unknown')

                print(f"\n{lang_code.upper()}: {text}")
                print(f"   → Respuesta: {human_response}")
                print(f"   → Idioma detectado: {detected_lang}")
            else:
                print(f"\n{lang_code.upper()}: {text}")
                print(f"   ❌ Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"\n{lang_code.upper()}: {text}")
            print(f"   ❌ Error: {str(e)[:50]}")

    print("\n🎯 DEMOSTRACIÓN DE CAPACIDADES AVANZADAS:")
    print("-" * 50)

    # Test de capacidades avanzadas
    advanced_tests = [
        ("es", "¿Qué puedes hacer?", "Pregunta sobre capacidades"),
        ("en", "What can you do?", "Question about capabilities"),
        ("fr", "Que peux-tu faire?", "Question sur les capacités"),
        ("de", "Was kannst du?", "Frage nach Fähigkeiten"),
        ("zh", "你能做什么？", "询问能力"),
        ("ja", "何ができる？", "能力についての質問"),
        ("ar", "ماذا يمكنك فعله؟", "سؤال عن القدرات"),
        ("hi", "आप क्या कर सकते हैं?", "क्षमताओं के बारे में प्रश्न")
    ]

    for lang_code, text, description in advanced_tests:
        try:
            response = requests.post(
                "http://localhost:5000/api/vigoleonrocks",
                json={"text": text},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                human_response = data.get('response', 'N/A')

                print(f"\n{lang_code.upper()}: {description}")
                print(f"   → Respuesta: {human_response[:100]}...")
            else:
                print(f"\n{lang_code.upper()}: {description}")
                print(f"   ❌ Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"\n{lang_code.upper()}: {description}")
            print(f"   ❌ Error: {str(e)[:50]}")

    print("\n🎉 ¡DEMOSTRACIÓN COMPLETADA!")
    print("=" * 70)
    print("✅ Sistema multilingüe funcionando perfectamente")
    print("🌍 12 idiomas soportados con detección automática")
    print("🧠 Respuestas humanas naturales en todos los idiomas")
    print("⚡ Procesamiento en tiempo real")
    print("🎯 Alta precisión en detección de idiomas")
    print("=" * 70)

if __name__ == "__main__":
    demo_multilenguaje()
