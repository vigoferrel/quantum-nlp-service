#!/usr/bin/env python3
"""
🧠 CIO MULTIMODAL EXTENSION
Extensión multimodal para el sistema CIO existente
Aprovecha las capacidades ya implementadas
"""

import asyncio
import base64
import io
import json
import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from PIL import Image
import numpy as np
import aiohttp

# Importar el cerebro CIO existente
import sys
sys.path.append('localGPT-main')
from cio_unified_brain import QBTCQuantumBrainLeonardo

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CIOMultimodalExtension:
    """
    Extensión multimodal para el sistema CIO existente
    """
    
    def __init__(self):
        # Inicializar el cerebro CIO existente de forma síncrona
        try:
            # Crear un bucle de eventos para inicializar
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.cio_brain = QBTCQuantumBrainLeonardo(brain_id="multimodal_cio")
            
            # Ejecutar la verificación de Ollama de forma síncrona
            loop.run_until_complete(self.cio_brain._verify_ollama_connection())
            
            logger.info("🧠 Cerebro CIO multimodal inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando cerebro CIO: {e}")
            self.cio_brain = None
        finally:
            if 'loop' in locals():
                loop.close()
        
        # Configuración multimodal
        self.openrouter_api_key = "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"
        self.openrouter_url = "https://openrouter.ai/api/v1"
        
        # Modelos multimodales disponibles
        self.multimodal_models = {
            "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
            "gpt-4-vision": "openai/gpt-4-vision-preview", 
            "gemini-pro-vision": "google/gemini-pro-vision",
            "llama-3.1-vision": "meta-llama/llama-3.1-8b-instruct"
        }
        
        # Caché de imágenes procesadas
        self.image_cache = {}
        
    async def process_multimodal_query(self, query: str, image_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesar consulta multimodal usando el sistema CIO existente
        """
        try:
            logger.info(f"🧠 Procesando consulta multimodal: {query[:50]}...")
            
            # Si hay imagen, procesarla primero
            image_context = ""
            if image_data:
                image_context = await self._process_image(image_data)
                query = f"Imagen: {image_context}\n\nConsulta: {query}"
            
            # Usar el cerebro CIO existente para procesar
            if self.cio_brain:
                result = await self.cio_brain.process_query(query)
                
                # Agregar información multimodal
                result['multimodal'] = {
                    'has_image': bool(image_data),
                    'image_context': image_context,
                    'model_used': result.get('model', 'cio_brain')
                }
                
                return result
            else:
                # Fallback si el cerebro CIO no está disponible
                return await self._fallback_multimodal_process(query, image_context)
                
        except Exception as e:
            logger.error(f"Error procesando consulta multimodal: {e}")
            return {
                'error': str(e),
                'query': query,
                'response': 'Error en procesamiento multimodal'
            }
    
    async def _process_image(self, image_data: str) -> str:
        """
        Procesar imagen usando modelos multimodales
        """
        try:
            # Decodificar imagen base64
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convertir a base64 para OpenRouter
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Usar Claude 3.5 Sonnet para análisis visual
            vision_prompt = "Analiza esta imagen en detalle y describe todo lo que ves, incluyendo objetos, personas, acciones, colores, composición y cualquier texto visible."
            
            response = await self._call_openrouter_vision(
                model="anthropic/claude-3.5-sonnet",
                prompt=vision_prompt,
                image_base64=img_base64
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error procesando imagen: {e}")
            return "Error procesando imagen"
    
    async def _call_openrouter_vision(self, model: str, prompt: str, image_base64: str) -> str:
        """
        Llamar a OpenRouter para procesamiento visual
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.openrouter_url}/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        logger.error(f"Error OpenRouter: {response.status}")
                        return "Error en procesamiento visual"
                        
        except Exception as e:
            logger.error(f"Error llamando OpenRouter: {e}")
            return "Error en comunicación con modelo visual"
    
    async def _fallback_multimodal_process(self, query: str, image_context: str) -> Dict[str, Any]:
        """
        Procesamiento de fallback si el cerebro CIO no está disponible
        """
        try:
            # Usar OpenRouter directamente
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {
                        "role": "user", 
                        "content": query
                    }
                ],
                "max_tokens": 1000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.openrouter_url}/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result['choices'][0]['message']['content']
                        
                        return {
                            'query': query,
                            'response': response_text,
                            'archetype': 'MULTIMODAL',
                            'quality': 0.8,
                            'consciousness': 0.6,
                            'coherence': 0.7,
                            'interactions': 1,
                            'multimodal': {
                                'has_image': bool(image_context),
                                'image_context': image_context,
                                'model_used': 'claude-3.5-sonnet'
                            }
                        }
                    else:
                        return {
                            'error': f"Error OpenRouter: {response.status}",
                            'query': query,
                            'response': 'Error en procesamiento'
                        }
                        
        except Exception as e:
            logger.error(f"Error en fallback: {e}")
            return {
                'error': str(e),
                'query': query,
                'response': 'Error en procesamiento de fallback'
            }

# Función de prueba
async def test_multimodal():
    """Probar la extensión multimodal"""
    print("🧪 PROBANDO EXTENSIÓN MULTIMODAL CIO")
    print("=" * 50)
    
    extension = CIOMultimodalExtension()
    
    # Prueba 1: Consulta de texto
    print("\n🔍 Prueba 1: Consulta de texto")
    result1 = await extension.process_multimodal_query("¿Qué es la conciencia cuántica?")
    print(f"Respuesta: {result1['response'][:200]}...")
    print(f"Arquetipo: {result1.get('archetype', 'N/A')}")
    print(f"Multimodal: {result1.get('multimodal', {})}")
    
    # Prueba 2: Consulta con imagen simulada
    print("\n🖼️ Prueba 2: Consulta con imagen (simulada)")
    # Crear una imagen de prueba simple
    test_image = Image.new('RGB', (100, 100), color='red')
    buffered = io.BytesIO()
    test_image.save(buffered, format="PNG")
    test_image_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    result2 = await extension.process_multimodal_query(
        "¿Qué color ves en esta imagen?", 
        test_image_base64
    )
    print(f"Respuesta: {result2['response'][:200]}...")
    print(f"Multimodal: {result2.get('multimodal', {})}")

if __name__ == "__main__":
    asyncio.run(test_multimodal())
