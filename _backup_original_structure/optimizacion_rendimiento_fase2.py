#!/usr/bin/env python3
"""
🚀 OPTIMIZACIÓN DE RENDIMIENTO - FASE 2
========================================
Sistema de optimización avanzada para mejorar tiempo de respuesta
"""

import asyncio
import time
import json
import traceback
from typing import Dict, Any, Optional
import threading
from concurrent.futures import ThreadPoolExecutor
import psutil
import gc

def optimizar_procesamiento_asincrono():
    """Optimizar el procesamiento asíncrono del motor conversacional"""
    print("⚡ OPTIMIZANDO PROCESAMIENTO ASÍNCRONO")
    print("=" * 50)
    
    # Leer el archivo del motor conversacional
    with open('advanced_conversational_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Optimización 1: Procesamiento paralelo de NLP y Quantum
    old_process_text = '''        elif content.media_type == MediaType.TEXT:
            # Procesar texto con NLP avanzado y núcleo cuántico
            text_content = content.content if isinstance(content.content, str) else ""
            
            # Análisis NLP completo
            nlp_features = await nlp_engine.analyze_text(text_content)
            content.nlp_features = nlp_features
            
            # 🧠 PROCESAMIENTO CUÁNTICO AVANZADO
            quantum_prompt = await self._create_quantum_prompt(text_content, nlp_features)
            quantum_result = await self.quantum_core.test_quantum_enhancement(text_content, "general")
            
            # Guardar resultado cuántico en el contenido
            content.quantum_features = quantum_result
            
            # Detectar idioma
            language = await nlp_engine.detect_language(text_content)
            
            # Extraer resumen
            summary = await nlp_engine.extract_summary(text_content)'''
    
    new_process_text = '''        elif content.media_type == MediaType.TEXT:
            # Procesar texto con NLP avanzado y núcleo cuántico - OPTIMIZADO
            text_content = content.content if isinstance(content.content, str) else ""
            
            # 🚀 PROCESAMIENTO PARALELO: NLP + Quantum simultáneamente
            async def process_nlp():
                return await nlp_engine.analyze_text(text_content)
            
            async def process_quantum():
                return await self.quantum_core.test_quantum_enhancement(text_content, "general")
            
            async def process_language():
                return await nlp_engine.detect_language(text_content)
            
            async def process_summary():
                return await nlp_engine.extract_summary(text_content)
            
            # Ejecutar todas las tareas en paralelo
            nlp_task = asyncio.create_task(process_nlp())
            quantum_task = asyncio.create_task(process_quantum())
            language_task = asyncio.create_task(process_language())
            summary_task = asyncio.create_task(process_summary())
            
            # Esperar todas las tareas completadas
            nlp_features, quantum_result, language, summary = await asyncio.gather(
                nlp_task, quantum_task, language_task, summary_task
            )
            
            # Guardar resultados
            content.nlp_features = nlp_features
            content.quantum_features = quantum_result'''
    
    content = content.replace(old_process_text, new_process_text)
    
    # Optimización 2: Cache inteligente con TTL
    cache_optimization = '''        # 🚀 CACHE Y OPTIMIZACIONES
        self._content_cache = {}
        self._nlp_cache = {}
        self._quantum_cache = {}
        
        logger.info("🚀 Motor conversacional avanzado con núcleo cuántico inicializado")'''
    
    cache_optimization_advanced = '''        # 🚀 CACHE Y OPTIMIZACIONES AVANZADAS
        self._content_cache = {}
        self._nlp_cache = {}
        self._quantum_cache = {}
        self._cache_ttl = 300  # 5 minutos TTL
        self._cache_timestamps = {}
        self._max_cache_size = 1000
        
        # Thread pool para operaciones pesadas
        self._thread_pool = ThreadPoolExecutor(max_workers=4)
        
        # Métricas de rendimiento
        self._performance_metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_response_time": 0.0,
            "total_response_time": 0.0
        }
        
        logger.info("🚀 Motor conversacional avanzado con núcleo cuántico optimizado inicializado")'''
    
    content = content.replace(cache_optimization, cache_optimization_advanced)
    
    # Optimización 3: Limpieza automática de cache
    cache_cleanup = '''    @lru_cache(maxsize=1000)
    def _get_cache_key(self, content_hash: str, media_type: str) -> str:
        """Generar clave de cache"""
        return f"{content_hash}_{media_type}"'''
    
    cache_cleanup_advanced = '''    def _get_cache_key(self, content_hash: str, media_type: str) -> str:
        """Generar clave de cache optimizada"""
        return f"{content_hash}_{media_type}"
    
    def _cleanup_cache(self):
        """Limpieza automática de cache expirado"""
        current_time = time.time()
        expired_keys = []
        
        for key, timestamp in self._cache_timestamps.items():
            if current_time - timestamp > self._cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            self._content_cache.pop(key, None)
            self._nlp_cache.pop(key, None)
            self._quantum_cache.pop(key, None)
            self._cache_timestamps.pop(key, None)
        
        # Limitar tamaño del cache
        if len(self._content_cache) > self._max_cache_size:
            # Eliminar elementos más antiguos
            sorted_keys = sorted(self._cache_timestamps.items(), key=lambda x: x[1])
            keys_to_remove = [k for k, _ in sorted_keys[:len(sorted_keys)//2]]
            
            for key in keys_to_remove:
                self._content_cache.pop(key, None)
                self._nlp_cache.pop(key, None)
                self._quantum_cache.pop(key, None)
                self._cache_timestamps.pop(key, None)
        
        # Forzar garbage collection
        gc.collect()'''
    
    content = content.replace(cache_cleanup, cache_cleanup_advanced)
    
    # Guardar archivo optimizado
    with open('advanced_conversational_engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Procesamiento asíncrono optimizado")

def optimizar_carga_modelos():
    """Optimizar la carga de modelos NLP"""
    print("\n🧠 OPTIMIZANDO CARGA DE MODELOS NLP")
    print("=" * 50)
    
    # Leer el archivo del motor NLP
    with open('advanced_nlp_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Optimización 1: Lazy loading de modelos
    lazy_loading = '''class AdvancedNLPEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧠 Inicializando motor NLP avanzado...")
        
        # Inicializar modelos
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.nlp = spacy.load("en_core_web_sm")
        self.transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Configurar NLTK
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        self.logger.info("🧠 Motor NLP avanzado inicializado correctamente")'''
    
    lazy_loading_optimized = '''class AdvancedNLPEngine:
    def __init__(self):
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
        
        self.logger.info("🧠 Motor NLP avanzado inicializado correctamente")
    
    def _load_models_if_needed(self):
        """Cargar modelos solo cuando se necesiten"""
        if not self._models_loaded:
            self.logger.info("🔄 Cargando modelos NLP...")
            self._sentiment_analyzer = SentimentIntensityAnalyzer()
            self._nlp = spacy.load("en_core_web_sm")
            self._transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
            self._models_loaded = True
            self.logger.info("✅ Modelos NLP cargados")
    
    @property
    def sentiment_analyzer(self):
        self._load_models_if_needed()
        return self._sentiment_analyzer
    
    @property
    def nlp(self):
        self._load_models_if_needed()
        return self._nlp
    
    @property
    def transformer_model(self):
        self._load_models_if_needed()
        return self._transformer_model'''
    
    content = content.replace(lazy_loading, lazy_loading_optimized)
    
    # Guardar archivo optimizado
    with open('advanced_nlp_engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Carga de modelos optimizada")

def crear_sistema_monitoreo_avanzado():
    """Crear sistema de monitoreo avanzado"""
    print("\n📊 CREANDO SISTEMA DE MONITOREO AVANZADO")
    print("=" * 50)
    
    monitoring_advanced = '''#!/usr/bin/env python3
"""
📊 SISTEMA DE MONITOREO AVANZADO - FASE 2
=========================================
Monitor de rendimiento avanzado con métricas en tiempo real
"""

import time
import psutil
import json
import threading
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
import requests
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

class AdvancedPerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "response_times": deque(maxlen=1000),
            "memory_usage": deque(maxlen=500),
            "cpu_usage": deque(maxlen=500),
            "requests_count": 0,
            "errors_count": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "start_time": time.time(),
            "endpoints": {},
            "alerts": []
        }
        self.lock = threading.Lock()
        self.alert_thresholds = {
            "response_time": 10.0,  # segundos
            "memory_usage": 80.0,   # porcentaje
            "cpu_usage": 90.0,      # porcentaje
            "error_rate": 5.0       # porcentaje
        }
    
    def record_request(self, endpoint: str, response_time: float, success: bool, 
                      cache_hit: bool = False, error_type: str = None):
        """Registrar métrica de request avanzada"""
        with self.lock:
            self.metrics["response_times"].append(response_time)
            self.metrics["requests_count"] += 1
            
            if not success:
                self.metrics["errors_count"] += 1
            
            if cache_hit:
                self.metrics["cache_hits"] += 1
            else:
                self.metrics["cache_misses"] += 1
            
            # Registrar por endpoint
            if endpoint not in self.metrics["endpoints"]:
                self.metrics["endpoints"][endpoint] = {
                    "count": 0,
                    "avg_time": 0.0,
                    "errors": 0,
                    "cache_hits": 0
                }
            
            endpoint_data = self.metrics["endpoints"][endpoint]
            endpoint_data["count"] += 1
            endpoint_data["avg_time"] = (
                (endpoint_data["avg_time"] * (endpoint_data["count"] - 1) + response_time) 
                / endpoint_data["count"]
            )
            
            if not success:
                endpoint_data["errors"] += 1
            
            if cache_hit:
                endpoint_data["cache_hits"] += 1
            
            # Verificar alertas
            self._check_alerts(endpoint, response_time, success, error_type)
    
    def _check_alerts(self, endpoint: str, response_time: float, success: bool, error_type: str):
        """Verificar y generar alertas"""
        current_time = datetime.now()
        
        # Alerta por tiempo de respuesta alto
        if response_time > self.alert_thresholds["response_time"]:
            alert = {
                "type": "HIGH_RESPONSE_TIME",
                "endpoint": endpoint,
                "value": response_time,
                "threshold": self.alert_thresholds["response_time"],
                "timestamp": current_time.isoformat(),
                "severity": "WARNING"
            }
            self.metrics["alerts"].append(alert)
        
        # Alerta por error
        if not success:
            alert = {
                "type": "ERROR",
                "endpoint": endpoint,
                "error_type": error_type,
                "timestamp": current_time.isoformat(),
                "severity": "ERROR"
            }
            self.metrics["alerts"].append(alert)
    
    def record_system_metrics(self):
        """Registrar métricas del sistema"""
        with self.lock:
            memory_percent = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent()
            
            self.metrics["memory_usage"].append(memory_percent)
            self.metrics["cpu_usage"].append(cpu_percent)
            
            # Verificar alertas del sistema
            if memory_percent > self.alert_thresholds["memory_usage"]:
                alert = {
                    "type": "HIGH_MEMORY_USAGE",
                    "value": memory_percent,
                    "threshold": self.alert_thresholds["memory_usage"],
                    "timestamp": datetime.now().isoformat(),
                    "severity": "WARNING"
                }
                self.metrics["alerts"].append(alert)
            
            if cpu_percent > self.alert_thresholds["cpu_usage"]:
                alert = {
                    "type": "HIGH_CPU_USAGE",
                    "value": cpu_percent,
                    "threshold": self.alert_thresholds["cpu_usage"],
                    "timestamp": datetime.now().isoformat(),
                    "severity": "WARNING"
                }
                self.metrics["alerts"].append(alert)
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas detalladas"""
        with self.lock:
            response_times = list(self.metrics["response_times"])
            memory_usage = list(self.metrics["memory_usage"])
            cpu_usage = list(self.metrics["cpu_usage"])
            
            # Calcular métricas avanzadas
            error_rate = (self.metrics["errors_count"] / max(self.metrics["requests_count"], 1)) * 100
            cache_hit_rate = (self.metrics["cache_hits"] / max(self.metrics["cache_hits"] + self.metrics["cache_misses"], 1)) * 100
            
            return {
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.metrics["start_time"],
                "requests": {
                    "total": self.metrics["requests_count"],
                    "errors": self.metrics["errors_count"],
                    "success_rate": 100 - error_rate,
                    "error_rate": error_rate
                },
                "performance": {
                    "avg_response_time": np.mean(response_times) if response_times else 0,
                    "min_response_time": np.min(response_times) if response_times else 0,
                    "max_response_time": np.max(response_times) if response_times else 0,
                    "p95_response_time": np.percentile(response_times, 95) if response_times else 0,
                    "p99_response_time": np.percentile(response_times, 99) if response_times else 0,
                    "avg_memory_usage": np.mean(memory_usage) if memory_usage else 0,
                    "avg_cpu_usage": np.mean(cpu_usage) if cpu_usage else 0
                },
                "cache": {
                    "hits": self.metrics["cache_hits"],
                    "misses": self.metrics["cache_misses"],
                    "hit_rate": cache_hit_rate
                },
                "endpoints": self.metrics["endpoints"],
                "alerts": self.metrics["alerts"][-10:],  # Últimas 10 alertas
                "system": {
                    "memory_available": psutil.virtual_memory().available,
                    "memory_total": psutil.virtual_memory().total,
                    "cpu_count": psutil.cpu_count(),
                    "disk_usage": psutil.disk_usage('/').percent
                }
            }
    
    def generate_performance_report(self) -> str:
        """Generar reporte de rendimiento"""
        stats = self.get_detailed_stats()
        
        report = f"""
📊 REPORTE DE RENDIMIENTO AVANZADO
==================================
⏰ Timestamp: {stats['timestamp']}
⏱️ Uptime: {stats['uptime']:.2f} segundos

📈 MÉTRICAS DE REQUESTS:
   Total: {stats['requests']['total']}
   Éxitos: {stats['requests']['total'] - stats['requests']['errors']}
   Errores: {stats['requests']['errors']}
   Tasa de éxito: {stats['requests']['success_rate']:.2f}%

⚡ RENDIMIENTO:
   Tiempo promedio: {stats['performance']['avg_response_time']:.3f}s
   Tiempo mínimo: {stats['performance']['min_response_time']:.3f}s
   Tiempo máximo: {stats['performance']['max_response_time']:.3f}s
   P95: {stats['performance']['p95_response_time']:.3f}s
   P99: {stats['performance']['p99_response_time']:.3f}s

🧠 SISTEMA:
   CPU promedio: {stats['performance']['avg_cpu_usage']:.2f}%
   Memoria promedio: {stats['performance']['avg_memory_usage']:.2f}%
   Memoria disponible: {stats['system']['memory_available'] / 1024**3:.2f} GB

🔄 CACHE:
   Hits: {stats['cache']['hits']}
   Misses: {stats['cache']['misses']}
   Hit rate: {stats['cache']['hit_rate']:.2f}%

🚨 ALERTAS RECIENTES: {len(stats['alerts'])}
"""
        
        return report
    
    def start_monitoring(self):
        """Iniciar monitoreo en background"""
        def monitor_loop():
            while True:
                self.record_system_metrics()
                time.sleep(2)  # Registrar cada 2 segundos
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        print("📊 Monitoreo avanzado iniciado en background")

# Instancia global del monitor avanzado
advanced_monitor = AdvancedPerformanceMonitor()

def test_advanced_monitoring():
    """Probar el sistema de monitoreo avanzado"""
    print("🧪 PROBANDO SISTEMA DE MONITOREO AVANZADO")
    print("=" * 50)
    
    # Iniciar monitoreo
    advanced_monitor.start_monitoring()
    
    # Simular requests
    for i in range(10):
        time.sleep(0.5)
        response_time = 1.0 + i * 0.2
        success = i < 8  # 80% éxito
        cache_hit = i % 3 == 0  # 33% cache hits
        
        advanced_monitor.record_request(
            endpoint=f"/api/test_{i % 3}",
            response_time=response_time,
            success=success,
            cache_hit=cache_hit,
            error_type="timeout" if not success else None
        )
        print(f"Request {i+1} registrado")
    
    # Generar reporte
    report = advanced_monitor.generate_performance_report()
    print(report)
    
    # Obtener estadísticas detalladas
    stats = advanced_monitor.get_detailed_stats()
    print("📊 Estadísticas detalladas:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_advanced_monitoring()
'''
    
    with open('advanced_performance_monitor.py', 'w', encoding='utf-8') as f:
        f.write(monitoring_advanced)
    
    print("✅ Sistema de monitoreo avanzado creado")

def crear_dashboard_monitoreo():
    """Crear dashboard de monitoreo web"""
    print("\n🌐 CREANDO DASHBOARD DE MONITOREO")
    print("=" * 50)
    
    dashboard_code = '''#!/usr/bin/env python3
"""
🌐 DASHBOARD DE MONITOREO WEB
=============================
Dashboard en tiempo real para monitorear el sistema
"""

from flask import Flask, render_template_string, jsonify
import json
import time
from datetime import datetime
from advanced_performance_monitor import advanced_monitor

app = Flask(__name__)

# HTML template para el dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Dashboard de Monitoreo - Sistema Avanzado</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .metric-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-subtitle {
            font-size: 14px;
            opacity: 0.8;
        }
        .alerts-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .alert-item {
            background: rgba(255, 0, 0, 0.2);
            border-left: 4px solid #ff4444;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online { background: #4CAF50; }
        .status-warning { background: #ff9800; }
        .status-error { background: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Dashboard de Monitoreo - Sistema Avanzado</h1>
            <p>Monitoreo en tiempo real del sistema NLP + Quantum</p>
            <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">🚀 Rendimiento</div>
                <div class="metric-value" id="avg-response-time">--</div>
                <div class="metric-subtitle">Tiempo promedio de respuesta</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📈 Requests</div>
                <div class="metric-value" id="total-requests">--</div>
                <div class="metric-subtitle">Total de requests procesados</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">✅ Tasa de Éxito</div>
                <div class="metric-value" id="success-rate">--</div>
                <div class="metric-subtitle">Porcentaje de requests exitosos</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🧠 Cache</div>
                <div class="metric-value" id="cache-hit-rate">--</div>
                <div class="metric-subtitle">Tasa de aciertos en cache</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">💾 Memoria</div>
                <div class="metric-value" id="memory-usage">--</div>
                <div class="metric-subtitle">Uso de memoria del sistema</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">⚡ CPU</div>
                <div class="metric-value" id="cpu-usage">--</div>
                <div class="metric-subtitle">Uso de CPU del sistema</div>
            </div>
        </div>
        
        <div class="alerts-section">
            <h2>🚨 Alertas Recientes</h2>
            <div id="alerts-container">
                <p>Cargando alertas...</p>
            </div>
        </div>
    </div>
    
    <script>
        function updateMetrics() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('avg-response-time').textContent = data.performance.avg_response_time.toFixed(3) + 's';
                    document.getElementById('total-requests').textContent = data.requests.total;
                    document.getElementById('success-rate').textContent = data.requests.success_rate.toFixed(2) + '%';
                    document.getElementById('cache-hit-rate').textContent = data.cache.hit_rate.toFixed(2) + '%';
                    document.getElementById('memory-usage').textContent = data.performance.avg_memory_usage.toFixed(2) + '%';
                    document.getElementById('cpu-usage').textContent = data.performance.avg_cpu_usage.toFixed(2) + '%';
                    
                    // Actualizar alertas
                    const alertsContainer = document.getElementById('alerts-container');
                    if (data.alerts.length === 0) {
                        alertsContainer.innerHTML = '<p>✅ No hay alertas activas</p>';
                    } else {
                        alertsContainer.innerHTML = data.alerts.map(alert => `
                            <div class="alert-item">
                                <strong>${alert.type}</strong> - ${alert.timestamp}<br>
                                ${alert.endpoint ? 'Endpoint: ' + alert.endpoint : ''}
                                ${alert.value ? 'Valor: ' + alert.value : ''}
                            </div>
                        `).join('');
                    }
                })
                .catch(error => {
                    console.error('Error actualizando métricas:', error);
                });
        }
        
        // Actualizar cada 5 segundos
        setInterval(updateMetrics, 5000);
        updateMetrics(); // Actualizar inmediatamente
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/metrics')
def get_metrics():
    """API para obtener métricas en tiempo real"""
    stats = advanced_monitor.get_detailed_stats()
    return jsonify(stats)

@app.route('/api/health')
def health_check():
    """Health check del dashboard"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "monitor_active": True
    })

if __name__ == '__main__':
    print("🌐 Iniciando Dashboard de Monitoreo...")
    print("🔗 URL: http://localhost:5005")
    app.run(host='0.0.0.0', port=5005, debug=False)
'''
    
    with open('dashboard_monitoreo.py', 'w', encoding='utf-8') as f:
        f.write(dashboard_code)
    
    print("✅ Dashboard de monitoreo creado")

def main():
    """Función principal de optimización Fase 2"""
    print("🚀 OPTIMIZACIÓN DE RENDIMIENTO - FASE 2")
    print("=" * 60)
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Paso 1: Optimizar procesamiento asíncrono
        optimizar_procesamiento_asincrono()
        
        # Paso 2: Optimizar carga de modelos
        optimizar_carga_modelos()
        
        # Paso 3: Crear sistema de monitoreo avanzado
        crear_sistema_monitoreo_avanzado()
        
        # Paso 4: Crear dashboard de monitoreo
        crear_dashboard_monitoreo()
        
        print("\n" + "=" * 60)
        print("✅ FASE 2: OPTIMIZACIÓN DE RENDIMIENTO COMPLETADA")
        print("📋 Próximos pasos:")
        print("   1. Reiniciar servidor avanzado")
        print("   2. Ejecutar pruebas de rendimiento")
        print("   3. Iniciar dashboard de monitoreo")
        print("   4. Verificar mejoras en tiempo de respuesta")
        
    except Exception as e:
        print(f"❌ Error durante la optimización: {e}")
        print(f"📄 Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
