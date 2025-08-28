#!/usr/bin/env python3
"""
🔥 SISTEMA DE WARM-UP AUTOMÁTICO
=================================
Sistema para optimizar el cold start del servidor
"""

import asyncio
import time
import requests
import json
from typing import Dict, Any

class WarmupSystem:
    def __init__(self, server_url: str = "http://localhost:5004"):
        self.server_url = server_url
        self.warmup_requests = [
            {"text": "Hola", "session_id": "warmup_1"},
            {"text": "¿Cómo estás?", "session_id": "warmup_2"},
            {"text": "Test de rendimiento", "session_id": "warmup_3"},
            {"text": "Análisis de sentimientos", "session_id": "warmup_4"},
            {"text": "Procesamiento cuántico", "session_id": "warmup_5"}
        ]
    
    async def warmup_server(self):
        """Realizar warm-up del servidor"""
        print("🔥 Iniciando warm-up del servidor...")
        
        results = []
        for i, request in enumerate(self.warmup_requests):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.server_url}/api/process_text",
                    json=request,
                    timeout=30
                )
                end_time = time.time()
                
                result = {
                    "request": i + 1,
                    "text": request["text"][:20] + "...",
                    "status_code": response.status_code,
                    "response_time": end_time - start_time,
                    "success": response.status_code == 200
                }
                
                results.append(result)
                print(f"   ✅ Warm-up {i+1}: {result['response_time']:.3f}s")
                
                # Pequeña pausa entre requests
                await asyncio.sleep(0.5)
                
            except Exception as e:
                result = {
                    "request": i + 1,
                    "text": request["text"][:20] + "...",
                    "error": str(e),
                    "success": False
                }
                results.append(result)
                print(f"   ❌ Warm-up {i+1}: Error - {e}")
        
        # Análisis de resultados
        successful = [r for r in results if r["success"]]
        avg_time = sum(r["response_time"] for r in successful) / len(successful) if successful else 0
        
        print(f"\n📊 RESULTADOS DEL WARM-UP:")
        print(f"   ✅ Requests exitosos: {len(successful)}/{len(results)}")
        print(f"   ⏱️ Tiempo promedio: {avg_time:.3f}s")
        print(f"   🎯 Estado: {'LISTO' if len(successful) >= 3 else 'NECESITA MÁS WARM-UP'}")
        
        return {
            "total_requests": len(results),
            "successful_requests": len(successful),
            "average_time": avg_time,
            "results": results
        }
    
    async def continuous_warmup(self, interval_minutes: int = 5):
        """Warm-up continuo en intervalos"""
        print(f"🔄 Iniciando warm-up continuo cada {interval_minutes} minutos...")
        
        while True:
            try:
                await self.warmup_server()
                await asyncio.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("🛑 Warm-up continuo detenido")
                break
            except Exception as e:
                print(f"⚠️ Error en warm-up continuo: {e}")
                await asyncio.sleep(60)  # Esperar 1 minuto antes de reintentar

async def main():
    """Función principal"""
    warmup_system = WarmupSystem()
    
    # Warm-up inicial
    await warmup_system.warmup_server()
    
    # Opcional: Warm-up continuo
    # await warmup_system.continuous_warmup()

if __name__ == "__main__":
    asyncio.run(main())
