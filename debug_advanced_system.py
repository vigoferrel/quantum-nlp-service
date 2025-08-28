#!/usr/bin/env python3
"""
Script de debug para el sistema avanzado
"""

import requests
import json
import time
import traceback

def debug_advanced_system():
    """Debug del sistema avanzado"""
    print("🔍 DEBUGGING SISTEMA AVANZADO")
    print("=" * 50)
    
    # Test 1: Verificar estado del servidor
    print("\n1️⃣ Verificando estado del servidor...")
    try:
        response = requests.get("http://localhost:5004/api/status", timeout=5)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Estado: {data}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Probar endpoint de texto
    print("\n2️⃣ Probando endpoint de texto...")
    url = "http://localhost:5004/api/process_text"
    
    data = {
        "text": "Hola, ¿cómo estás?",
        "session_id": "debug_001",
        "user_id": "debug_user"
    }
    
    try:
        print(f"📤 Enviando request a {url}")
        print(f"📝 Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=60)
        response_time = time.time() - start_time
        
        print(f"⏱️ Tiempo de respuesta: {response_time:.3f}s")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Respuesta exitosa:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            # Análisis detallado
            print(f"\n📊 ANÁLISIS DETALLADO:")
            print(f"   Success: {response_data.get('success')}")
            print(f"   Response: {response_data.get('response')}")
            print(f"   Processing time: {response_data.get('processing_time')}")
            print(f"   NLP Analysis: {response_data.get('nlp_analysis')}")
            print(f"   Quantum Analysis: {response_data.get('quantum_analysis')}")
            print(f"   Context 26D: {response_data.get('context_26d')}")
            
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"📝 Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_advanced_system()
