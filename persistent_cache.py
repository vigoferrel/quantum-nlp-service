#!/usr/bin/env python3
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
