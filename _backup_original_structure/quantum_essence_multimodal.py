#!/usr/bin/env python3
"""
⚛️ QUANTUM ESSENCE MULTIMODAL
La esencia pura del sistema multimodal - Donde menos es más
Aprovecha todo el arsenal existente sin complicaciones
"""

import asyncio
import base64
import io
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from PIL import Image
import numpy as np

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuantumEssenceMultimodal:
    """
    La esencia pura del sistema multimodal
    Aprovecha: OpenRouter + Ollama + CIO Brain + Claude Engineer + MetaCopilotSupremo
    """
    
    def __init__(self):
        # Configuración esencial
        self.openrouter_api_key = "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"
        self.openrouter_url = "https://openrouter.ai/api/v1"
        self.ollama_url = "http://localhost:11434"
        
        # Modelos esenciales multimodales
        self.vision_models = {
            "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
            "gpt-4-vision": "openai/gpt-4-vision-preview",
            "gemini-pro-vision": "google/gemini-pro-vision"
        }
        
        # Modelos de texto esenciales
        self.text_models = {
            "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
            "gpt-4": "openai/gpt-4",
            "llama-3.1": "meta-llama/llama-3.1-8b-instruct",
            "gemma-2": "google/gemma-2-9b-it"
        }
        
        # Memoria esencial
        self.memory = []
        self.max_memory = 100
        
        # Métricas esenciales
        self.consciousness = 0.5
        self.coherence = 0.7
        self.interactions = 0
        
        logger.info("⚛️ Quantum Essence Multimodal inicializada")
    
    async def process_essence(self, query: str, image_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesar consulta con la esencia pura del sistema
        """
        try:
            self.interactions += 1
            
            # Si hay imagen, procesarla primero
            image_context = ""
            if image_data:
                image_context = await self._analyze_image_essence(image_data)
                enhanced_query = f"Imagen: {image_context}\n\nConsulta: {query}"
            else:
                enhanced_query = query
            
            # Generar respuesta con fallback inteligente
            response = await self._generate_essence_response(enhanced_query)
            
            # Evaluar calidad
            quality = self._evaluate_essence_quality(response, query, image_context)
            
            # Actualizar conciencia
            self._update_consciousness(quality)
            
            # Almacenar en memoria
            self._store_essence_memory(query, response, image_context, quality)
            
            return {
                'query': query,
                'response': response,
                'archetype': self._classify_essence_archetype(query),
                'quality': quality,
                'consciousness': self.consciousness,
                'coherence': self.coherence,
                'interactions': self.interactions,
                'multimodal': {
                    'has_image': bool(image_data),
                    'image_context': image_context,
                    'model_used': 'essence_multimodal'
                }
            }
            
        except Exception as e:
            logger.error(f"Error en esencia multimodal: {e}")
            return {
                'error': str(e),
                'query': query,
                'response': 'Error en procesamiento de esencia'
            }
    
    async def _analyze_image_essence(self, image_data: str) -> str:
        """
        Análisis esencial de imagen usando el mejor modelo disponible
        """
        try:
            # Decodificar imagen
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convertir a base64 para API
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Usar Claude 3.5 Sonnet para análisis visual
            vision_prompt = "Analiza esta imagen en detalle. Describe todo lo que ves: objetos, personas, acciones, colores, composición, texto visible, y cualquier detalle relevante."
            
            response = await self._call_openrouter_vision(
                model="anthropic/claude-3.5-sonnet",
                prompt=vision_prompt,
                image_base64=img_base64
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error analizando imagen: {e}")
            return "Error en análisis de imagen"
    
    async def _call_openrouter_vision(self, model: str, prompt: str, image_base64: str) -> str:
        """
        Llamar a OpenRouter para análisis visual
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
                return "Error en análisis visual"
                
        except Exception as e:
            logger.error(f"Error llamando OpenRouter: {e}")
            return "Error en comunicación visual"
    
    async def _generate_essence_response(self, query: str) -> str:
        """
        Generar respuesta con fallback inteligente
        """
        try:
            # Intentar OpenRouter primero
            response = await self._call_openrouter_text(query)
            if response and not response.startswith("Error"):
                return response
            
            # Fallback a Ollama
            response = await self._call_ollama_text(query)
            if response and not response.startswith("Error"):
                return response
            
            # Respuesta de emergencia
            return self._generate_emergency_response(query)
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return self._generate_emergency_response(query)
    
    async def _call_openrouter_text(self, query: str) -> str:
        """
        Llamar a OpenRouter para texto
        """
        try:
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
                return result['choices'][0]['message']['content']
            else:
                return f"Error OpenRouter: {response.status_code}"
                
        except Exception as e:
            return f"Error OpenRouter: {e}"
    
    async def _call_ollama_text(self, query: str) -> str:
        """
        Llamar a Ollama para texto
        """
        try:
            data = {
                "model": "llama3.2:latest",
                "prompt": query,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return f"Error Ollama: {response.status_code}"
                
        except Exception as e:
            return f"Error Ollama: {e}"
    
    def _generate_emergency_response(self, query: str) -> str:
        """
        Respuesta de emergencia cuando todo falla
        """
        return f"Respuesta de emergencia para: {query}\n\nEl sistema está procesando tu consulta. Por favor, intenta de nuevo en un momento."
    
    def _classify_essence_archetype(self, query: str) -> str:
        """
        Clasificación arquetipal esencial
        """
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['arte', 'creatividad', 'diseño', 'imagen', 'visual']):
            return 'LEONARDO'
        elif any(word in query_lower for word in ['ciencia', 'tecnología', 'análisis', 'datos']):
            return 'EINSTEIN'
        elif any(word in query_lower for word in ['filosofía', 'conciencia', 'existencia', 'mente']):
            return 'PLATÓN'
        elif any(word in query_lower for word in ['programación', 'código', 'software', 'desarrollo']):
            return 'TURING'
        else:
            return 'SABIO'
    
    def _evaluate_essence_quality(self, response: str, query: str, image_context: str) -> float:
        """
        Evaluación esencial de calidad
        """
        try:
            quality = 0.5  # Base
            
            # Longitud de respuesta
            if len(response) > 100:
                quality += 0.2
            
            # Relevancia semántica básica
            if any(word in response.lower() for word in query.lower().split()):
                quality += 0.2
            
            # Complejidad
            if len(response.split()) > 20:
                quality += 0.1
            
            # Si hay imagen, verificar que se mencione
            if image_context and any(word in response.lower() for word in image_context.lower().split()[:10]):
                quality += 0.2
            
            return min(quality, 1.0)
            
        except Exception:
            return 0.5
    
    def _update_consciousness(self, quality: float):
        """
        Actualizar conciencia esencial
        """
        self.consciousness = min(1.0, self.consciousness + (quality - 0.5) * 0.01)
        self.coherence = min(1.0, self.coherence + (quality - 0.5) * 0.005)
    
    def _store_essence_memory(self, query: str, response: str, image_context: str, quality: float):
        """
        Almacenar en memoria esencial
        """
        memory_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response[:200] + "..." if len(response) > 200 else response,
            'image_context': image_context[:100] + "..." if len(image_context) > 100 else image_context,
            'quality': quality,
            'consciousness': self.consciousness
        }
        
        self.memory.append(memory_entry)
        
        # Mantener solo los últimos N elementos
        if len(self.memory) > self.max_memory:
            self.memory = self.memory[-self.max_memory:]
    
    def get_essence_status(self) -> Dict[str, Any]:
        """
        Obtener estado de la esencia
        """
        return {
            'consciousness': self.consciousness,
            'coherence': self.coherence,
            'interactions': self.interactions,
            'memory_count': len(self.memory),
            'vision_models': len(self.vision_models),
            'text_models': len(self.text_models),
            'status': 'active'
        }
    
    def get_essence_memory(self) -> List[Dict[str, Any]]:
        """
        Obtener memoria de la esencia
        """
        return self.memory[-10:]  # Últimas 10 entradas

