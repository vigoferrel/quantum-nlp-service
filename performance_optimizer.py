#!/usr/bin/env python3
"""
🚀 Optimizador de Rendimiento para Sistema Multimodal VIGOLEONROCKS
Implementa caching inteligente, gestión de memoria y lazy loading optimizado
"""

import asyncio
import sys
import time
import logging
import gc
import threading
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from functools import wraps, lru_cache
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import weakref
import psutil
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Métricas de rendimiento del sistema"""
    models_loaded: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    total_inferences: int = 0
    average_response_time: float = 0.0
    last_cleanup: datetime = field(default_factory=datetime.now)
    optimizations_applied: List[str] = field(default_factory=list)

@dataclass 
class CacheEntry:
    """Entrada de cache con metadatos"""
    data: Any
    timestamp: datetime
    access_count: int = 0
    size_bytes: int = 0
    ttl_seconds: int = 3600  # 1 hora por defecto

class IntelligentCache:
    """Sistema de cache inteligente con TTL y gestión de memoria"""
    
    def __init__(self, max_size_mb: int = 500, default_ttl: int = 3600):
        self.max_size_mb = max_size_mb
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._size_bytes = 0
        
        # Métricas
        self.hits = 0
        self.misses = 0
        
        # Iniciar limpieza automática
        self._cleanup_thread = threading.Thread(target=self._background_cleanup, daemon=True)
        self._cleanup_thread.start()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor del cache"""
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            
            entry = self._cache[key]
            
            # Verificar TTL
            if datetime.now() - entry.timestamp > timedelta(seconds=entry.ttl_seconds):
                self._remove_entry(key)
                self.misses += 1
                return None
            
            # Actualizar estadísticas de acceso
            entry.access_count += 1
            self.hits += 1
            
            return entry.data
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Guarda valor en cache"""
        with self._lock:
            ttl = ttl_seconds or self.default_ttl
            
            # Calcular tamaño aproximado
            size_bytes = sys.getsizeof(value)
            
            # Verificar límites de memoria
            if self._size_bytes + size_bytes > self.max_size_mb * 1024 * 1024:
                self._evict_lru()
            
            # Crear entrada
            entry = CacheEntry(
                data=value,
                timestamp=datetime.now(),
                size_bytes=size_bytes,
                ttl_seconds=ttl
            )
            
            # Remover entrada anterior si existe
            if key in self._cache:
                self._remove_entry(key)
            
            # Agregar nueva entrada
            self._cache[key] = entry
            self._size_bytes += size_bytes
            
            return True
    
    def _remove_entry(self, key: str) -> None:
        """Remueve entrada del cache"""
        if key in self._cache:
            entry = self._cache.pop(key)
            self._size_bytes -= entry.size_bytes
    
    def _evict_lru(self) -> None:
        """Elimina entradas menos usadas recientemente"""
        if not self._cache:
            return
        
        # Ordenar por access_count y timestamp
        sorted_entries = sorted(
            self._cache.items(),
            key=lambda x: (x[1].access_count, x[1].timestamp)
        )
        
        # Eliminar 25% de las entradas menos usadas
        to_remove = max(1, len(sorted_entries) // 4)
        
        for key, _ in sorted_entries[:to_remove]:
            self._remove_entry(key)
        
        logger.info(f"📦 Cache LRU: eliminadas {to_remove} entradas")
    
    def _background_cleanup(self) -> None:
        """Limpieza automática en segundo plano"""
        while True:
            try:
                time.sleep(300)  # Cada 5 minutos
                self.cleanup_expired()
            except Exception as e:
                logger.error(f"Error en limpieza de cache: {e}")
    
    def cleanup_expired(self) -> int:
        """Limpia entradas expiradas"""
        with self._lock:
            now = datetime.now()
            expired_keys = []
            
            for key, entry in self._cache.items():
                if now - entry.timestamp > timedelta(seconds=entry.ttl_seconds):
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_entry(key)
            
            if expired_keys:
                logger.info(f"🧹 Cache cleanup: {len(expired_keys)} entradas expiradas eliminadas")
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        with self._lock:
            hit_rate = self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
            
            return {
                "entries": len(self._cache),
                "size_mb": self._size_bytes / (1024 * 1024),
                "max_size_mb": self.max_size_mb,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate,
                "memory_usage_percent": (self._size_bytes / (self.max_size_mb * 1024 * 1024)) * 100
            }

class PerformanceOptimizer:
    """Optimizador principal del sistema multimodal"""
    
    def __init__(self):
        self.cache = IntelligentCache(max_size_mb=500)
        self.metrics = PerformanceMetrics()
        self._optimization_lock = threading.Lock()
        self._rate_limiter = {}  # Rate limiting por IP/usuario
        
        # Monitoreo de sistema
        self._monitoring_thread = threading.Thread(target=self._system_monitoring, daemon=True)
        self._monitoring_thread.start()
        
        logger.info("🚀 PerformanceOptimizer inicializado")
    
    def cached_model_inference(self, cache_ttl: int = 3600):
        """Decorador para cachear inferencias de modelos"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generar clave de cache basada en argumentos
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)
                
                # Intentar obtener del cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"💾 Cache hit para {func.__name__}")
                    return cached_result
                
                # Ejecutar función original
                start_time = time.time()
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Guardar en cache si la ejecución fue exitosa
                if result and not hasattr(result, 'error'):
                    self.cache.set(cache_key, result, ttl_seconds=cache_ttl)
                    logger.debug(f"💾 Resultado cacheado para {func.__name__}")
                
                # Actualizar métricas
                self.metrics.total_inferences += 1
                self._update_response_time(execution_time)
                
                return result
            return wrapper
        return decorator
    
    def rate_limit(self, requests_per_minute: int = 60):
        """Decorador para rate limiting"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Obtener identificador (IP, usuario, etc.)
                identifier = self._get_request_identifier(kwargs)
                
                if not self._check_rate_limit(identifier, requests_per_minute):
                    raise Exception(f"Rate limit exceeded: {requests_per_minute} requests per minute")
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Genera clave única para cache basada en función y argumentos"""
        # Crear string determinista de argumentos
        key_data = f"{func_name}:{str(args)}:{sorted(kwargs.items())}"
        
        # Hash para clave más corta y consistente
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_request_identifier(self, kwargs: dict) -> str:
        """Obtiene identificador único para rate limiting"""
        # Intentar obtener IP del request
        if 'request' in kwargs:
            return kwargs['request'].remote_addr
        
        # Fallback a identificador genérico
        return "default"
    
    def _check_rate_limit(self, identifier: str, limit: int) -> bool:
        """Verifica rate limiting"""
        now = time.time()
        minute_window = int(now // 60)
        
        key = f"{identifier}:{minute_window}"
        
        if key not in self._rate_limiter:
            self._rate_limiter[key] = 0
        
        if self._rate_limiter[key] >= limit:
            return False
        
        self._rate_limiter[key] += 1
        
        # Limpiar entradas antiguas
        old_keys = [k for k in self._rate_limiter.keys() 
                   if int(k.split(':')[1]) < minute_window - 2]
        for old_key in old_keys:
            del self._rate_limiter[old_key]
        
        return True
    
    def _update_response_time(self, execution_time: float) -> None:
        """Actualiza tiempo promedio de respuesta"""
        if self.metrics.total_inferences == 1:
            self.metrics.average_response_time = execution_time
        else:
            # Media móvil simple
            self.metrics.average_response_time = (
                (self.metrics.average_response_time * (self.metrics.total_inferences - 1) + execution_time) 
                / self.metrics.total_inferences
            )
    
    def _system_monitoring(self) -> None:
        """Monitoreo continuo del sistema"""
        while True:
            try:
                # Actualizar métricas de sistema
                self.metrics.memory_usage_mb = psutil.virtual_memory().used / (1024 * 1024)
                self.metrics.cpu_usage_percent = psutil.cpu_percent(interval=1)
                
                # Verificar si necesitamos optimizaciones
                self._check_optimization_needs()
                
                time.sleep(30)  # Cada 30 segundos
                
            except Exception as e:
                logger.error(f"Error en monitoreo de sistema: {e}")
                time.sleep(60)
    
    def _check_optimization_needs(self) -> None:
        """Verifica si se necesitan optimizaciones automáticas"""
        with self._optimization_lock:
            optimizations_applied = []
            
            # Si uso de memoria es alto, forzar limpieza
            if self.metrics.memory_usage_mb > 4000:  # 4GB
                gc.collect()
                optimizations_applied.append("memory_cleanup")
            
            # Si CPU está alto, reducir TTL del cache
            if self.metrics.cpu_usage_percent > 80:
                self.cache.default_ttl = max(300, self.cache.default_ttl - 300)
                optimizations_applied.append("reduce_cache_ttl")
            elif self.metrics.cpu_usage_percent < 30:
                self.cache.default_ttl = min(3600, self.cache.default_ttl + 300)
            
            # Si cache está lleno, forzar limpieza
            cache_stats = self.cache.get_stats()
            if cache_stats["memory_usage_percent"] > 90:
                self.cache._evict_lru()
                optimizations_applied.append("cache_eviction")
            
            if optimizations_applied:
                self.metrics.optimizations_applied.extend(optimizations_applied)
                logger.info(f"🔧 Optimizaciones aplicadas: {optimizations_applied}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Genera reporte completo de rendimiento"""
        cache_stats = self.cache.get_stats()
        
        return {
            "system_metrics": {
                "memory_usage_mb": self.metrics.memory_usage_mb,
                "cpu_usage_percent": self.metrics.cpu_usage_percent,
                "models_loaded": self.metrics.models_loaded,
                "total_inferences": self.metrics.total_inferences,
                "average_response_time": round(self.metrics.average_response_time, 3)
            },
            "cache_performance": cache_stats,
            "optimizations": {
                "applied_count": len(self.metrics.optimizations_applied),
                "recent_optimizations": self.metrics.optimizations_applied[-5:],
                "last_cleanup": self.metrics.last_cleanup.isoformat()
            },
            "recommendations": self._generate_recommendations(cache_stats)
        }
    
    def _generate_recommendations(self, cache_stats: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones de optimización"""
        recommendations = []
        
        # Recomendaciones basadas en cache
        if cache_stats["hit_rate"] < 0.5:
            recommendations.append("Considerar aumentar TTL del cache para mejorar hit rate")
        
        if cache_stats["memory_usage_percent"] > 85:
            recommendations.append("Considerar aumentar el tamaño máximo del cache")
        
        # Recomendaciones basadas en sistema
        if self.metrics.cpu_usage_percent > 70:
            recommendations.append("CPU alto - considerar optimizar algoritmos o usar más cores")
        
        if self.metrics.memory_usage_mb > 3000:
            recommendations.append("Memoria alta - implementar cleanup más agresivo")
        
        if self.metrics.average_response_time > 5.0:
            recommendations.append("Tiempo de respuesta alto - revisar caching y lazy loading")
        
        return recommendations

# Instancia global del optimizador
performance_optimizer = PerformanceOptimizer()

def optimize_multimodal_manager():
    """Aplica optimizaciones al MultimodalAIManager existente"""
    try:
        from multimodal_ai_manager import get_multimodal_manager
        manager = get_multimodal_manager()
        
        # Aplicar decorador de cache a métodos críticos
        original_analyze_image = manager.analyze_image
        manager.analyze_image = performance_optimizer.cached_model_inference(cache_ttl=1800)(original_analyze_image)
        
        if hasattr(manager, 'transcribe_audio'):
            original_transcribe_audio = manager.transcribe_audio
            manager.transcribe_audio = performance_optimizer.cached_model_inference(cache_ttl=3600)(original_transcribe_audio)
        
        logger.info("✅ Optimizaciones aplicadas al MultimodalAIManager")
        performance_optimizer.metrics.optimizations_applied.append("multimodal_caching")
        
        return True
        
    except Exception as e:
        logger.error(f"Error aplicando optimizaciones: {e}")
        return False

if __name__ == "__main__":
    # Test del optimizador
    print("🧪 Probando PerformanceOptimizer...")
    
    # Aplicar optimizaciones
    success = optimize_multimodal_manager()
    if success:
        print("✅ Optimizaciones aplicadas exitosamente")
    
    # Mostrar reporte
    report = performance_optimizer.get_performance_report()
    print("\n📊 Reporte de Rendimiento:")
    print(f"  - Memoria: {report['system_metrics']['memory_usage_mb']:.1f} MB")
    print(f"  - CPU: {report['system_metrics']['cpu_usage_percent']:.1f}%")
    print(f"  - Cache Hit Rate: {report['cache_performance']['hit_rate']:.2f}")
    
    if report['recommendations']:
        print("\n💡 Recomendaciones:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
    
    print("\n🚀 PerformanceOptimizer listo para producción!")
