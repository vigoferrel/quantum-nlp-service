#!/usr/bin/env python3
import requests
import json

def debug_empathic():
    print("🔍 DEBUGGING RESPUESTAS EMPÁTICAS")
    print("=" * 50)
    
    # Probar diferentes niveles
    tests = [
        {"template": "greeting", "level": 1},
        {"template": "greeting", "level": 5},
        {"template": "greeting", "level": 10},
        {"template": "support", "level": 1},
        {"template": "support", "level": 5},
        {"template": "support", "level": 10},
        {"template": "gratitude", "level": 1},
        {"template": "gratitude", "level": 5},
        {"template": "gratitude", "level": 10}
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
                print(f"🔧 Método: {data.get('method', 'N/A')}")
                print("-" * 50)
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_empathic()
