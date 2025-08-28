#!/usr/bin/env python3
"""
Script de prueba simple para diagnosticar el sistema avanzado
"""

import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_advanced_engine():
    """Probar el motor conversacional avanzado directamente"""
    print("🧪 Probando motor conversacional avanzado directamente...")
    
    try:
        from advanced_conversational_engine import (
            AdvancedConversationalEngine,
            ConversationRequest,
            MediaContent,
            MediaType
        )
        
        # Crear instancia del motor
        print("📦 Creando instancia del motor...")
        engine = AdvancedConversationalEngine()
        print("✅ Motor creado correctamente")
        
        # Crear contenido de texto
        print("📝 Creando contenido de texto...")
        content = MediaContent(
            media_type=MediaType.TEXT,
            content="Hola, ¿cómo estás?",
            mime_type="text/plain"
        )
        print("✅ Contenido creado correctamente")
        
        # Crear request
        print("📤 Creando request...")
        request = ConversationRequest(
            content=content,
            session_id="test_session_001",
            user_id="test_user"
        )
        print("✅ Request creado correctamente")
        
        # Procesar conversación
        print("🔄 Procesando conversación...")
        response = await engine.process_conversation(request)
        print(f"✅ Respuesta recibida: {response.success}")
        
        if response.success:
            print(f"📝 Respuesta: {response.response.content.content}")
            print(f"⏱️ Tiempo: {response.processing_time:.3f}s")
            
            # Verificar NLP features
            if response.response.content.nlp_features:
                print("🧠 NLP features disponibles")
                print(f"   Sentiment: {response.response.content.nlp_features.sentiment.level.value}")
                print(f"   Intent: {response.response.content.nlp_features.intent.intent.value}")
            else:
                print("❌ NLP features no disponibles")
            
            # Verificar quantum features
            if response.response.content.quantum_features:
                print("⚛️ Quantum features disponibles")
                print(f"   Quantum score: {response.response.content.quantum_features.quantum_score}")
            else:
                print("❌ Quantum features no disponibles")
        else:
            print(f"❌ Error: {response.error}")
            
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_advanced_engine())
