#!/usr/bin/env python3
"""
🚀 OPTIMIZACIÓN COLD START - FASE 2.5
======================================
Sistema para optimizar el tiempo del primer request
"""

import time
import json
import traceback
import asyncio

def optimizar_pre_warming():
    """Implementar pre-warming de modelos"""
    print("🔥 IMPLEMENTANDO PRE-WARMING DE MODELOS")
    print("=" * 50)
    
    # Leer el archivo del motor NLP
    with open('advanced_nlp_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Añadir pre-warming al constructor
    old_init = '''    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧠 Inicializando motor NLP avanzado...")
        
        # 🚀 LAZY LOADING: Modelos se cargan solo cuando se necesitan
        self._sentiment_analyzer = None
        self._nlp = None
        self._transformer_model = None
        self._models_loaded = False
        
        # Configurar NLTK
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        self.logger.info("🧠 Motor NLP avanzado inicializado correctamente")'''
    
    new_init = '''    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧠 Inicializando motor NLP avanzado...")
        
        # 🚀 LAZY LOADING: Modelos se cargan solo cuando se necesitan
        self._sentiment_analyzer = None
        self._nlp = None
        self._transformer_model = None
        self._models_loaded = False
        
        # Configurar NLTK
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        # 🔥 PRE-WARMING: Cargar modelos en background
        self._pre_warm_models()
        
        self.logger.info("🧠 Motor NLP avanzado inicializado correctamente")
    
    def _pre_warm_models(self):
        """Pre-warming de modelos en background"""
        try:
            self.logger.info("🔥 Iniciando pre-warming de modelos...")
            
            # Cargar modelos en background
            import threading
            def load_models():
                try:
                    self.logger.info("🔄 Cargando modelos NLP...")
                    self._sentiment_analyzer = SentimentIntensityAnalyzer()
                    self._nlp = spacy.load("en_core_web_sm")
                    self._transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
                    self._models_loaded = True
                    self.logger.info("✅ Pre-warming de modelos completado")
                except Exception as e:
                    self.logger.error(f"❌ Error en pre-warming: {e}")
            
            # Ejecutar en thread separado
            thread = threading.Thread(target=load_models, daemon=True)
            thread.start()
            
        except Exception as e:
            self.logger.error(f"❌ Error iniciando pre-warming: {e}")'''
    
    content = content.replace(old_init, new_init)
    
    # Guardar optimizado
    with open('advanced_nlp_engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Pre-warming de modelos implementado")

def optimizar_cache_persistente():
    """Implementar cache persistente"""
    print("\n💾 IMPLEMENTANDO CACHE PERSISTENTE")
    print("=" * 50)
    
    cache_code = '''#!/usr/bin/env python3
"""
💾 CACHE PERSISTENTE AVANZADO
=============================
Sistema de cache persistente para optimizar cold start
"""

import json
import time
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import hashlib

class PersistentCache:
    def __init__(self, cache_dir: str = "cache", max_size: int = 1000, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.ttl_hours = ttl_hours
        self.cache_file = os.path.join(cache_dir, "persistent_cache.pkl")
        self.metadata_file = os.path.join(cache_dir, "cache_metadata.json")
        
        # Crear directorio si no existe
        os.makedirs(cache_dir, exist_ok=True)
        
        # Cargar cache existente
        self.cache = self._load_cache()
        self.metadata = self._load_metadata()
        
        # Limpiar cache expirado al inicio
        self._cleanup_expired()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Cargar cache desde archivo"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            print(f"⚠️ Error cargando cache: {e}")
        return {}
    
    def _save_cache(self):
        """Guardar cache a archivo"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            print(f"⚠️ Error guardando cache: {e}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Cargar metadata del cache"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error cargando metadata: {e}")
        return {"created": datetime.now().isoformat(), "access_count": 0}
    
    def _save_metadata(self):
        """Guardar metadata del cache"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error guardando metadata: {e}")
    
    def _generate_key(self, data: Any) -> str:
        """Generar clave única para los datos"""
        if isinstance(data, str):
            content = data
        else:
            content = json.dumps(data, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cleanup_expired(self):
        """Limpiar entradas expiradas"""
        current_time = datetime.now()
        expired_keys = []
        
        for key, value in self.cache.items():
            if 'timestamp' in value:
                cache_time = datetime.fromisoformat(value['timestamp'])
                if current_time - cache_time > timedelta(hours=self.ttl_hours):
                    expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            print(f"🧹 Limpiadas {len(expired_keys)} entradas expiradas del cache")
            self._save_cache()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del cache"""
        if key in self.cache:
            value = self.cache[key]
            
            # Verificar si no ha expirado
            if 'timestamp' in value:
                cache_time = datetime.fromisoformat(value['timestamp'])
                if datetime.now() - cache_time > timedelta(hours=self.ttl_hours):
                    del self.cache[key]
                    self._save_cache()
                    return None
            
            # Actualizar metadata
            self.metadata["access_count"] += 1
            self._save_metadata()
            
            return value.get('data')
        return None
    
    def set(self, key: str, data: Any, ttl_hours: Optional[int] = None):
        """Guardar valor en cache"""
        # Limpiar cache si está lleno
        if len(self.cache) >= self.max_size:
            self._cleanup_oldest()
        
        # Guardar con timestamp
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'ttl_hours': ttl_hours or self.ttl_hours
        }
        
        self._save_cache()
    
    def _cleanup_oldest(self):
        """Limpiar entradas más antiguas"""
        if not self.cache:
            return
        
        # Ordenar por timestamp
        sorted_items = sorted(
            self.cache.items(),
            key=lambda x: x[1].get('timestamp', ''),
            reverse=True
        )
        
        # Mantener solo la mitad más reciente
        keep_count = self.max_size // 2
        self.cache = dict(sorted_items[:keep_count])
        
        print(f"🧹 Cache limpiado: {keep_count} entradas mantenidas")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "access_count": self.metadata.get("access_count", 0),
            "created": self.metadata.get("created"),
            "cache_file_size": os.path.getsize(self.cache_file) if os.path.exists(self.cache_file) else 0
        }
    
    def clear(self):
        """Limpiar todo el cache"""
        self.cache = {}
        self._save_cache()
        print("🗑️ Cache completamente limpiado")

# Instancia global
persistent_cache = PersistentCache()

def test_persistent_cache():
    """Probar el cache persistente"""
    print("🧪 Probando cache persistente...")
    
    # Test 1: Guardar y recuperar
    test_data = {"text": "Hola mundo", "nlp_result": {"sentiment": "positive"}}
    key = persistent_cache._generate_key(test_data)
    
    persistent_cache.set(key, test_data)
    retrieved = persistent_cache.get(key)
    
    print(f"✅ Cache test: {retrieved == test_data}")
    
    # Test 2: Estadísticas
    stats = persistent_cache.get_stats()
    print(f"📊 Cache stats: {stats}")
    
    return persistent_cache

if __name__ == "__main__":
    test_persistent_cache()
'''
    
    with open('persistent_cache.py', 'w', encoding='utf-8') as f:
        f.write(cache_code)
    
    print("✅ Cache persistente implementado")

def optimizar_health_check():
    """Implementar health check con warm-up"""
    print("\n🏥 IMPLEMENTANDO HEALTH CHECK CON WARM-UP")
    print("=" * 50)
    
    # Leer el archivo del servidor
    with open('advanced_multimodal_server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Añadir health check optimizado
    health_check_code = '''@app.get("/health")
async def health_check():
    """Health check con warm-up automático"""
    try:
        # Verificar estado básico
        basic_health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time() - start_time,
            "version": "2.5.0"
        }
        
        # Verificar modelos NLP
        try:
            nlp_ready = engine.nlp_engine._models_loaded
            basic_health["nlp_models"] = "ready" if nlp_ready else "loading"
        except:
            basic_health["nlp_models"] = "error"
        
        # Verificar quantum core
        try:
            quantum_ready = hasattr(engine.quantum_core, 'test_quantum_enhancement')
            basic_health["quantum_core"] = "ready" if quantum_ready else "error"
        except:
            basic_health["quantum_core"] = "error"
        
        # Warm-up automático si es necesario
        if not nlp_ready:
            basic_health["warmup"] = "triggered"
            # Trigger warm-up en background
            asyncio.create_task(engine.nlp_engine._load_models_if_needed())
        
        return basic_health
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }'''
    
    # Buscar el health check existente y reemplazarlo
    if '@app.get("/health")' in content:
        # Extraer el health check existente
        start_marker = '@app.get("/health")'
        end_marker = 'return {"status": "healthy"}'
        
        old_health = content[content.find(start_marker):content.find(end_marker) + len(end_marker)]
        content = content.replace(old_health, health_check_code)
    else:
        # Añadir antes del if __name__ == '__main__':
        content = content.replace('if __name__ == "__main__":', health_check_code + '\n\nif __name__ == "__main__":')
    
    # Guardar optimizado
    with open('advanced_multimodal_server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Health check optimizado implementado")

def crear_sistema_warmup():
    """Crear sistema de warm-up automático"""
    print("\n🔥 CREANDO SISTEMA DE WARM-UP AUTOMÁTICO")
    print("=" * 50)
    
    warmup_code = '''#!/usr/bin/env python3
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
'''
    
    with open('warmup_system.py', 'w', encoding='utf-8') as f:
        f.write(warmup_code)
    
    print("✅ Sistema de warm-up automático creado")

def main():
    """Función principal de optimización Fase 2.5"""
    print("🚀 OPTIMIZACIÓN COLD START - FASE 2.5")
    print("=" * 60)
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Paso 1: Pre-warming de modelos
        optimizar_pre_warming()
        
        # Paso 2: Cache persistente
        optimizar_cache_persistente()
        
        # Paso 3: Health check optimizado
        optimizar_health_check()
        
        # Paso 4: Sistema de warm-up
        crear_sistema_warmup()
        
        print("\n" + "=" * 60)
        print("✅ FASE 2.5: OPTIMIZACIÓN COLD START COMPLETADA")
        print("📋 Próximos pasos:")
        print("   1. Reiniciar servidor")
        print("   2. Ejecutar warm-up automático")
        print("   3. Probar cold start optimizado")
        print("   4. Verificar mejoras en tiempo de respuesta")
        
    except Exception as e:
        print(f"❌ Error durante la optimización: {e}")
        print(f"📄 Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
