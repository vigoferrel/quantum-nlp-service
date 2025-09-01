#!/usr/bin/env python3
import requests
import json

def test_multilenguaje_global():
    """Prueba del sistema multilingüe global con 12 idiomas"""
    print("🌍 PRUEBA DEL SISTEMA MULTILINGÜE GLOBAL")
    print("=" * 60)

    # Test cases para cada idioma
    test_cases = [
        # Español
        {"text": "Hola, ¿cómo estás?", "expected_lang": "es", "description": "Español"},
        {"text": "¿Quién eres?", "expected_lang": "es", "description": "Español"},

        # Inglés
        {"text": "Hello, how are you?", "expected_lang": "en", "description": "Inglés"},
        {"text": "What can you do?", "expected_lang": "en", "description": "Inglés"},

        # Portugués
        {"text": "Olá, como vai?", "expected_lang": "pt", "description": "Portugués"},
        {"text": "O que você pode fazer?", "expected_lang": "pt", "description": "Portugués"},

        # Francés
        {"text": "Bonjour, comment allez-vous?", "expected_lang": "fr", "description": "Francés"},
        {"text": "Qui es-tu?", "expected_lang": "fr", "description": "Francés"},

        # Alemán
        {"text": "Hallo, wie geht es Ihnen?", "expected_lang": "de", "description": "Alemán"},
        {"text": "Was kannst du?", "expected_lang": "de", "description": "Alemán"},

        # Italiano
        {"text": "Ciao, come stai?", "expected_lang": "it", "description": "Italiano"},
        {"text": "Cosa puoi fare?", "expected_lang": "it", "description": "Italiano"},

        # Chino
        {"text": "你好，你怎么样？", "expected_lang": "zh", "description": "Chino"},
        {"text": "你是谁？", "expected_lang": "zh", "description": "Chino"},

        # Japonés
        {"text": "こんにちは、お元気ですか？", "expected_lang": "ja", "description": "Japonés"},
        {"text": "あなたは誰ですか？", "expected_lang": "ja", "description": "Japonés"},

        # Coreano
        {"text": "안녕하세요, 어떻게 지내세요?", "expected_lang": "ko", "description": "Coreano"},
        {"text": "누구세요?", "expected_lang": "ko", "description": "Coreano"},

        # Ruso
        {"text": "Привет, как дела?", "expected_lang": "ru", "description": "Ruso"},
        {"text": "Кто ты?", "expected_lang": "ru", "description": "Ruso"},

        # Árabe
        {"text": "مرحبا، كيف حالك؟", "expected_lang": "ar", "description": "Árabe"},
        {"text": "من أنت؟", "expected_lang": "ar", "description": "Árabe"},

        # Hindi
        {"text": "नमस्ते, आप कैसे हैं?", "expected_lang": "hi", "description": "Hindi"},
        {"text": "तुम कौन हो?", "expected_lang": "hi", "description": "Hindi"},

        # Holandés
        {"text": "Hallo, hoe gaat het met je?", "expected_lang": "nl", "description": "Holandés"},
        {"text": "Wie ben je?", "expected_lang": "nl", "description": "Holandés"}
    ]

    correct_detections = 0
    total_tests = len(test_cases)

    print(f"\n🔍 Probando {total_tests} casos de detección de idioma:")
    print("-" * 50)

    for i, test in enumerate(test_cases, 1):
        try:
            # Test de detección de idioma
            detect_response = requests.post(
                "http://localhost:5000/api/detect-language",
                json={"text": test["text"]},
                timeout=5
            )

            if detect_response.status_code == 200:
                detect_data = detect_response.json()
                detected_lang = detect_data.get('detected_language', 'unknown')

                status = "✅" if detected_lang == test["expected_lang"] else "❌"
                if detected_lang == test["expected_lang"]:
                    correct_detections += 1

                print(f"Test {i:2d}: {test['description'][:8]} - {status} Detectado: {detected_lang} (esperado: {test['expected_lang']})")
            else:
                print(f"Test {i:2d}: {test['description'][:8]} - ❌ Error HTTP: {detect_response.status_code}")
        except Exception as e:
            print(f"Test {i:2d}: {test['description'][:8]} - ❌ Error: {str(e)[:50]}")
    # Estadísticas de detección
    detection_accuracy = (correct_detections / total_tests) * 100
    print("\n📊 ESTADÍSTICAS DE DETECCIÓN:")    print(f"   Total de tests: {total_tests}")
    print(f"   Detecciones correctas: {correct_detections}")
    print(f"   Precisión: {detection_accuracy:.1f}%")

    # Test de respuestas humanas en diferentes idiomas
    print("\n🧠 PRUEBA DE RESPUESTAS HUMANAS EN DIFERENTES IDIOMAS:")
    print("-" * 55)

    response_tests = [
        {"text": "Hola", "lang": "es", "expected_contains": ["Hola", "😊"]},
        {"text": "Hello", "lang": "en", "expected_contains": ["Hello", "😊"]},
        {"text": "Olá", "lang": "pt", "expected_contains": ["Olá", "prazer"]},
        {"text": "Bonjour", "lang": "fr", "expected_contains": ["Bonjour", "vous aider"]},
        {"text": "你好", "lang": "zh", "expected_contains": ["你好", "帮助"]},
        {"text": "こんにちは", "lang": "ja", "expected_contains": ["こんにちは", "お手伝い"]},
        {"text": "안녕하세요", "lang": "ko", "expected_contains": ["안녕하세요", "도와드릴까요"]},
        {"text": "Привет", "lang": "ru", "expected_contains": ["Привет", "помочь"]},
        {"text": "مرحبا", "lang": "ar", "expected_contains": ["مرحبا", "مساعدتك"]},
        {"text": "नमस्ते", "lang": "hi", "expected_contains": ["नमस्ते", "मदद"]},
        {"text": "Hallo", "lang": "nl", "expected_contains": ["Hallo", "helpen"]}
    ]

    successful_responses = 0

    for i, test in enumerate(response_tests, 1):
        try:
            response = requests.post(
                "http://localhost:5000/api/vigoleonrocks",
                json={"text": test["text"]},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')

                # Verificar que contiene elementos esperados
                contains_expected = any(word in response_text for word in test["expected_contains"])

                if contains_expected:
                    print(f"Test {i:2d}: {test['lang'].upper()} - ✅ Respuesta correcta")
                    successful_responses += 1
                else:
                    print(f"Test {i:2d}: {test['lang'].upper()} - ❌ Respuesta inesperada: {response_text[:50]}...")
            else:
                print(f"Test {i:2d}: {test['lang'].upper()} - ❌ Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"Test {i:2d}: {test['lang'].upper()} - ❌ Error: {str(e)[:50]}")
    # Estadísticas finales
    response_accuracy = (successful_responses / len(response_tests)) * 100

    print("\n🎯 RESULTADOS FINALES:")
    print(f"   Precisión de detección: {detection_accuracy:.1f}%")
    print(f"   Éxito de respuestas: {response_accuracy:.1f}%")
    print(f"   Idiomas soportados: 12")
    print(f"   Tests totales: {total_tests + len(response_tests)}")

    if detection_accuracy >= 80 and response_accuracy >= 70:
        print("\n🎉 ¡SISTEMA MULTILINGÜE OPERATIVO! 🌍")
    else:
        print("\n⚠️  SISTEMA REQUIERE AJUSTES")
    print("=" * 60)

if __name__ == "__main__":
    test_multilenguaje_global()
