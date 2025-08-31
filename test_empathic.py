#!/usr/bin/env python3
import requests
import json

def test_empathic():
    print("💝 PROBANDO RESPUESTAS EMPÁTICAS")
    print("=" * 50)
    
    tests = [
        {"template": "greeting", "level": 3},
        {"template": "greeting", "level": 7},
        {"template": "greeting", "level": 10},
        {"template": "support", "level": 5},
        {"template": "support", "level": 8},
        {"template": "gratitude", "level": 6},
        {"template": "gratitude", "level": 9}
    ]
    
    for test in tests:
        try:
            response = requests.post(
                "http://localhost:5000/api/empathic-generate",
                json=test,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"📝 Template: {test['template']}, Nivel: {test['level']}")
                print(f"💬 Respuesta: {data['response']}")
                print("-" * 50)
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_empathic()
