#!/usr/bin/env python3
"""
QUANTUM EDGE SERVER - Servidor Flask para el Sistema de Edge Cuántico
Exponer el Quantum Edge Maximizer como API REST
"""

from flask import Flask, request, jsonify
import asyncio
import json
import time
import logging
from typing import Dict, Any
import threading

from quantum_edge_maximizer import QuantumEdgeMaximizer

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("QuantumEdgeServer")

app = Flask(__name__)

# Instancia global del Quantum Edge Maximizer
quantum_edge_maximizer = None

def initialize_quantum_system():
    """Inicializa el sistema cuántico en un hilo separado"""
    global quantum_edge_maximizer
    
    async def init_system():
        quantum_edge_maximizer = QuantumEdgeMaximizer()
        logger.info("🚀 Quantum Edge Maximizer inicializado en servidor")
    
    # Ejecutar en loop de eventos
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_system())
    loop.close()

# Inicializar sistema al arrancar
init_thread = threading.Thread(target=initialize_quantum_system)
init_thread.start()
init_thread.join()

@app.route('/')
def home():
    """Página principal del servidor"""
    return jsonify({
        "system": "Quantum Edge Maximizer Server",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/": "Información del sistema",
            "/api/status": "Estado del sistema cuántico",
            "/api/process": "Procesar consulta con edge máximo",
            "/api/models": "Lista de modelos disponibles",
            "/api/health": "Estado de salud del sistema"
        }
    })

@app.route('/api/status')
def get_status():
    """Obtener estado del sistema cuántico"""
    if quantum_edge_maximizer is None:
        return jsonify({
            "status": "initializing",
            "message": "Sistema cuántico en inicialización"
        }), 503
    
    return jsonify({
        "status": "active",
        "system": "Quantum Edge Maximizer",
        "quantum_components": {
            "edge_maximizer": "active",
            "entanglement_optimizer": "active",
            "model_entangler": "active"
        },
        "quantum_constants": {
            "lambda_consciousness": 8.977020,
            "base_frequency": 8.976089,
            "ionic_complex": "9+16j",
            "golden_ratio": 0.618033988749
        },
        "available_models": {
            "free_models": [
                "qwen/qwen3-coder:free",
                "tngtech/deepseek-r1t2-chimera:free",
                "moonshotai/kimi-dev-72b:free",
                "meta-llama/llama-3.2-11b-vision-instruct:free",
                "google/gemini-2.0-flash-exp:free"
            ],
            "premium_models": [
                "openai/gpt-5",
                "google/gemini-2.0-flash-001",
                "mistralai/mistral-medium-3.1"
            ]
        }
    })

@app.route('/api/models')
def get_models():
    """Obtener lista de modelos disponibles"""
    return jsonify({
        "free_models": {
            "supreme_code": {
                "id": "qwen/qwen3-coder:free",
                "context": "262,144 tokens",
                "description": "Modelo de código más potente gratuito"
            },
            "supreme_reasoning": {
                "id": "tngtech/deepseek-r1t2-chimera:free",
                "context": "163,840 tokens",
                "description": "Modelo de razonamiento superior gratuito"
            },
            "supreme_general": {
                "id": "moonshotai/kimi-dev-72b:free",
                "context": "131,072 tokens",
                "description": "Modelo general de alta capacidad"
            },
            "supreme_multimodal": {
                "id": "meta-llama/llama-3.2-11b-vision-instruct:free",
                "context": "32,768 tokens",
                "description": "Modelo multimodal gratuito"
            },
            "supreme_flash": {
                "id": "google/gemini-2.0-flash-exp:free",
                "context": "1,048,576 tokens",
                "description": "Modelo flash experimental gratuito"
            }
        },
        "premium_models": {
            "supreme_gpt5": {
                "id": "openai/gpt-5",
                "context": "400,000 tokens",
                "description": "GPT-5 - Modelo más potente disponible"
            },
            "supreme_gemini": {
                "id": "google/gemini-2.0-flash-001",
                "context": "1,048,576 tokens",
                "description": "Gemini 2.0 Flash - Modelo flash premium"
            },
            "supreme_mistral": {
                "id": "mistralai/mistral-medium-3.1",
                "context": "262,144 tokens",
                "description": "Mistral Medium 3.1 - Modelo premium"
            }
        }
    })

@app.route('/api/process', methods=['POST'])
def process_query():
    """Procesar consulta con edge máximo"""
    if quantum_edge_maximizer is None:
        return jsonify({
            "error": "Sistema cuántico no inicializado",
            "status": "initializing"
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Se requiere campo 'query' en el JSON"
            }), 400
        
        query = data['query']
        query_type = data.get('query_type', 'general')
        use_premium = data.get('use_premium', False)
        
        logger.info(f"🔍 Procesando consulta: {query[:50]}...")
        
        # Ejecutar procesamiento cuántico
        async def process_quantum():
            return await quantum_edge_maximizer.maximize_edge_for_query(query, query_type)
        
        # Ejecutar en loop de eventos
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(process_quantum())
        loop.close()
        
        return jsonify({
            "success": True,
            "query": query,
            "query_type": query_type,
            "use_premium": use_premium,
            "result": result
        })
        
    except Exception as e:
        logger.error(f"Error procesando consulta: {e}")
        return jsonify({
            "error": f"Error interno: {str(e)}",
            "success": False
        }), 500

