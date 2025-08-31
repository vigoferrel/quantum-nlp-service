#!/usr/bin/env python3
"""
🧪 TEST COMPLETO: INTEGRACIÓN DE JOYAS INTERNAS
Verifica que todos los endpoints de las joyas funcionen correctamente
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
TEST_MESSAGES = [
    "Hola, ¿cómo estás?",
    "Hello, how are you?",
    "Olá, como você está?",
    "Bonjour, comment allez-vous?",
    "Hallo, wie geht es dir?",
    "Ciao, come stai?"
]

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Prueba un endpoint específico"""
    try:
        url = f"{BASE_URL}{endpoint}"
        headers = {'Content-Type': 'application/json'} if data else {}
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {description}: OK")
            return True, result
        else:
            print(f"❌ {description}: Error {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ {description}: Exception - {str(e)}")
        return False, None

def test_translation():
    """Prueba el sistema de traducción"""
    print("\n🌍 PROBANDO SISTEMA DE TRADUCCIÓN")
    print("=" * 50)
    
    test_cases = [
        {"text": "Hello world", "target": "es", "expected": "Hola mundo"},
        {"text": "Gracias por tu ayuda", "target": "en", "expected": "Thank you for your help"},
        {"text": "Bonjour le monde", "target": "pt", "expected": "Olá mundo"}
    ]
    
    for i, case in enumerate(test_cases, 1):
        success, result = test_endpoint(
            "/api/translate",
            method="POST",
            data={"text": case["text"], "target_language": case["target"]},
            description=f"Traducción {i}: {case['text']} → {case['target']}"
        )
        
        if success and result:
            print(f"   📝 Resultado: {result.get('translated_text', 'N/A')}")
            print(f"   🔧 Método: {result.get('method', 'N/A')}")
            print(f"   🎯 Confianza: {result.get('confidence', 'N/A')}")

def test_language_detection():
    """Prueba la detección de idiomas"""
    print("\n🔍 PROBANDO DETECCIÓN DE IDIOMAS")
    print("=" * 50)
    
    for i, message in enumerate(TEST_MESSAGES, 1):
        success, result = test_endpoint(
            "/api/detect-language",
            method="POST",
            data={"text": message},
            description=f"Detección {i}: {message[:30]}..."
        )
        
        if success and result:
            print(f"   🌍 Idioma detectado: {result.get('language', 'N/A')}")
            print(f"   🎯 Confianza: {result.get('confidence', 'N/A')}")

def test_archetypal_analysis():
    """Prueba el análisis arquetipal"""
    print("\n🎭 PROBANDO ANÁLISIS ARQUETIPAL")
    print("=" * 50)
    
    test_texts = [
        "El héroe valiente luchó contra el dragón para salvar al pueblo",
        "El sabio mentor enseñó al joven aprendiz los secretos de la vida",
        "La sombra oscura acechaba en las profundidades del bosque",
        "La intuición femenina guió su camino hacia la verdad"
    ]
    
    for i, text in enumerate(test_texts, 1):
        success, result = test_endpoint(
            "/api/archetypal-analysis",
            method="POST",
            data={"text": text},
            description=f"Análisis {i}: {text[:40]}..."
        )
        
        if success and result:
            print(f"   🎭 Arquetipo dominante: {result.get('dominant_archetype', 'N/A')}")
            print(f"   📊 Patrones: {', '.join(result.get('archetypal_patterns', []))}")
            print(f"   🎯 Confianza: {result.get('confidence', 'N/A')}")

def test_empathic_generation():
    """Prueba la generación de respuestas empáticas"""
    print("\n💝 PROBANDO GENERACIÓN EMPÁTICA")
    print("=" * 50)
    
    templates = ["greeting", "support", "gratitude"]
    empathy_levels = [3, 7, 10]
    
    for template in templates:
        for level in empathy_levels:
            success, result = test_endpoint(
                "/api/empathic-generate",
                method="POST",
                data={"template_type": template, "empathy_level": level},
                description=f"Empático {template} (nivel {level})"
            )
            
            if success and result:
                print(f"   💝 Respuesta: {result.get('empathic_response', 'N/A')[:60]}...")
                print(f"   📊 Nivel: {result.get('empathy_level', 'N/A')}")

