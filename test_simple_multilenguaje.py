#!/usr/bin/env python3
import requests
import json

def test_simple_multilenguaje():
    """Prueba simple del sistema multilingüe con algunos idiomas clave"""
    print("🌍 PRUEBA SIMPLE DEL SISTEMA MULTILINGÜE")
    print("=" * 50)

    # Test cases simples
    test_cases = [
        {"text": "Hola, ¿cómo estás?", "expected_lang": "es", "description": "Español"},
        {"text": "Hello, how are you?", "expected_lang": "en", "description": "Inglés"},
        {"text": "Olá, como vai?", "expected_lang": "pt", "description": "Portugués"},
        {"text": "Bonjour, comment allez-vous?", "expected_lang": "fr", "description": "Francés"},
        {"text": "你好，你怎么样？", "expected_lang": "zh", "description": "Chino"},
        {"text": "こんにちは、お元気ですか？", "expected_lang": "ja", "description": "Japonés"},
        {"text": "안녕하세요, 어떻게 지내세요?", "expected_lang": "ko", "description": "Coreano"},
        {"text": "Привет, как дела?", "expected_lang": "ru", "description": "Ruso"}
    ]

    correct_detections = 0
    total_tests = len(test_cases)

    print(f"\n🔍 Probando {total_tests} casos de detección de idioma:")
    print("-" * 50)

    for i, test in enumerate(test_cases, 1):
        try:
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
    print("\n📊 ESTADÍSTICAS DE DETECCIÓN:")
    print(f"   Total de tests: {total_tests}")
    print(f"   Detecciones correctas: {correct_detections}")
    print(f"   Precisión de detección: {detection_accuracy:.1f}%")
    # Test de respuestas humanas
    print("\n🧠 PRUEBA DE RESPUESTAS HUMANAS:")
    print("-" * 35)

    response_tests = [
        {"text": "Hola", "lang": "es"},
        {"text": "Hello", "lang": "en"},
        {"text": "Olá", "lang": "pt"},
        {"text": "Bonjour", "lang": "fr"}
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

                if response_text and len(response_text) > 5:
                    print(f"Test {i:2d}: {test['lang'].upper()} - ✅ Respuesta generada")
                    successful_responses += 1
                else:
                    print(f"Test {i:2d}: {test['lang'].upper()} - ❌ Respuesta vacía")
            else:
                print(f"Test {i:2d}: {test['lang'].upper()} - ❌ Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"Test {i:2d}: {test['lang'].upper()} - ❌ Error: {str(e)[:50]}")

    # Estadísticas finales
    response_accuracy = (successful_responses / len(response_tests)) * 100

    print("\n🎯 RESULTADOS FINALES:")
    print(f"   Precisión de detección: {detection_accuracy:.1f}%")
    print(f"   Éxito de respuestas: {response_accuracy:.1f}%")    print(f"   Idiomas soportados: 12")
    print(f"   Tests totales: {total_tests + len(response_tests)}")

    if detection_accuracy >= 75 and response_accuracy >= 75:
        print("\n🎉 ¡SISTEMA MULTILINGÜE OPERATIVO! 🌍")
    else:
        print("\n⚠️  SISTEMA REQUIERE AJUSTES")

    print("=" * 50)

if __name__ == "__main__":
    test_simple_multilenguaje()
