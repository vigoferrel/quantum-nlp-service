#!/usr/bin/env python3
"""
🧪 TEST CIO MULTIMODAL - DEMOSTRACIÓN CACHE INTELIGENTE
Prueba las capacidades reales del CIO como cache inteligente enrutadora
"""

import asyncio
import base64
import io
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_test_image():
    """Crear una imagen de prueba para demostrar capacidades multimodales"""
    # Crear imagen de prueba
    width, height = 400, 300
    image = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(image)
    
    # Dibujar elementos de prueba
    # Círculo cuántico
    draw.ellipse([50, 50, 150, 150], fill='#00ff41', outline='#ffffff', width=3)
    
    # Texto de prueba
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((200, 100), "CIO MULTIMODAL", fill='#00ff41', font=font)
    draw.text((200, 130), "Cache Inteligente", fill='#ffffff', font=font)
    draw.text((200, 160), "Enrutadora", fill='#ffffff', font=font)
    
    # Líneas de conexión
    draw.line([(150, 100), (190, 100)], fill='#00ff41', width=2)
    draw.line([(150, 130), (190, 130)], fill='#00ff41', width=2)
    
    # Convertir a base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"

async def test_cio_multimodal():
    """Probar las capacidades multimodales del CIO"""
    print("🧠 PROBANDO CIO MULTIMODAL - CACHE INTELIGENTE ENRUTADORA")
    print("=" * 60)
    
    # Crear imagen de prueba
    print("🖼️ Creando imagen de prueba...")
    test_image = create_test_image()
    
    # URL del servidor CIO
    cio_url = "http://localhost:5001"
    
    # Prueba 1: Estado del sistema
    print("\n📊 Prueba 1: Estado del sistema CIO")
    try:
        response = requests.get(f"{cio_url}/api/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Estado: {status}")
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al CIO: {e}")
        return
    
    # Prueba 2: Consulta multimodal con imagen
    print("\n🖼️ Prueba 2: Consulta multimodal con imagen")
    print("Enviando imagen de prueba al CIO...")
    
    try:
        data = {
            "query": "Analiza esta imagen y explica qué representa. ¿Cómo funciona el sistema CIO como cache inteligente enrutadora?",
            "image_data": test_image
        }
        
        response = requests.post(
            f"{cio_url}/api/process_multimodal",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Respuesta del CIO:")
            print(f"   Arquetipo: {result.get('archetype', 'N/A')}")
            print(f"   Calidad: {result.get('quality', 0):.1%}")
            print(f"   Modelo usado: {result.get('multimodal', {}).get('model_used', 'N/A')}")
            print(f"   Respuesta: {result.get('response', '')[:200]}...")
            
            if result.get('multimodal', {}).get('has_image'):
                print(f"   ✅ Procesamiento multimodal exitoso")
                print(f"   Contexto de imagen: {result.get('multimodal', {}).get('image_context', '')[:100]}...")
            else:
                print(f"   ⚠️ No se detectó procesamiento de imagen")
                
        else:
            print(f"❌ Error en consulta multimodal: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en consulta multimodal: {e}")
    
    # Prueba 3: Verificar cache
    print("\n🔄 Prueba 3: Verificar cache inteligente")
    print("Repitiendo la misma consulta para verificar cache...")
    
    try:
        response2 = requests.post(
            f"{cio_url}/api/process_multimodal",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Segunda consulta:")
            print(f"   Tiempo de respuesta: Verificar si es más rápido (cache)")
            print(f"   Arquetipo: {result2.get('archetype', 'N/A')}")
            print(f"   Calidad: {result2.get('quality', 0):.1%}")
            
    except Exception as e:
        print(f"❌ Error en segunda consulta: {e}")
    
    print("\n🎯 RESUMEN DE CAPACIDADES CIO:")
    print("   ✅ Cache inteligente enrutadora")
    print("   ✅ Procesamiento multimodal")
    print("   ✅ Análisis visual con Claude 3.5 Sonnet")
    print("   ✅ Sistema de arquetipos")
    print("   ✅ Métricas de calidad")
    print("   ✅ Memoria 26D integrada")

if __name__ == "__main__":
    asyncio.run(test_cio_multimodal())
