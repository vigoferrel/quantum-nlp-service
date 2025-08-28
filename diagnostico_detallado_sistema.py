#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO DETALLADO DEL SISTEMA
====================================
Script para identificar exactamente dónde falla el procesamiento
"""

import asyncio
import time
import traceback
from typing import Dict, Any
import requests
import json

# Importar componentes del sistema
try:
    from advanced_conversational_engine import AdvancedConversationalEngine
    from advanced_nlp_engine import nlp_engine
    from quantum_core_26d_engine import QuantumCore26DEngine
    from advanced_multimodal_server import MediaContent, MediaType, ConversationRequest
    print("✅ Imports exitosos")
except Exception as e:
    print(f"❌ Error en imports: {e}")
    exit(1)

async def test_nlp_engine():
    """Probar el motor NLP directamente"""
    print("\n🧠 TESTING NLP ENGINE")
    print("=" * 50)
    
    test_texts = [
        "Hola, ¿cómo estás?",
        "Estoy muy feliz hoy!",
        "Necesito ayuda con programación",
        "¿Puedes explicarme cómo funciona la computación cuántica?"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        try:
            # Test 1: Análisis básico
            print("  🔍 Análisis básico...")
            nlp_features = await nlp_engine.analyze_text(text)
            print(f"    ✅ NLP Features obtenidas: {type(nlp_features)}")
            print(f"    📊 Sentiment: {nlp_features.sentiment.level}")
            print(f"    🎯 Intent: {nlp_features.intent.intent}")
            
            # Test 2: Detección de idioma
            print("  🌍 Detección de idioma...")
            language = await nlp_engine.detect_language(text)
            print(f"    ✅ Idioma detectado: {language}")
            
            # Test 3: Extracción de resumen
            print("  📋 Extracción de resumen...")
            summary = await nlp_engine.extract_summary(text)
            print(f"    ✅ Resumen: {summary}")
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            print(f"    📄 Traceback: {traceback.format_exc()}")

async def test_quantum_core():
    """Probar el núcleo cuántico directamente"""
    print("\n⚛️ TESTING QUANTUM CORE")
    print("=" * 50)
    
    quantum_core = QuantumCore26DEngine()
    test_texts = [
        "Explica la teoría de la relatividad",
        "¿Cómo funciona la computación cuántica?",
        "Necesito resolver un problema complejo",
        "Analiza este código de programación"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        try:
            print("  ⚛️ Procesamiento cuántico...")
            quantum_result = await quantum_core.test_quantum_enhancement(text, "general")
            print(f"    ✅ Quantum result obtenido: {type(quantum_result)}")
            print(f"    📊 Quantum Score: {quantum_result.quantum_score}")
            print(f"    🌌 Quantum State: {quantum_result.quantum_state_achieved}")
            print(f"    📈 Improvement Factor: {quantum_result.improvement_factor}")
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            print(f"    📄 Traceback: {traceback.format_exc()}")

async def test_conversational_engine():
    """Probar el motor conversacional completo"""
    print("\n🤖 TESTING CONVERSATIONAL ENGINE")
    print("=" * 50)
    
    engine = AdvancedConversationalEngine()
    test_texts = [
        "Hola, ¿cómo estás?",
        "Estoy muy feliz hoy!",
        "Necesito ayuda con programación"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        try:
            # Crear contenido multimedia
            content = MediaContent(
                media_type=MediaType.TEXT,
                content=text,
                mime_type="text/plain"
            )
            
            # Crear request
            request = ConversationRequest(
                content=content,
                session_id=f"test_session_{i}",
                user_id="test_user"
            )
            
            print("  🔄 Procesando conversación...")
            response = await engine.process_conversation(request)
            
            print(f"    ✅ Success: {response.success}")
            print(f"    ⏱️ Processing time: {response.processing_time:.3f}s")
            
            if response.success and response.response:
                print(f"    📝 Response content: {type(response.response.content)}")
                
                # Verificar NLP features
                if hasattr(response.response.content, 'nlp_features'):
                    print(f"    🧠 NLP Features: {response.response.content.nlp_features is not None}")
                else:
                    print(f"    ❌ No NLP features en response")
                
                # Verificar Quantum features
                if hasattr(response.response.content, 'quantum_features'):
                    print(f"    ⚛️ Quantum Features: {response.response.content.quantum_features is not None}")
                else:
                    print(f"    ❌ No Quantum features en response")
            else:
                print(f"    ❌ Error: {response.error}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
            print(f"    📄 Traceback: {traceback.format_exc()}")

async def test_server_endpoint():
    """Probar el endpoint del servidor"""
    print("\n🌐 TESTING SERVER ENDPOINT")
    print("=" * 50)
    
    test_data = {
        "text": "Hola, ¿cómo estás?",
        "session_id": "diagnostic_test",
        "user_id": "test_user"
    }
    
    try:
        print("  📡 Enviando request...")
        response = requests.post(
            "http://localhost:5004/api/process_text",
            json=test_data,
            timeout=30
        )
        
        print(f"    ✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"    📊 Success: {data.get('success')}")
            print(f"    ⏱️ Processing Time: {data.get('processing_time', 0):.3f}s")
            print(f"    🧠 NLP Analysis: {data.get('nlp_analysis') is not None}")
            print(f"    ⚛️ Quantum Analysis: {data.get('quantum_analysis') is not None}")
            
            if data.get('nlp_analysis'):
                print(f"    📝 NLP Details: {json.dumps(data['nlp_analysis'], indent=2)}")
            else:
                print(f"    ❌ No NLP analysis disponible")
                
            if data.get('quantum_analysis'):
                print(f"    📝 Quantum Details: {json.dumps(data['quantum_analysis'], indent=2)}")
            else:
                print(f"    ❌ No Quantum analysis disponible")
        else:
            print(f"    ❌ Error response: {response.text}")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
        print(f"    📄 Traceback: {traceback.format_exc()}")

async def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DETALLADO DEL SISTEMA")
    print("=" * 60)
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: NLP Engine
    await test_nlp_engine()
    
    # Test 2: Quantum Core
    await test_quantum_core()
    
    # Test 3: Conversational Engine
    await test_conversational_engine()
    
    # Test 4: Server Endpoint
    await test_server_endpoint()
    
    print("\n" + "=" * 60)
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print("📄 Revisa los resultados arriba para identificar problemas")

if __name__ == "__main__":
    asyncio.run(main())
