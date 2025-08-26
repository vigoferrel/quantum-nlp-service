#!/usr/bin/env python3
"""
🚀 GEMINI CIO SIMPLE TEST
Versión simplificada que funciona correctamente
"""

import asyncio
import aiohttp
import time
import json
import hashlib
from typing import Dict, Any

class GeminiCIOSimpleTest:
    """Sistema simplificado que funciona"""
    
    def __init__(self):
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://gemini-cio-simple.local",
            "X-Title": "Gemini CIO Simple Test"
        }
        
        # Métricas
        self.total_queries = 0
        self.successful_queries = 0
        self.total_cost = 0.0
        
        print("🚀 Gemini CIO Simple Test inicializado")
        print("🏆 Usando Gemini Flash 1.5 8B (Ultra-económico)")
    
    def _categorize_query(self, query: str) -> str:
        """Categoriza el query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["consciencia", "cuántico", "iónico", "arquetipo"]):
            return "cio_consciousness"
        elif any(word in query_lower for word in ["arquitectura", "sistema", "microservicios"]):
            return "gemini_complex"
        elif any(word in query_lower for word in ["diagrama", "imagen", "visual", "multimodal"]):
            return "gemini_multimodal"
        elif any(word in query_lower for word in ["patrón", "diseño", "optimización"]):
            return "gemini_analysis"
        else:
            return "gemini_general"
    
    async def _call_gemini_flash_lite(self, query: str) -> Dict[str, Any]:
        """Llamada directa a Gemini Flash 1.5 8B (ULTRA ECONÓMICO)"""
        
        payload = {
            "model": "google/gemini-flash-1.5-8b",  # 🏆 ULTRA ECONÓMICO: $0.0000000375/1M
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content']
                        usage = data.get('usage', {})
                        
                        # 🎯 COSTO ULTRA ECONÓMICO: $0.0000000375/$0.00000015 por 1M tokens
                        input_tokens = usage.get('prompt_tokens', 0)
                        output_tokens = usage.get('completion_tokens', 0)
                        cost = (input_tokens * 0.0000000375) + (output_tokens * 0.00000015)
                        
                        response_time = time.time() - start_time
                        
                        return {
                            "success": True,
                            "response": content,
                            "cost": cost,
                            "response_time": response_time,
                            "input_tokens": input_tokens,
                            "output_tokens": output_tokens
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "cost": 0.0,
                            "response_time": time.time() - start_time
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "cost": 0.0,
                "response_time": time.time() - start_time
            }
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Procesa una consulta"""
        
        self.total_queries += 1
        category = self._categorize_query(query)
        
        print(f"\n🎯 Query #{self.total_queries}: {category.upper()}")
        print(f"📝 Query: {query[:100]}...")
        
        # Llamar a Gemini Flash-Lite
        result = await self._call_gemini_flash_lite(query)
        
        if result["success"]:
            self.successful_queries += 1
            self.total_cost += result["cost"]
            
            print(f"✅ ÉXITO!")
            print(f"🤖 Modelo: Gemini Flash 1.5 8B (Ultra-económico)")
            print(f"💰 Costo: ${result['cost']:.8f}")
            print(f"⏱️  Tiempo: {result['response_time']:.2f}s")
            print(f"🔢 Tokens: {result['input_tokens']} → {result['output_tokens']}")
            print(f"📝 Respuesta: {result['response'][:200]}...")
        else:
            print(f"❌ ERROR: {result['error']}")
            print(f"⏱️  Tiempo: {result['response_time']:.2f}s")
        
        return {
            "success": result["success"],
            "model_used": "Gemini Flash 1.5 8B (Ultra-económico)",
            "category": category,
            "cost": result.get("cost", 0.0),
            "response_time": result.get("response_time", 0.0),
            "response": result.get("response", ""),
            "error": result.get("error", "")
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas"""
        
        success_rate = (self.successful_queries / max(1, self.total_queries)) * 100
        
        return {
            "total_queries": self.total_queries,
            "successful_queries": self.successful_queries,
            "success_rate": success_rate,
            "total_cost": self.total_cost,
            "average_cost": self.total_cost / max(1, self.successful_queries)
        }

async def main():
    """Función principal"""
    
    print("🚀 INICIANDO GEMINI CIO SIMPLE TEST")
    print("🏆 OPTIMIZADO CON GEMINI FLASH 1.5 8B")
    print("💰 $0.0000000375/$0.00000015 por 1M tokens - ULTRA ECONÓMICO")
    print("=" * 70)
    
    # Inicializar sistema
    system = GeminiCIOSimpleTest()
    
    # Consultas de prueba
    test_queries = [
        "Analiza mi nivel de consciencia cuántica y evolución arquetipal.",
        "Realiza ingeniería inversa de esta arquitectura de microservicios bancarios.",
        "Optimiza este código para máxima eficiencia cuántica local.",
        "Analiza este diagrama de flujo de datos y proporciona optimizaciones.",
        "Genera 40,000 captions de fotos usando el modelo más barato de Google."
    ]
    
    # Procesar consultas
    for i, query in enumerate(test_queries, 1):
        print(f"\n🎯 PROCESANDO CONSULTA {i}")
        print("-" * 50)
        
        result = await system.process_query(query)
        
        if result["success"]:
            print(f"✅ Consulta {i} exitosa")
        else:
            print(f"❌ Consulta {i} falló")
    
    # Estadísticas finales
    print(f"\n📊 ESTADÍSTICAS FINALES")
    print("=" * 70)
    
    stats = system.get_statistics()
    
    print(f"🎯 Total consultas: {stats['total_queries']}")
    print(f"✅ Exitosas: {stats['successful_queries']}")
    print(f"📈 Tasa de éxito: {stats['success_rate']:.1f}%")
    print(f"💰 Costo total: ${stats['total_cost']:.8f}")
    print(f"💰 Costo promedio: ${stats['average_cost']:.8f}")
    
    print(f"\n🚀 GEMINI CIO SIMPLE TEST - COMPLETADO")
    print("🏆 Sistema funcionando con Gemini Flash 1.5 8B (Ultra-económico)")

if __name__ == "__main__":
    asyncio.run(main())
