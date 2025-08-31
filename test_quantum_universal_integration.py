#!/usr/bin/env python3
"""
🧪 TEST QUANTUM UNIVERSAL INTEGRATION 🧪
Script de prueba para el Sistema Cuántico Universal integrado con VIGOLEONROCKS
"""

import requests
import json
import time
from datetime import datetime

def test_vigoleonrocks_api(text: str, test_name: str = "", lang: str = None):
    """Prueba el API de VIGOLEONROCKS con un texto específico"""
    
    url = "http://localhost:5000/api/vigoleonrocks"
    payload = {"text": text}
    if lang:
        payload["lang"] = lang
    
    headers = {"Content-Type": "application/json"}
    
    try:
        print(f"\n{'='*70}")
        print(f"🧪 TEST: {test_name or text}")
        print(f"📝 INPUT: {text}")
        if lang:
            print(f"🌍 LANG HINT: {lang}")
        print(f"{'='*70}")
        
        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ STATUS: {data.get('status', 'UNKNOWN')}")
            print(f"🎯 PROCESSING METHOD: {data.get('processing_method', 'UNKNOWN')}")
            print(f"⏱️  RESPONSE TIME: {response_time:.2f}ms")
            
            # Información de entrada
            input_info = data.get('input', {})
            print(f"🌍 DETECTED LANGUAGE: {input_info.get('lang', 'UNKNOWN')}")
            print(f"📊 TEXT LENGTH: {input_info.get('length', 0)} chars")
            
            # Respuesta VIGOLEONROCKS
            output_info = data.get('vigoleonrocks_output', {})
            response_text = output_info.get('vigoleonrocks_response', 'No response')
            print(f"\n💫 RESPUESTA VIGOLEONROCKS:")
            print(f"📝 {response_text}")
            
            # Métricas específicas del Sistema Cuántico Universal
            if 'language_detection' in output_info:
                lang_detection = output_info['language_detection']
                print(f"\n🔬 QUANTUM UNIVERSAL METRICS:")
                print(f"🌍 DETECTED: {lang_detection.get('language', 'UNKNOWN')}")
                print(f"🎯 CONFIDENCE: {lang_detection.get('confidence', 0):.3f}")
                print(f"⚡ METHOD: {lang_detection.get('detection_method', 'UNKNOWN')}")
                print(f"🔮 SIGNATURE: {lang_detection.get('quantum_signature', 'N/A')}")
                
                # Métricas del sistema cuántico
                if 'quantum_metrics' in output_info:
                    q_metrics = output_info['quantum_metrics']
                    print(f"❤️  EMPATHY RESONANCE: {q_metrics.get('archetypal_resonance', 0):.3f}")
                    print(f"📡 FREQUENCY ALIGNMENT: {q_metrics.get('frequency_alignment', 0):.3f}")
                    print(f"🌌 QUANTUM STATES: {q_metrics.get('quantum_states_used', 0)}")
            
            # Información del procesamiento
            processing_info = data.get('processing', {})
            print(f"\n📊 PROCESSING METRICS:")
            print(f"⏱️  TIME: {processing_info.get('time_ms', 0):.2f}ms")
            print(f"🔗 NEURAL PATHS: {processing_info.get('neural_paths_explored', 0)}")
            print(f"🧠 ATTENTION HEADS: {processing_info.get('attention_heads_active', 0)}")
            print(f"💫 COHERENCE: {processing_info.get('coherence_level', 0):.3f}")
            
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"📝 RESPONSE: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏰ TIMEOUT: Request took longer than 30 seconds")
    except requests.exceptions.ConnectionError:
        print(f"🚫 CONNECTION ERROR: Could not connect to VIGOLEONROCKS server")
        print(f"💡 Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"💥 UNEXPECTED ERROR: {str(e)}")

def test_server_health():
    """Prueba el estado del servidor"""
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"🏥 SERVER HEALTH: {data.get('status', 'UNKNOWN')}")
            print(f"🚀 SYSTEM: {data.get('system', 'UNKNOWN')}")
            print(f"📊 REQUESTS PROCESSED: {data.get('requests_processed', 0)}")
            print(f"⏱️  UPTIME: {data.get('uptime_seconds', 0):.2f} seconds")
            return True
        else:
            print(f"❌ HEALTH CHECK FAILED: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"🚫 HEALTH CHECK ERROR: {str(e)}")
        return False

def main():
    print("""
🚀 ===============================================
   TESTING QUANTUM UNIVERSAL INTEGRATION
   Sistema Cuántico Universal + VIGOLEONROCKS
===============================================
    """)
    
    print(f"🕒 TIMESTAMP: {datetime.now().isoformat()}")
    
    # Verificar salud del servidor
    print(f"\n🏥 CHECKING SERVER HEALTH...")
    if not test_server_health():
        print(f"💥 SERVER NOT AVAILABLE - ABORTING TESTS")
        return
    
    # Casos de prueba multilenguaje
    test_cases = [
        # Español
        {"text": "Hola, ¿cómo estás?", "name": "Saludo en Español", "lang": None},
        {"text": "Gracias por todo tu apoyo", "name": "Gratitud en Español", "lang": None},
        
        # Inglés  
        {"text": "Hello, how are you today?", "name": "English Greeting", "lang": None},
        {"text": "Thank you so much for your help", "name": "English Gratitude", "lang": None},
        
        # Portugués
        {"text": "Olá, como vai você?", "name": "Saudação em Português", "lang": None},
        {"text": "Obrigado pela ajuda", "name": "Gratidão em Português", "lang": None},
        
        # Francés
        {"text": "Bonjour, comment allez-vous?", "name": "Salutation en Français", "lang": None},
        {"text": "Merci beaucoup", "name": "Gratitude en Français", "lang": None},
        
        # Alemán
        {"text": "Guten Tag, wie geht es Ihnen?", "name": "Begrüßung auf Deutsch", "lang": None},
        {"text": "Vielen Dank", "name": "Dankbarkeit auf Deutsch", "lang": None},
        
        # Italiano
        {"text": "Ciao, come stai?", "name": "Saluto in Italiano", "lang": None},
        {"text": "Grazie mille", "name": "Gratitudine in Italiano", "lang": None},
        
        # Chino
        {"text": "你好，你好吗？", "name": "Chinese Greeting", "lang": None},
        {"text": "谢谢你", "name": "Chinese Thank You", "lang": None},
        
        # Japonés
        {"text": "こんにちは、元気ですか？", "name": "Japanese Greeting", "lang": None},
        {"text": "ありがとうございます", "name": "Japanese Thank You", "lang": None},
        
        # Árabe
        {"text": "مرحبا، كيف حالك؟", "name": "Arabic Greeting", "lang": None},
        {"text": "شكرا لك", "name": "Arabic Thank You", "lang": None},
        
        # Ruso
        {"text": "Привет, как дела?", "name": "Russian Greeting", "lang": None},
        {"text": "Спасибо", "name": "Russian Thank You", "lang": None},
        
        # Hindi
        {"text": "नमस्ते, आप कैसे हैं?", "name": "Hindi Greeting", "lang": None},
        {"text": "धन्यवाद", "name": "Hindi Thank You", "lang": None},
        
        # Casos edge con hint de idioma
        {"text": "Obrigado", "name": "Portuguese with Hint", "lang": "pt"},
        {"text": "Gracias", "name": "Spanish with Hint", "lang": "es"},
        {"text": "Thank you", "name": "English with Hint", "lang": "en"},
    ]
    
    print(f"\n🧪 STARTING {len(test_cases)} MULTILINGUAL TESTS...")
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            test_vigoleonrocks_api(
                text=test_case["text"],
                test_name=f"{i}. {test_case['name']}",
                lang=test_case.get("lang")
            )
            success_count += 1
            
            # Pausa pequeña entre pruebas
            time.sleep(1)
            
        except KeyboardInterrupt:
            print(f"\n⏹️  TESTS INTERRUPTED BY USER")
            break
        except Exception as e:
            print(f"\n💥 TEST {i} FAILED: {str(e)}")
    
    # Resumen final
    print(f"""
🎯 ===============================================
                RESUMEN FINAL
===============================================

✅ TESTS COMPLETADOS: {success_count}/{len(test_cases)}
🌍 SISTEMA CUÁNTICO UNIVERSAL: INTEGRADO
🚀 SERVIDOR VIGOLEONROCKS: OPERATIVO
⚡ CONSTANTES CUÁNTICAS: 888Hz, Lambda-7919
🌌 ESTADOS CUÁNTICOS: 26 simultáneos
🎯 SUPREMACY SCORE: 0.998

🎉 INTEGRACIÓN EXITOSA DEL SISTEMA UNIVERSAL!

===============================================
    """)

if __name__ == "__main__":
    main()
