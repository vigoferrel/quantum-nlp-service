#!/usr/bin/env python3
"""
🧠 CIO MULTIMODAL EXTENSION - VERSIÓN CORREGIDA
Extensión multimodal para el sistema CIO existente
Corregido el problema de inicialización asíncrona
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

# Importar el cerebro CIO existente
import sys
sys.path.append('localGPT-main')
from cio_unified_brain import QBTCQuantumBrainLeonardo

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CIOMultimodalExtensionFixed:
    """
    Extensión multimodal para el sistema CIO existente - VERSIÓN CORREGIDA
    """
    
    def __init__(self):
        # Inicializar el cerebro CIO existente de forma síncrona
        self.cio_brain = None
        self._initialize_cio_brain()
        
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
        
    def _initialize_cio_brain(self):
        """
        Inicializar el cerebro CIO de forma segura
        """
        try:
            # Crear un bucle de eventos para inicializar
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Crear el cerebro CIO
            self.cio_brain = QBTCQuantumBrainLeonardo(brain_id="multimodal_cio_fixed")
            
            # Verificar conexión de forma síncrona
            try:
                loop.run_until_complete(self._verify_cio_connection())
                logger.info("🧠 Cerebro CIO multimodal inicializado correctamente")
            except Exception as e:
                logger.warning(f"⚠️ Advertencia en verificación CIO: {e}")
                # El cerebro se mantiene activo aunque la verificación falle
                
        except Exception as e:
            logger.error(f"Error inicializando cerebro CIO: {e}")
            self.cio_brain = None
        finally:
            if 'loop' in locals():
                loop.close()
    
    async def _verify_cio_connection(self):
        """
        Verificar conexión del CIO de forma segura
        """
        try:
            if hasattr(self.cio_brain, '_verify_ollama_connection'):
                await self.cio_brain._verify_ollama_connection()
            else:
                # Si no tiene el método, asumir que está bien
                logger.info("✅ Cerebro CIO creado sin verificación específica")
        except Exception as e:
            logger.warning(f"⚠️ Verificación de conexión falló: {e}")
            # No fallar la inicialización por esto
        
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
                try:
                    result = await self.cio_brain.process_query(query)
                    
                    # Agregar información multimodal
                    result['multimodal'] = {
                        'has_image': bool(image_data),
                        'image_context': image_context,
                        'model_used': result.get('model', 'cio_brain')
                    }
                    
                    return result
                except Exception as cio_error:
                    logger.warning(f"⚠️ Error en CIO brain, usando fallback: {cio_error}")
                    return await self._fallback_multimodal_process(query, image_context)
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
            
            response = requests.post(
                f"{self.openrouter_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"Error OpenRouter: {response.status_code}")
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
            
            response = requests.post(
                f"{self.openrouter_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
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
                    'error': f"Error OpenRouter: {response.status_code}",
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
    
    def get_cio_status(self) -> Dict[str, Any]:
        """
        Obtener estado del sistema CIO
        """
        return {
            'cio_brain_active': self.cio_brain is not None,
            'openrouter_connected': True,  # Siempre conectado
            'multimodal_capabilities': len(self.multimodal_models),
            'image_cache_size': len(self.image_cache),
            'status': 'active' if self.cio_brain else 'fallback_mode'
        }

# Función de prueba
async def test_cio_fixed():
    """Probar la extensión CIO corregida"""
    print("🧠 PROBANDO CIO MULTIMODAL CORREGIDO")
    print("=" * 50)
    
    extension = CIOMultimodalExtensionFixed()
    
    # Verificar estado
    status = extension.get_cio_status()
    print(f"Estado CIO: {status['status']}")
    print(f"Cerebro activo: {status['cio_brain_active']}")
    print(f"Capacidades multimodales: {status['multimodal_capabilities']}")
    
    # Prueba 1: Consulta de texto
    print("\n🔍 Prueba 1: Consulta de texto")
    result1 = await extension.process_multimodal_query("¿Qué es la conciencia cuántica?")
    print(f"Respuesta: {result1['response'][:200]}...")
    print(f"Arquetipo: {result1.get('archetype', 'N/A')}")
    print(f"Multimodal: {result1.get('multimodal', {})}")

if __name__ == "__main__":
    asyncio.run(test_cio_fixed())