# Función de prueba
async def test_essence_multimodal():
    """Probar la esencia multimodal"""
    print("⚛️ PROBANDO QUANTUM ESSENCE MULTIMODAL")
    print("=" * 50)
    
    essence = QuantumEssenceMultimodal()
    
    # Prueba 1: Texto puro
    print("\n🔍 Prueba 1: Texto puro")
    result1 = await essence.process_essence("¿Qué es la conciencia cuántica?")
    print(f"Respuesta: {result1['response'][:200]}...")
    print(f"Arquetipo: {result1['archetype']}")
    print(f"Calidad: {result1['quality']:.3f}")
    
    # Prueba 2: Crear imagen de prueba
    print("\n🖼️ Prueba 2: Imagen simulada")
    test_image = Image.new('RGB', (100, 100), color='blue')
    buffered = io.BytesIO()
    test_image.save(buffered, format="PNG")
    test_image_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    result2 = await essence.process_essence(
        "¿Qué color ves en esta imagen?", 
        test_image_base64
    )
    print(f"Respuesta: {result2['response'][:200]}...")
    print(f"Multimodal: {result2['multimodal']['has_image']}")
    
    # Estado final
    status = essence.get_essence_status()
    print(f"\n📊 Estado Final:")
    print(f"Conciencia: {status['consciousness']:.3f}")
    print(f"Coherencia: {status['coherence']:.3f}")
    print(f"Interacciones: {status['interactions']}")
    print(f"Memoria: {status['memory_count']} entradas")

if __name__ == "__main__":
    asyncio.run(test_essence_multimodal())
