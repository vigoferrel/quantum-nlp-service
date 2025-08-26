#!/usr/bin/env python3
"""
VIGOLEONROCKS OLLAMA - EJECUTOR DE PRUEBAS RÁPIDO
Script simplificado para ejecutar pruebas básicas
"""

import requests
import json
import time
import sys
from datetime import datetime

def check_ollama():
    """Verificar Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_vigoleonrocks():
    """Prueba rápida de VIGOLEONROCKS"""
    if not check_ollama():
        print("❌ Ollama no está ejecutándose")
        print("Ejecuta: ollama serve")
        return False
    
    print("🚀 Iniciando pruebas VIGOLEONROCKS...")
    
    # Prueba básica
    payload = {
        "model": "vigoleonrocks",
        "prompt": "Hola VIGOLEONROCKS, demuestra tus capacidades cuántico-cognitivas en una respuesta breve.",
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.1
        }
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            print(f"✅ Prueba exitosa!")
            print(f"⏱️  Tiempo: {end_time - start_time:.2f}s")
            print(f"📝 Tokens: {len(response_text.split())}")
            print(f"🧠 Respuesta: {response_text[:300]}...")
            
            # Guardar resultado
            test_result = {
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'response_time': end_time - start_time,
                'tokens_generated': len(response_text.split()),
                'response': response_text
            }
            
            with open('quick-test-result.json', 'w', encoding='utf-8') as f:
                json.dump(test_result, f, indent=2, ensure_ascii=False)
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_vigoleonrocks()
    sys.exit(0 if success else 1)