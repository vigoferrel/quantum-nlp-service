#!/usr/bin/env python3
"""
Script de prueba para diagnosticar el sistema avanzado
"""

import requests
import json
import time

def test_advanced_system():
    """Probar el sistema avanzado directamente"""
    print("🧪 Probando sistema avanzado...")
    
    url = "http://localhost:5004/api/process_text"
    
    # Test simple
    data = {
        "text": "Hola, ¿cómo estás?",
        "session_id": "test_001",
        "user_id": "test_user"
    }
    
    try:
        print(f"📤 Enviando request a {url}")
        print(f"📝 Data: {json.dumps(data, indent=2)}")
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=30)
        response_time = time.time() - start_time
        
        print(f"⏱️ Tiempo de respuesta: {response_time:.3f}s")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Respuesta exitosa:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            # Analizar la respuesta
            if response_data.get("success"):
                print("✅ Campo 'success' presente")
            else:
                print("❌ Campo 'success' ausente")
                
            if response_data.get("nlp_analysis"):
                print("✅ Campo 'nlp_analysis' presente")
                nlp = response_data["nlp_analysis"]
                if nlp.get("sentiment"):
                    print(f"✅ Sentiment: {nlp['sentiment']}")
                if nlp.get("intent"):
                    print(f"✅ Intent: {nlp['intent']}")
            else:
                print("❌ Campo 'nlp_analysis' ausente")
                
            if response_data.get("quantum_analysis"):
                print("✅ Campo 'quantum_analysis' presente")
            else:
                print("❌ Campo 'quantum_analysis' ausente")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_advanced_system()
