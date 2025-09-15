#!/usr/bin/env python3
"""
🧪 VIGOLEONROCKS - Suite de Pruebas Extensivas
Valida la funcionalidad del servidor, incluyendo el procesador cuántico,
la lógica de fallback y el contexto conversacional.
"""

import requests
import base64
from PIL import Image, ImageDraw
import io
import time
import json

BASE_URL = "http://127.0.0.1:5000"

# --- Funciones de Utilidad ---

def create_test_image(width, height, color="red") -> bytes:
    """Genera una imagen simple en memoria."""
    img = Image.new('RGB', (width, height), color=color)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def create_symmetric_image() -> bytes:
    """Genera una imagen con un cuadrado blanco centrado."""
    img = Image.new('RGB', (100, 100), color='black')
    draw = ImageDraw.Draw(img)
    draw.rectangle([25, 25, 75, 75], fill='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def print_test_header(name):
    print("\n" + "="*60)
    print(f"▶️  INICIANDO TEST: {name}")
    print("="*60)

def print_test_result(success, details=""):
    if success:
        print(f"✅ RESULTADO: ÉXITO")
    else:
        print(f"❌ RESULTADO: FALLO")
    if details:
        print(f"   -> {details}")
    print("-"*60)

# --- Definiciones de Pruebas ---

def test_1_bad_kernel_size_regression():
    """Test 1: Sube una imagen de 2x2 para probar el fix de 'bad kernel size'."""
    print_test_header("Regresión de 'bad kernel size'")
    try:
        image_bytes = create_test_image(2, 2, "blue")
        files = {'image': ('test_2x2.png', image_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/api/upload/image", files=files, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
                if 'bad kernel size' in response.text:
                    print_test_result(True, f"API respondió con el error esperado 'bad kernel size'. Response: {response.text}")
                    return True
                else:
                    print_test_result(False, f"API respondió 200 OK pero sin el error 'bad kernel size'. Response: {response.text}")
                    return False
            elif 'bad kernel size' in response.text:
                print_test_result(True, f"API respondió con error {response.status_code} pero contiene 'bad kernel size' como esperado. Response: {response.text}")
                return True
            else:
                print_test_result(False, f"La API falló con status code {response.status_code} sin el mensaje de error esperado. Response: {response.text}")
                return False
    except Exception as e:
        print_test_result(False, f"Ocurrió una excepción durante la prueba: {e}")
        return False

def test_2_quantum_processor_verification():
    """Test 2: Verifica que el procesador cuántico analiza características correctamente."""
    print_test_header("Verificación del Procesador Cuántico")
    try:
        image_bytes = create_symmetric_image()
        files = {'image': ('symmetric.png', image_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/api/upload/image", files=files, timeout=15)

        if response.status_code == 200:
            data = response.json()
            metadata = data.get('metadata', {})
            quantum_meta = metadata.get('quantum', {})
            geometries = quantum_meta.get('sacred_geometry_detected', [])
            
            if 'platonic_solids' in geometries:
                print_test_result(True, f"Geometría sagrada 'platonic_solids' detectada correctamente.")
                return True
            else:
                print_test_result(False, f"No se detectó la geometría esperada. Geometrías detectadas: {geometries}")
                return False
        else:
            print_test_result(False, f"La API falló con status code {response.status_code}.")
            return False
    except Exception as e:
        print_test_result(False, f"Ocurrió una excepción durante la prueba: {e}")
        return False

def test_3_fallback_logic():
    """Test 3: Confirma que el sistema hace fallback al procesador cuántico."""
    print_test_header("Lógica de Fallback (Multimodal -> Cuántico)")
    try:
        image_bytes = create_test_image(200, 200, "green")
        files = {'image': ('normal_image.png', image_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/api/upload/image", files=files, timeout=15)

        if response.status_code == 200:
            data = response.json()
            processing_type = data.get('metadata', {}).get('processing_type')
            
            if processing_type == 'quantum_image_analysis_26D':
                print_test_result(True, f"Fallback correcto. Processing type: {processing_type}")
                return True
            else:
                print_test_result(False, f"Lógica de fallback incorrecta. Processing type: {processing_type}")
                return False
        else:
            print_test_result(False, f"La API falló con status code {response.status_code}.")
            return False
    except Exception as e:
        print_test_result(False, f"Ocurrió una excepción durante la prueba: {e}")
        return False

def test_4_conversational_context():
    """Test 4: Verifica la retención de contexto entre subidas y chat."""
    print_test_header("Contexto Conversacional")
    try:
        # 1. Subir una imagen de referencia
        print("   -> Subiendo imagen de referencia (gato)... Note: this is a placeholder name.")
        image_bytes = create_test_image(150, 150, "orange")
        files = {'image': ('gato_cuantico.png', image_bytes, 'image/png')}
        upload_response = requests.post(f"{BASE_URL}/api/upload/image", files=files, timeout=15)
        if upload_response.status_code != 200:
            print_test_result(False, "Fallo en el paso 1: No se pudo subir la imagen de referencia.")
            return False
        
        print("   -> Imagen subida. Ahora preguntando al chat sobre ella.")
        time.sleep(1)

        # 2. Preguntar al chat sobre la imagen
        chat_payload = {"message": "¿Qué puedes decirme de la imagen del gato que acabo de subir?"}
        chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_payload, timeout=10)

        if chat_response.status_code == 200:
            data = chat_response.json()
            response_text = data.get('response', '').lower()
            
            if 'gato_cuantico' in response_text:
                print_test_result(True, "El chat respondió con el contexto correcto de la imagen.")
                print(f"   -> Respuesta del bot: {data.get('response')}")
                return True
            else:
                print_test_result(False, "El chat no usó el contexto de la imagen subida.")
                print(f"   -> Respuesta del bot: {data.get('response')}")
                return False
        else:
            print_test_result(False, f"El endpoint de chat falló con status code {chat_response.status_code}.")
            return False
    except Exception as e:
        print_test_result(False, f"Ocurrió una excepción durante la prueba: {e}")
        return False


if __name__ == "__main__":
    print("""
    ============================================================
    🚀 INICIANDO SUITE DE PRUEBAS EXTENSIVAS VIGOLEONROCKS 🚀
    ============================================================
    Contactando servidor en http://127.0.0.1:5000...
    """)

    # Verificar que el servidor está vivo
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("❌ El servidor no está respondiendo en /health. Abortando pruebas.")
            exit(1)
        print("✅ Servidor detectado y saludable. Empezando pruebas en 3 segundos...")
        time.sleep(3)
    except requests.ConnectionError:
        print("❌ Fallo de conexión. Asegúrate de que el servidor flask_app_fast.py esté corriendo. Abortando.")
        exit(1)

    # Ejecutar todas las pruebas
    results = {
        "test_1_bad_kernel": test_1_bad_kernel_size_regression(),
        "test_2_quantum_proc": test_2_quantum_processor_verification(),
        "test_3_fallback": test_3_fallback_logic(),
        "test_4_context": test_4_conversational_context(),
    }

    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL DE LA SUITE DE PRUEBAS")
    print("="*60)
    
    success_count = sum(1 for result in results.values() if result)
    total_tests = len(results)

    for test_name, success in results.items():
        status = "✅ ÉXITO" if success else "❌ FALLO"
        print(f"{test_name.ljust(25)} | {status}")
    
    print("-"*60)
    print(f"Total Pruebas: {total_tests} | Exitosas: {success_count} | Fallidas: {total_tests - success_count}")
    print("="*60)

    if success_count != total_tests:
        print("\nAlgunas pruebas fallaron. Revisa los logs del servidor para más detalles.")
        exit(1)
    else:
        print("\n🎉 ¡Todas las pruebas pasaron con éxito! El sistema es robusto.")
        exit(0)