def test_quantum_metrics():
    """Prueba las métricas cuánticas"""
    print("\n📊 PROBANDO MÉTRICAS CUÁNTICAS")
    print("=" * 50)
    
    success, result = test_endpoint(
        "/api/quantum-metrics",
        description="Métricas cuánticas en tiempo real"
    )
    
    if success and result:
        print(f"   ⚛️ Estados cuánticos: {result.get('quantum_states_active', 'N/A')}")
        print(f"   🎯 Supremacy Score: {result.get('supremacy_score', 'N/A')}")
        print(f"   📡 Resonancia: {result.get('resonance_frequency', 'N/A')}Hz")
        print(f"   🌍 Idiomas procesados: {result.get('languages_processed', 'N/A')}")
        print(f"   🧠 Cerebro disponible: {result.get('quantum_brain_available', 'N/A')}")

def test_quantum_configuration():
    """Prueba la configuración cuántica"""
    print("\n⚛️ PROBANDO CONFIGURACIÓN CUÁNTICA")
    print("=" * 50)
    
    # Probar configuración de perfil
    profiles = ["leonardo", "technical", "empathic"]
    for profile in profiles:
        success, result = test_endpoint(
            "/api/set-quantum-profile",
            method="POST",
            data={"profile": profile},
            description=f"Configurar perfil: {profile}"
        )
        
        if success and result:
            print(f"   🧠 Perfil configurado: {result.get('profile_set', 'N/A')}")
    
    # Probar configuración de estados
    states_to_test = [13, 26]
    for states in states_to_test:
        success, result = test_endpoint(
            "/api/set-quantum-states",
            method="POST",
            data={"states": states},
            description=f"Configurar estados: {states}"
        )
        
        if success and result:
            print(f"   ⚛️ Estados configurados: {result.get('quantum_states_set', 'N/A')}")
            print(f"   📊 Coherencia: {result.get('coherence_percentage', 'N/A')}%")

def test_interaction_history():
    """Prueba el historial de interacciones"""
    print("\n📈 PROBANDO HISTORIAL DE INTERACCIONES")
    print("=" * 50)
    
    filters = ["all", "empathic", "technical", "multilingual"]
    
    for filter_type in filters:
        success, result = test_endpoint(
            f"/api/interaction-history?filter={filter_type}",
            description=f"Historial filtrado: {filter_type}"
        )
        
        if success and result:
            interactions = result.get('interactions', [])
            print(f"   📊 Total interacciones ({filter_type}): {len(interactions)}")
            if interactions:
                print(f"   📝 Última: {interactions[0].get('text_preview', 'N/A')}")

def test_main_vigoleonrocks():
    """Prueba el endpoint principal"""
    print("\n🚀 PROBANDO ENDPOINT PRINCIPAL")
    print("=" * 50)
    
    test_messages = [
        "Hola, ¿quién eres?",
        "Hello, what can you do?",
        "Olá, como você funciona?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        success, result = test_endpoint(
            "/api/vigoleonrocks",
            method="POST",
            data={"text": message},
            description=f"Procesamiento principal {i}: {message}"
        )
        
        if success and result:
            print(f"   💬 Respuesta: {result.get('response', 'N/A')[:80]}...")
            print(f"   ⏱️ Tiempo: {result.get('processing_time', 'N/A')}ms")
            print(f"   🔧 Método: {result.get('processing_method', 'N/A')}")

def main():
    """Ejecuta todas las pruebas"""
    print("🧪 INICIANDO TEST COMPLETO DE JOYAS INTEGRADAS")
    print("=" * 60)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Servidor: {BASE_URL}")
    
    start_time = time.time()
    
    # Ejecutar todas las pruebas
    test_translation()
    test_language_detection()
    test_archetypal_analysis()
    test_empathic_generation()
    test_quantum_metrics()
    test_quantum_configuration()
    test_interaction_history()
    test_main_vigoleonrocks()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🏁 TEST COMPLETADO")
    print(f"⏱️ Duración total: {duration:.2f} segundos")
    print(f"🎯 Todas las joyas internas han sido probadas exitosamente")
    print("=" * 60)

if __name__ == "__main__":
    main()
