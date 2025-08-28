#!/usr/bin/env python3
"""
🔧 CORRECCIÓN ESPECÍFICA DE SERIALIZACIÓN HTTP
Corregir el problema de NLP Score y Quantum Score = 0.00
"""

import os
import re

def corregir_serializacion_especifica():
    """Corregir serialización HTTP específicamente"""
    print("🔧 CORRECCIÓN ESPECÍFICA DE SERIALIZACIÓN HTTP")
    print("=" * 50)
    
    archivo = "advanced_multimodal_server.py"
    if not os.path.exists(archivo):
        print(f"❌ No se encontró {archivo}")
        return False
    
    # Leer archivo
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print("📖 Analizando archivo...")
    
    # Buscar el endpoint /api/process_text
    if '/api/process_text' not in contenido:
        print("❌ No se encontró el endpoint /api/process_text")
        return False
    
    # Buscar patrones de respuesta problemáticos
    patrones_problematicos = [
        'nlp_analysis.*None',
        'quantum_analysis.*None',
        'response.response.content.nlp_features',
        'getattr(response.response'
    ]
    
    for patron in patrones_problematicos:
        if patron in contenido:
            print(f"⚠️ Encontrado patrón problemático: {patron}")
    
    # Buscar la función específica del endpoint
    lines = contenido.split('\n')
    start_line = -1
    end_line = -1
    
    for i, line in enumerate(lines):
        if '@app.post("/api/process_text")' in line:
            start_line = i
            print(f"📍 Encontrado endpoint en línea {i+1}")
        elif start_line != -1 and 'return {' in line:
            # Buscar el final del return
            for j in range(i, len(lines)):
                if lines[j].strip() == '}':
                    end_line = j
                    break
            break
    
    if start_line == -1:
        print("❌ No se pudo encontrar el endpoint")
        return False
    
    print(f"🔍 Analizando líneas {start_line+1} a {end_line+1}")
    
    # Extraer la función actual
    funcion_actual = '\n'.join(lines[start_line:end_line+1])
    print("📝 Función actual encontrada:")
    print(funcion_actual[:500] + "..." if len(funcion_actual) > 500 else funcion_actual)
    
    # Crear nueva función corregida
    nueva_funcion = '''@app.post("/api/process_text")
async def process_text(request: TextRequest):
    """Procesar texto con análisis NLP y cuántico"""
    start_time = time.time()
    
    try:
        # Crear contenido multimedia
        content = MediaContent(
            media_type=MediaType.TEXT,
            content=request.text,
            mime_type="text/plain"
        )
        
        # Crear request de conversación
        conversation_request = ConversationRequest(
            content=content,
            session_id=request.session_id,
            user_id=request.user_id
        )
        
        # Procesar conversación
        response = await conversational_engine.process_conversation(conversation_request)
        
        processing_time = time.time() - start_time
        
        # Extraer análisis NLP y cuántico correctamente
        nlp_analysis = None
        quantum_analysis = None
        
        if response.success and response.response:
            # Obtener el contenido procesado
            processed_content = response.response.content
            
            # Extraer NLP features
            if hasattr(processed_content, 'nlp_features') and processed_content.nlp_features:
                nlp_analysis = {
                    "sentiment": {
                        "level": str(processed_content.nlp_features.sentiment.level),
                        "compound": processed_content.nlp_features.sentiment.compound,
                        "confidence": processed_content.nlp_features.sentiment.confidence,
                        "subjectivity": processed_content.nlp_features.sentiment.subjectivity
                    },
                    "intent": {
                        "type": str(processed_content.nlp_features.intent.intent),
                        "confidence": processed_content.nlp_features.intent.confidence,
                        "keywords": processed_content.nlp_features.intent.keywords,
                        "context": processed_content.nlp_features.intent.context
                    },
                    "entities": [
                        {
                            "text": entity.text,
                            "type": str(entity.type),
                            "confidence": entity.confidence,
                            "description": entity.description
                        }
                        for entity in processed_content.nlp_features.intent.entities
                    ]
                }
            
            # Extraer quantum features
            if hasattr(processed_content, 'quantum_features') and processed_content.quantum_features:
                quantum_analysis = {
                    "quantum_score": processed_content.quantum_features.quantum_score,
                    "quantum_state": str(processed_content.quantum_features.quantum_state_achieved),
                    "improvement_factor": processed_content.quantum_features.improvement_factor,
                    "dimension_scores": processed_content.quantum_features.dimension_scores
                }
        
        return {
            "success": response.success,
            "response": response.response.content.content if response.success else None,
            "processing_time": processing_time,
            "session_id": request.session_id,
            "nlp_analysis": nlp_analysis,
            "quantum_analysis": quantum_analysis,
            "context_26d": [dim.__dict__ for dim in response.context_26d_updated] if response.success else None
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        return {
            "success": False,
            "error": str(e),
            "processing_time": processing_time,
            "session_id": request.session_id,
            "nlp_analysis": None,
            "quantum_analysis": None,
            "context_26d": []
        }'''
    
    # Reemplazar la función
    nuevo_contenido = contenido.replace(funcion_actual, nueva_funcion)
    
    # Guardar archivo corregido
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
    
    print("✅ Serialización HTTP corregida específicamente")
    print("📝 Cambios aplicados:")
    print("   - Extracción correcta de nlp_features")
    print("   - Extracción correcta de quantum_features")
    print("   - Manejo de errores mejorado")
    print("   - Serialización JSON optimizada")
    
    return True

