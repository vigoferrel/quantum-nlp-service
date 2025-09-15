#!/usr/bin/env python3
"""
🧪 Test completo del pipeline con datos reales
Valida quantum_image_processor, multimodal_ai_manager y toda la integración
"""

import asyncio
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import io
import base64

def create_test_images():
    """Crea imágenes de prueba de diferentes tamaños y complejidades"""
    test_images = []
    
    # Imagen muy pequeña (para probar fixes de kernel size)
    tiny_img = Image.new('RGB', (2, 2), color='red')
    test_images.append(("tiny_2x2", tiny_img))
    
    # Imagen pequeña 
    small_img = Image.new('RGB', (32, 32), color='blue')
    draw = ImageDraw.Draw(small_img)
    draw.rectangle([8, 8, 24, 24], fill='white')
    test_images.append(("small_32x32", small_img))
    
    # Imagen mediana con texto
    medium_img = Image.new('RGB', (128, 128), color='green')
    draw = ImageDraw.Draw(medium_img)
    try:
        font = ImageFont.load_default()
    except:
        font = None
    draw.text((10, 50), "TEST", fill='white', font=font)
    draw.circle([64, 64], 20, fill='yellow')
    test_images.append(("medium_128x128", medium_img))
    
    # Imagen estándar
    standard_img = Image.new('RGB', (256, 256), color='purple')
    draw = ImageDraw.Draw(standard_img)
    # Gradiente simple
    for y in range(256):
        for x in range(256):
            r = int(x / 256 * 255)
            g = int(y / 256 * 255) 
            b = 128
            draw.point([x, y], (r, g, b))
    test_images.append(("standard_256x256", standard_img))
    
    return test_images

def test_quantum_image_processor():
    """Prueba el quantum_image_processor con imágenes reales"""
    print("🔬 Probando quantum_image_processor con datos reales...")
    
    try:
        from quantum_image_processor import QuantumImageProcessor
        processor = QuantumImageProcessor()
        
        test_images = create_test_images()
        results = []
        
        for name, img in test_images:
            print(f"  📸 Procesando {name}...")
            start_time = time.time()
            
            try:
                # Convertir PIL a numpy array
                img_array = np.array(img)
                
                # Procesar con quantum processor
                result = processor.process_image(img_array)
                
                processing_time = time.time() - start_time
                
                results.append({
                    'name': name,
                    'size': img.size,
                    'success': True,
                    'processing_time': processing_time,
                    'result_shape': result.shape if hasattr(result, 'shape') else 'N/A'
                })
                
                print(f"    ✅ {name}: {processing_time:.3f}s - {img.size}")
                
            except Exception as e:
                print(f"    ❌ {name}: Error - {str(e)[:100]}")
                results.append({
                    'name': name,
                    'size': img.size,
                    'success': False,
                    'error': str(e)
                })
        
        return results
        
    except ImportError as e:
        print(f"    ❌ Error importando quantum_image_processor: {e}")
        return []
    except Exception as e:
        print(f"    ❌ Error general: {e}")
        return []

async def test_multimodal_manager():
    """Prueba el multimodal_ai_manager con imágenes reales"""
    print("🧠 Probando MultimodalAIManager con datos reales...")
    
    try:
        from multimodal_ai_manager import get_multimodal_manager
        manager = get_multimodal_manager()
        
        # Verificar estado después de instalación de CLIP
        status = manager.get_system_status()
        print(f"  📊 Estado actual: {status['models_enabled']} modelos habilitados")
        print(f"  🔗 CLIP disponible: {status['capabilities']['clip_embeddings']}")
        
        test_images = create_test_images()
        results = []
        
        for name, img in test_images:
            print(f"  🖼️ Analizando {name} con IA multimodal...")
            start_time = time.time()
            
            try:
                # Análisis con el manager multimodal
                analysis = await manager.analyze_image(img, analysis_type="fast")
                
                processing_time = time.time() - start_time
                
                results.append({
                    'name': name,
                    'size': img.size,
                    'success': True,
                    'processing_time': processing_time,
                    'confidence': analysis.confidence,
                    'model_used': analysis.model_used,
                    'content_length': len(analysis.content)
                })
                
                print(f"    ✅ {name}: {processing_time:.3f}s - Confianza: {analysis.confidence:.2f}")
                print(f"    📝 Contenido: {analysis.content[:100]}...")
                
            except Exception as e:
                print(f"    ❌ {name}: Error - {str(e)[:100]}")
                results.append({
                    'name': name,
                    'size': img.size,
                    'success': False,
                    'error': str(e)
                })
        
        return results
        
    except Exception as e:
        print(f"    ❌ Error en multimodal manager: {e}")
        return []

