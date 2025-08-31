#!/usr/bin/env python3
import requests
import json

def test_mejoras():
    print("🚀 PROBANDO MEJORAS DEL SISTEMA")
    print("=" * 50)
    
    # Probar traducciones mejoradas
    print("\n🌍 PROBANDO TRADUCCIONES MEJORADAS:")
    print("-" * 30)
    
    translation_tests = [
        {"text": "Hello, how are you?", "target": "es"},
        {"text": "Who are you?", "target": "pt"},
        {"text": "What can you do?", "target": "es"},
        {"text": "Thank you very much", "target": "pt"},
        {"text": "Hola, ¿cómo estás?", "target": "en"},
        {"text": "Quem é você?", "target": "en"}
    ]
    
    for test in translation_tests:
        try:
            response = requests.post(
                "http://localhost:5000/api/translate",
                json=test,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"📝 '{test['text']}' → '{data['translated_text']}' ({test['target']})")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Probar análisis arquetipal mejorado
    print("\n🎭 PROBANDO ANÁLISIS ARQUETIPAL MEJORADO:")
    print("-" * 40)
    
    archetypal_tests = [
        "El guerrero valiente protegió al pueblo",
        "El sabio consejero guió al joven aprendiz",
        "La sombra oscura acechaba en las profundidades",
        "La intuición misteriosa reveló la verdad",
        "El tramposo astuto engañó a todos"
    ]
    
    for text in archetypal_tests:
        try:
            response = requests.post(
                "http://localhost:5000/api/archetypal-analysis",
                json={"text": text},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"📝 '{text[:30]}...' → {data['dominant_archetype']} (conf: {data['confidence']})")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Probar respuestas empáticas mejoradas
    print("\n💝 PROBANDO RESPUESTAS EMPÁTICAS MEJORADAS:")
    print("-" * 40)
    
    empathic_tests = [
        {"template": "greeting", "level": 1},
        {"template": "greeting", "level": 5},
        {"template": "greeting", "level": 10},
        {"template": "support", "level": 1},
        {"template": "support", "level": 5},
        {"template": "support", "level": 10}
    ]
    
    for test in empathic_tests:
        try:
            response = requests.post(
                "http://localhost:5000/api/empathic-generate",
                json=test,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"📝 {test['template']} (nivel {test['level']}): {data['response'][:50]}...")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_mejoras()