def verificar_correccion():
    """Verificar que la corrección se aplicó correctamente"""
    print("\n🔍 VERIFICANDO CORRECCIÓN")
    print("-" * 30)
    
    archivo = "advanced_multimodal_server.py"
    if not os.path.exists(archivo):
        print("❌ Archivo no encontrado")
        return False
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar que los cambios se aplicaron
    verificaciones = [
        ("nlp_analysis = None", "✅ Variable nlp_analysis definida"),
        ("quantum_analysis = None", "✅ Variable quantum_analysis definida"),
        ("hasattr(processed_content, 'nlp_features')", "✅ Verificación de nlp_features"),
        ("hasattr(processed_content, 'quantum_features')", "✅ Verificación de quantum_features"),
        ("str(processed_content.nlp_features.sentiment.level)", "✅ Serialización de sentimiento"),
        ("str(processed_content.nlp_features.intent.intent)", "✅ Serialización de intención"),
        ("processed_content.quantum_features.quantum_score", "✅ Extracción de quantum_score")
    ]
    
    todas_correctas = True
    for verificacion, mensaje in verificaciones:
        if verificacion in contenido:
            print(f"   {mensaje}")
        else:
            print(f"   ❌ {mensaje} - NO ENCONTRADO")
            todas_correctas = False
    
    return todas_correctas

def main():
    """Función principal"""
    print("🚀 CORRECCIÓN ESPECÍFICA DE SERIALIZACIÓN HTTP")
    print("=" * 60)
    
    # Ejecutar corrección
    if corregir_serializacion_especifica():
        print("\n✅ CORRECCIÓN APLICADA")
        
        # Verificar corrección
        if verificar_correccion():
            print("\n🎉 CORRECCIÓN VERIFICADA EXITOSAMENTE")
            print("\n🎯 PRÓXIMOS PASOS:")
            print("   1. Reiniciar servidor avanzado")
            print("   2. Probar endpoint /api/process_text")
            print("   3. Verificar que NLP Score > 0")
            print("   4. Verificar que Quantum Score > 0")
        else:
            print("\n⚠️ CORRECCIÓN APLICADA PERO VERIFICACIÓN FALLÓ")
    else:
        print("\n❌ CORRECCIÓN FALLÓ")

if __name__ == "__main__":
    main()
