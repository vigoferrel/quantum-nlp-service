#!/usr/bin/env python3
"""
🧪 VIGOLEONROCKS - Script de Pruebas del Sistema Híbrido v4.0.0
Verifica la integración completa: UnifiedAIService + Backend Multimodal + Gateway
"""

import sys
import time
import requests
import json
from datetime import datetime

def print_test_header(test_name):
    """Imprime header de prueba"""
    print("=" * 60)
    print(f"🧪 {test_name}")
    print("=" * 60)

def print_test_result(test_name, success, details=""):
    """Imprime resultado de prueba"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")
    print()

def test_unified_service():
    """Probar UnifiedAIService directamente"""
    print_test_header("PRUEBA 1: UnifiedAIService Directo")
    
    try:
        # Importar y probar el servicio unificado
        from vigoleonrocks.services.unified_ai_service import get_unified_service
        
        service = get_unified_service()
        
        # Prueba 1: Detección de idioma
        lang = service.detect_language("Hola, ¿cómo estás?")
        print_test_result("Detección de idioma", lang == 'es', f"Detectado: {lang}")
        
        # Prueba 2: Procesamiento de consulta
        result = service.process_query("Hola, soy una prueba del sistema", 'hybrid', 26)
        
        success = (
            'response' in result and 
            'language' in result and 
            'quantum_states' in result and
            result['quantum_states'] == 26
        )
        
        print_test_result("Procesamiento híbrido", success, f"Respuesta generada: {len(result.get('response', ''))} caracteres")
        
        if success:
            print(f"   📝 Respuesta: {result['response'][:100]}...")
            print(f"   🔢 Estados cuánticos: {result['quantum_states']}")
            print(f"   🌐 Idioma: {result['language']}")
            print(f"   ⏱️ Tiempo: {result['processing_time']:.2f}ms")
        
        return True
        
    except ImportError as e:
        print_test_result("UnifiedAIService", False, f"Import error: {e}")
        return False
    except Exception as e:
        print_test_result("UnifiedAIService", False, f"Error: {e}")
        return False

def test_backend_api():
    """Probar backend Flask"""
    print_test_header("PRUEBA 2: Backend Flask Multimodal")
    
    base_url = "http://localhost:5000"
    
    try:
        # Prueba 1: Estado del sistema
        response = requests.get(f"{base_url}/api/status", timeout=10)
        status_success = response.status_code == 200
        
        if status_success:
            data = response.json()
            hybrid_active = data.get('system_mode', '').startswith('Hybrid')
            print_test_result("Estado del sistema", status_success, f"Modo: {data.get('system_mode', 'Unknown')}")
            print_test_result("Servicio híbrido", hybrid_active, f"IA Unificada: {data.get('ai_service', {}).get('unified_service_active', False)}")
        else:
            print_test_result("Estado del sistema", False, f"HTTP {response.status_code}")
            return False
        
        # Prueba 2: Endpoint de chat híbrido
        chat_data = {
            "text": "Hola, esta es una prueba del sistema híbrido VIGOLEONROCKS v4.0.0",
            "profile": "hybrid",
            "quantum_states": 26
        }
        
        response = requests.post(f"{base_url}/api/chat", json=chat_data, timeout=15)
        chat_success = response.status_code == 200
        
        if chat_success:
            data = response.json()
            has_response = bool(data.get('response', '').strip())
            print_test_result("Chat híbrido", chat_success and has_response, f"Respuesta: {len(data.get('response', ''))} caracteres")
            
            if has_response:
                print(f"   📝 Respuesta: {data['response'][:150]}...")
                print(f"   🌐 Idioma: {data.get('language', 'N/A')}")
                print(f"   ⚛️ Coherencia: {data.get('coherence_level', 0)}%")
                print(f"   📊 Supremacy: {data.get('supremacy_score', 0)}")
        else:
            print_test_result("Chat híbrido", False, f"HTTP {response.status_code}")
        
        return status_success and chat_success
        
    except requests.exceptions.ConnectionError:
        print_test_result("Backend Flask", False, "No se puede conectar al backend (¿está ejecutándose en puerto 5000?)")
        return False
    except Exception as e:
        print_test_result("Backend Flask", False, f"Error: {e}")
        return False

def test_multimodal_processing():
    """Probar procesamiento multimodal"""
    print_test_header("PRUEBA 3: Procesamiento Multimodal")
    
    base_url = "http://localhost:5000"
    
    try:
        # Crear un archivo de prueba simple
        test_content = """
        Hola, este es un documento de prueba para el sistema VIGOLEONROCKS.
        Contiene texto en español para probar la detección de idioma.
        El sistema debería analizar este contenido y generar insights inteligentes.
        
        Características a probar:
        1. Detección de idioma
        2. Conteo de palabras
        3. Análisis contextual
        4. Generación de respuesta conversacional
        """
        
        # Preparar datos multimodales
        files = {
            'files': ('test_document.txt', test_content, 'text/plain')
        }
        data = {
            'text': 'Por favor analiza este documento de prueba',
            'format': 'natural'
        }
        
        response = requests.post(f"{base_url}/api/process", files=files, data=data, timeout=20)
        success = response.status_code == 200
        
        if success:
            result = response.json()
            has_analysis = bool(result.get('integrated_response', '').strip())
            files_processed = len(result.get('files_processed', []))
            
            print_test_result("Procesamiento multimodal", success and has_analysis, f"Archivos: {files_processed}")
            
            if has_analysis:
                print(f"   📄 Respuesta integrada: {len(result['integrated_response'])} caracteres")
                print(f"   🔄 ID procesamiento: {result.get('processing_id', 'N/A')}")
                print(f"   ⏱️ Tiempo: {result.get('processing_time_ms', 0)}ms")
                
                # Mostrar parte de la respuesta
                response_preview = result['integrated_response'].replace('<br>', '\n').replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '')
                print(f"   📝 Vista previa:\n{response_preview[:300]}...")
        else:
            print_test_result("Procesamiento multimodal", False, f"HTTP {response.status_code}")
        
        return success
        
    except Exception as e:
        print_test_result("Procesamiento multimodal", False, f"Error: {e}")
        return False

def test_gateway():
    """Probar gateway OpenRouter"""
    print_test_header("PRUEBA 4: Gateway OpenRouter")
    
    base_url = "http://localhost:8004"
    
    try:
        # Prueba 1: Estado del gateway
        response = requests.get(f"{base_url}/health", timeout=10)
        health_success = response.status_code == 200
        
        if health_success:
            data = response.json()
            hybrid_active = data.get('hybrid_service') == 'active'
            print_test_result("Health check", health_success, f"Estado: {data.get('status', 'unknown')}")
            print_test_result("Servicio híbrido", hybrid_active, f"Backend: {data.get('main_api', 'unknown')}")
        else:
            print_test_result("Health check", False, f"HTTP {response.status_code}")
        
        # Prueba 2: Endpoint de modelos
        response = requests.get(f"{base_url}/v1/models", timeout=10)
        models_success = response.status_code == 200
        
        if models_success:
            data = response.json()
            has_models = len(data.get('data', [])) > 0
            print_test_result("Listado de modelos", has_models, f"Modelos disponibles: {len(data.get('data', []))}")
            
            if has_models:
                model = data['data'][0]
                print(f"   🤖 Modelo: {model.get('name', 'N/A')}")
                print(f"   💰 Precio prompt: ${model.get('pricing', {}).get('prompt', 0)}/1K")
                print(f"   📊 Contexto: {model.get('context_length', 0):,} tokens")
        else:
            print_test_result("Listado de modelos", False, f"HTTP {response.status_code}")
        
        # Prueba 3: Chat completions (estilo OpenRouter)
        completion_data = {
            "model": "vigoleonrocks/vigoleonrocks-quantum-hybrid-500k",
            "messages": [
                {"role": "user", "content": "Hola, esta es una prueba del gateway OpenRouter para VIGOLEONROCKS"}
            ]
        }
        
        response = requests.post(f"{base_url}/v1/chat/completions", json=completion_data, timeout=15)
        completion_success = response.status_code == 200
        
        if completion_success:
            data = response.json()
            has_completion = bool(data.get('choices', [{}])[0].get('message', {}).get('content', '').strip())
            print_test_result("Chat completions", completion_success and has_completion, f"Tokens: {data.get('usage', {}).get('total_tokens', 0)}")
            
            if has_completion:
                message = data['choices'][0]['message']['content']
                usage = data.get('usage', {})
                metadata = data.get('vigoleonrocks_metadata', {})
                
                print(f"   📝 Respuesta: {message[:100]}...")
                print(f"   💰 Costo: ${usage.get('cost', 0):.6f}")
                print(f"   ⚛️ Coherencia: {metadata.get('quantum_coherence', 0)}%")
                print(f"   🎯 Supremacy: {metadata.get('supremacy_score', 0)}")
        else:
            print_test_result("Chat completions", False, f"HTTP {response.status_code}")
        
        return health_success and models_success and completion_success
        
    except requests.exceptions.ConnectionError:
        print_test_result("Gateway OpenRouter", False, "No se puede conectar al gateway (¿está ejecutándose en puerto 8004?)")
        return False
    except Exception as e:
        print_test_result("Gateway OpenRouter", False, f"Error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 VIGOLEONROCKS v4.0.0 - Suite de Pruebas del Sistema Híbrido")
    print(f"⏰ Iniciado: {datetime.now().isoformat()}")
    print()
    
    results = []
    
    # Ejecutar todas las pruebas
    results.append(("UnifiedAIService", test_unified_service()))
    results.append(("Backend Flask", test_backend_api()))
    results.append(("Multimodal Processing", test_multimodal_processing()))
    results.append(("Gateway OpenRouter", test_gateway()))
    
    # Resumen final
    print_test_header("RESUMEN DE PRUEBAS")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ¡Todos los sistemas funcionan correctamente!")
        print("✅ El sistema híbrido VIGOLEONROCKS v4.0.0 está listo para producción")
    else:
        print("⚠️ Algunos sistemas requieren atención antes del despliegue")
        print("🔧 Revisa los logs de error arriba para detalles específicos")
    
    print()
    print("📝 PRÓXIMOS PASOS:")
    if passed == total:
        print("   1. Transferir archivos actualizados al VPS")
        print("   2. Detener contenedores antiguos")
        print("   3. Construir nuevas imágenes Docker")
        print("   4. Desplegar sistema híbrido en producción")
    else:
        print("   1. Corregir problemas identificados")
        print("   2. Volver a ejecutar pruebas")
        print("   3. Proceder con despliegue una vez todo pase")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Pruebas interrumpidas por el usuario")
        sys.exit(2)
    except Exception as e:
        print(f"\n💥 Error crítico en suite de pruebas: {e}")
        sys.exit(3)