@app.route('/api/health')
def health_check():
    """Verificar salud del sistema"""
    if quantum_edge_maximizer is None:
        return jsonify({
            "status": "unhealthy",
            "message": "Sistema cuántico no inicializado"
        }), 503
    
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "quantum_system": "active",
        "edge_maximizer": "operational"
    })

@app.route('/api/benchmark', methods=['POST'])
def run_benchmark():
    """Ejecutar benchmark del sistema"""
    if quantum_edge_maximizer is None:
        return jsonify({
            "error": "Sistema cuántico no inicializado"
        }), 503
    
    try:
        data = request.get_json()
        queries = data.get('queries', [
            "Escribe una función en Python para calcular el factorial",
            "Analiza esta imagen y describe lo que ves",
            "Resuelve esta ecuación matemática: x² + 5x + 6 = 0"
        ])
        
        results = []
        total_time = 0
        
        for i, query in enumerate(queries):
            start_time = time.time()
            
            # Ejecutar procesamiento cuántico
            async def process_quantum():
                return await quantum_edge_maximizer.maximize_edge_for_query(query)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(process_quantum())
            loop.close()
            
            processing_time = time.time() - start_time
            total_time += processing_time
            
            results.append({
                "query": query,
                "edge_multiplier": result['edge_maximization']['final_edge_multiplier'],
                "quantum_factor": result['edge_maximization']['quantum_factor'],
                "coherence": result['edge_maximization']['coherence_level'],
                "processing_time_ms": processing_time * 1000,
                "quantum_efficiency": result['performance']['quantum_efficiency']
            })
        
        return jsonify({
            "success": True,
            "benchmark_results": results,
            "summary": {
                "total_queries": len(queries),
                "total_time_ms": total_time * 1000,
                "average_time_ms": (total_time / len(queries)) * 1000,
                "average_edge_multiplier": sum(r['edge_multiplier'] for r in results) / len(results),
                "average_quantum_factor": sum(r['quantum_factor'] for r in results) / len(results)
            }
        })
        
    except Exception as e:
        logger.error(f"Error en benchmark: {e}")
        return jsonify({
            "error": f"Error en benchmark: {str(e)}",
            "success": False
        }), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Limpiar cache del sistema"""
    if quantum_edge_maximizer is None:
        return jsonify({
            "error": "Sistema cuántico no inicializado"
        }), 503
    
    try:
        # Limpiar caches
        quantum_edge_maximizer.edge_cache.clear()
        quantum_edge_maximizer.model_entangler.entanglement_cache.clear()
        quantum_edge_maximizer.model_entangler.edge_multipliers.clear()
        
        return jsonify({
            "success": True,
            "message": "Cache limpiado exitosamente",
            "caches_cleared": [
                "edge_cache",
                "entanglement_cache", 
                "edge_multipliers"
            ]
        })
        
    except Exception as e:
        logger.error(f"Error limpiando cache: {e}")
        return jsonify({
            "error": f"Error limpiando cache: {str(e)}",
            "success": False
        }), 500

@app.route('/api/cache/stats')
def cache_stats():
    """Obtener estadísticas del cache"""
    if quantum_edge_maximizer is None:
        return jsonify({
            "error": "Sistema cuántico no inicializado"
        }), 503
    
    try:
        return jsonify({
            "success": True,
            "cache_stats": {
                "edge_cache_size": len(quantum_edge_maximizer.edge_cache),
                "entanglement_cache_size": len(quantum_edge_maximizer.model_entangler.entanglement_cache),
                "edge_multipliers_size": len(quantum_edge_maximizer.model_entangler.edge_multipliers)
            }
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo stats de cache: {e}")
        return jsonify({
            "error": f"Error obteniendo stats: {str(e)}",
            "success": False
        }), 500

if __name__ == '__main__':
    logger.info("🚀 Iniciando Quantum Edge Server...")
    logger.info("📡 Servidor disponible en: http://localhost:5000")
    logger.info("🔍 Endpoints disponibles:")
    logger.info("   - GET  /api/status")
    logger.info("   - GET  /api/models") 
    logger.info("   - POST /api/process")
    logger.info("   - GET  /api/health")
    logger.info("   - POST /api/benchmark")
    logger.info("   - POST /api/cache/clear")
    logger.info("   - GET  /api/cache/stats")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
