#!/usr/bin/env python3
import requests
import json

def test_response(text):
    try:
        response = requests.post(
            "http://localhost:5000/api/vigoleonrocks",
            json={"text": text},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"📝 Input: '{text}'")
            print(f"💬 Output: '{data['response']}'")
            print(f"🌍 Language: {data['language']}")
            print(f"⏱️ Time: {data['processing_time']}ms")
            print("-" * 50)
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🧪 PROBANDO RESPUESTAS HUMANAS")
    print("=" * 50)
    
    test_cases = [
        "Hola",
        "¿Cómo estás?",
        "¿Quién eres?",
        "Gracias",
        "Hello, how are you?",
        "Who are you?",
        "Thank you",
        "Olá, como vai?",
        "Quem é você?",
        "Obrigado"
    ]
    
    for text in test_cases:
        test_response(text)
        import time
        time.sleep(0.5)