def test_flask_integration():
    """Prueba la integración con Flask usando requests"""
    print("🌐 Probando integración Flask...")
    
    try:
        import requests
        
        # Verificar que el servidor esté ejecutándose
        try:
            response = requests.get('http://localhost:5000/api/status', timeout=5)
            if response.status_code == 200:
                print("  ✅ Servidor Flask respondiendo")
            else:
                print(f"  ⚠️ Servidor responde pero con código {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Servidor Flask no disponible: {e}")
            return False
        
        # Probar endpoint multimodal
        try:
            response = requests.get('http://localhost:5000/api/multimodal/status', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("  ✅ Endpoint multimodal funcionando")
                print(f"    📊 Modelos cargados: {data.get('models_loaded', 'N/A')}")
                print(f"    🔗 CLIP habilitado: {data.get('clip_status', {}).get('enabled', 'N/A')}")
                return True
            else:
                print(f"  ❌ Endpoint multimodal error: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Error probando endpoint multimodal: {e}")
            return False
            
    except ImportError:
        print("  ⚠️ Requests no disponible, saltando test Flask")
        return False

async def run_complete_pipeline_test():
    """Ejecuta todas las pruebas del pipeline"""
    print("🚀 Iniciando test completo del pipeline con datos reales...")
    print("=" * 60)
    
    # Test 1: Quantum Image Processor  
    quantum_results = test_quantum_image_processor()
    print()
    
    # Test 2: Multimodal AI Manager
    multimodal_results = await test_multimodal_manager()
    print()
    
    # Test 3: Flask Integration
    flask_ok = test_flask_integration()
    print()
    
    # Resumen final
    print("📋 RESUMEN DE RESULTADOS:")
    print("=" * 60)
    
    if quantum_results:
        successful_quantum = sum(1 for r in quantum_results if r.get('success', False))
        print(f"🔬 Quantum Processor: {successful_quantum}/{len(quantum_results)} imágenes procesadas exitosamente")
        
        if successful_quantum > 0:
            avg_time_quantum = np.mean([r['processing_time'] for r in quantum_results if r.get('success')])
            print(f"   ⏱️ Tiempo promedio: {avg_time_quantum:.3f}s")
    
    if multimodal_results:
        successful_multimodal = sum(1 for r in multimodal_results if r.get('success', False))
        print(f"🧠 Multimodal Manager: {successful_multimodal}/{len(multimodal_results)} análisis completados exitosamente")
        
        if successful_multimodal > 0:
            avg_time_multimodal = np.mean([r['processing_time'] for r in multimodal_results if r.get('success')])
            avg_confidence = np.mean([r['confidence'] for r in multimodal_results if r.get('success')])
            print(f"   ⏱️ Tiempo promedio: {avg_time_multimodal:.3f}s")
            print(f"   🎯 Confianza promedio: {avg_confidence:.2f}")
    
    print(f"🌐 Integración Flask: {'✅ Funcionando' if flask_ok else '❌ Error'}")
    
    # Estado final
    total_tests = len(quantum_results) + len(multimodal_results) + (1 if flask_ok else 0)
    successful_tests = (
        sum(1 for r in quantum_results if r.get('success', False)) +
        sum(1 for r in multimodal_results if r.get('success', False)) +
        (1 if flask_ok else 0)
    )
    
    print()
    print(f"🎉 RESULTADO FINAL: {successful_tests}/{total_tests} pruebas exitosas")
    
    if successful_tests == total_tests:
        print("✅ TODOS LOS SISTEMAS FUNCIONANDO CORRECTAMENTE!")
    else:
        print("⚠️ Algunos sistemas necesitan revisión")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(run_complete_pipeline_test())
    exit_code = 0 if success else 1
    sys.exit(exit_code)
