#!/usr/bin/env python3
"""
🧪 TEST SCRIPT PARA SERVIDOR MULTIMODAL AVANZADO
Script de prueba para diagnosticar problemas
"""

import asyncio
import json
import time
from advanced_conversational_engine import (
    AdvancedConversationalEngine, 
    ConversationRequest, 
    MediaContent, 
    MediaType
)

async def test_conversational_engine():
    """Probar el motor conversacional directamente"""
    print("🧪 Probando motor conversacional directamente...")
    
    try:
        # Crear instancia del motor
        engine = AdvancedConversationalEngine()
        print("✅ Motor creado correctamente")
        
        # Crear contenido de texto
        content = MediaContent(
            media_type=MediaType.TEXT,
            content="Hola mundo",
            mime_type="text/plain"
        )
        print("✅ Contenido creado correctamente")
        
        # Crear request
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
        else:
            print(f"❌ Error: {response.error}")
            
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_conversational_engine())
