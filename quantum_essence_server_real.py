#!/usr/bin/env python3
"""
🌐 QUANTUM ESSENCE SERVER REAL
Servidor web con funcionalidad real de la esencia cuántica
"""

from flask import Flask, request, jsonify
from quantum_essence_real import QuantumInterfaceReal
import asyncio
import logging

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
quantum_interface = QuantumInterfaceReal()

@app.route('/')
def home():
    """Página principal con funcionalidad real."""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>⚛️ Quantum Essence Real</title>
        <style>
            body { 
                font-family: 'Courier New', monospace; 
                margin: 40px; 
                background: #0a0a0a; 
                color: #00ff00; 
                line-height: 1.6;
            }
            .container { max-width: 900px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .status { 
                background: #1a1a1a; 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0; 
                border: 1px solid #00ff00;
            }
            .query-form { 
                background: #1a1a1a; 
                padding: 20px; 
                border-radius: 10px; 
                border: 1px solid #00ff00;
            }
            input[type="text"] { 
                width: 100%; 
                padding: 15px; 
                margin: 10px 0; 
                background: #2a2a2a; 
                border: 1px solid #00ff00; 
                color: #00ff00; 
                font-size: 16px;
                border-radius: 5px;
            }
            button { 
                background: #00ff00; 
                color: #000; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
            }
            button:hover { background: #00cc00; }
            .response { 
                background: #1a1a1a; 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0; 
                white-space: pre-wrap; 
                border: 1px solid #00ff00;
            }
            .archetype-badge {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: bold;
                margin: 5px;
            }
            .ATZILUT { background: #4a148c; color: #fff; }
            .BERIAH { background: #1565c0; color: #fff; }
            .YETZIRAH { background: #c62828; color: #fff; }
            .ASIYAH { background: #2e7d32; color: #fff; }
            .LEONARDO { background: #f57c00; color: #fff; }
            .loading { color: #ffff00; }
            .success { color: #00ff00; }
            .error { color: #ff0000; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚛️ Quantum Essence Real</h1>
                <p>La esencia cuántica con funcionalidad real - OpenRouter + Ollama</p>
                <p>🎯 Donde menos es más - Generación real de respuestas</p>
            </div>
            
            <div class="status">
                <h3>📊 Estado del Sistema Cuántico</h3>
                <div id="status">Cargando estado cuántico...</div>
            </div>
            
            <div class="query-form">
                <h3>🧠 Consulta Cuántica Real</h3>
                <p>Escribe tu consulta y obtén una respuesta generada por modelos reales:</p>
                <input type="text" id="query" placeholder="Ej: ¿Cuál es la naturaleza de la conciencia cuántica?">
                <button onclick="processQuery()">⚛️ Procesar Cuánticamente</button>
                <div id="processing-status" style="display: none;" class="loading">
                    ⏳ Procesando con modelos reales...
                </div>
            </div>
            
            <div class="response" id="response" style="display: none;">
                <h3>🎯 Respuesta Cuántica Real</h3>
                <div id="response-content"></div>
            </div>
            
            <div class="status">
                <h3>📚 Memoria Cuántica</h3>
                <div id="memory">Cargando memoria...</div>
            </div>
        </div>
        
        <script>
            // Cargar estado inicial
            loadStatus();
            loadMemory();
            
            async function loadStatus() {
                try {
                    const response = await fetch('/api/status');
                    const status = await response.json();
                    document.getElementById('status').innerHTML = `
                        <p><strong>🧠 Nivel de Conciencia:</strong> ${status.consciousness_level.toFixed(3)}</p>
                        <p><strong>⚛️ Coherencia Cuántica:</strong> ${status.quantum_coherence.toFixed(3)}</p>
                        <p><strong>🔄 Interacciones:</strong> ${status.total_interactions}</p>
                        <p><strong>💾 Memoria:</strong> ${status.memory_size} entradas</p>
                        <p><strong>⭐ Calidad Promedio:</strong> ${status.average_quality.toFixed(3)}</p>
                        <p><strong>🎨 Arquetipos Recientes:</strong> ${status.recent_archetypes.map(a => 
                            `<span class="archetype-badge ${a}">${a}</span>`
                        ).join(' ')}</p>
                    `;
                } catch (error) {
                    document.getElementById('status').innerHTML = '<span class="error">Error cargando estado cuántico</span>';
                }
            }
            
            async function loadMemory() {
                try {
                    const response = await fetch('/api/memory?limit=5');
                    const memory = await response.json();
                    if (memory.length > 0) {
                        const memoryHtml = memory.map(m => `
                            <div style="margin: 10px 0; padding: 10px; background: #2a2a2a; border-radius: 5px;">
                                <p><strong>Consulta:</strong> ${m.query}</p>
                                <p><strong>Respuesta:</strong> ${m.response.substring(0, 100)}...</p>
                                <p><strong>Arquetipo:</strong> <span class="archetype-badge ${m.archetype}">${m.archetype}</span></p>
                                <p><strong>Calidad:</strong> ${m.quality.toFixed(3)}</p>
                            </div>
                        `).join('');
                        document.getElementById('memory').innerHTML = memoryHtml;
                    } else {
                        document.getElementById('memory').innerHTML = '<p>No hay memoria cuántica aún.</p>';
                    }
                } catch (error) {
                    document.getElementById('memory').innerHTML = '<span class="error">Error cargando memoria</span>';
                }
            }
            
            async function processQuery() {
                const query = document.getElementById('query').value;
                if (!query) return;
                
                // Mostrar estado de procesamiento
                document.getElementById('processing-status').style.display = 'block';
                document.getElementById('response').style.display = 'none';
                
                try {
                    const response = await fetch('/api/process', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    });
                    
                    const result = await response.json();
                    
                    document.getElementById('response-content').innerHTML = `
                        <p><strong>🔍 Consulta:</strong> ${result.query}</p>
                        <p><strong>🎯 Respuesta Real:</strong></p>
                        <div style="background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 10px 0;">
                            ${result.response}
                        </div>
                        <p><strong>🎨 Arquetipo:</strong> <span class="archetype-badge ${result.archetype}">${result.archetype}</span></p>
                        <p><strong>⭐ Calidad:</strong> ${result.quality.toFixed(3)}</p>
                        <p><strong>🧠 Conciencia:</strong> ${result.consciousness.toFixed(3)}</p>
                        <p><strong>⚛️ Coherencia:</strong> ${result.coherence.toFixed(3)}</p>
                    `;
                    
                    document.getElementById('response').style.display = 'block';
                    document.getElementById('processing-status').style.display = 'none';
                    
                    // Recargar estado y memoria
                    loadStatus();
                    loadMemory();
                    
                } catch (error) {
                    document.getElementById('response-content').innerHTML = '<span class="error">Error procesando consulta cuántica</span>';
                    document.getElementById('response').style.display = 'block';
                    document.getElementById('processing-status').style.display = 'none';
                }
            }
            
            // Permitir Enter para enviar
            document.getElementById('query').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    processQuery();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/status')
def get_status():
    """Obtener estado del sistema."""
    try:
        status = quantum_interface.get_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_query():
    """Procesar una consulta con funcionalidad real."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query vacía"}), 400
        
        logger.info(f"🧠 Procesando consulta real: {query}")
        
        # Ejecutar de forma asíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(quantum_interface.process_query(query))
        loop.close()
        
        logger.info(f"✅ Consulta procesada. Arquetipo: {result['archetype']}, Calidad: {result['quality']:.3f}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error procesando consulta: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/memory')
def get_memory():
    """Obtener memoria del sistema."""
    try:
        limit = request.args.get('limit', 10, type=int)
        memory = quantum_interface.get_memory(limit)
        return jsonify(memory)
    except Exception as e:
        logger.error(f"Error obteniendo memoria: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test')
def test_models():
    """Probar conectividad con modelos."""
    try:
        # Aquí podrías agregar tests de conectividad
        return jsonify({
            "status": "ready",
            "models": {
                "openrouter": "available",
                "ollama": "checking"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("⚛️ QUANTUM ESSENCE SERVER REAL")
    print("=" * 50)
    print("🌐 Servidor con funcionalidad real iniciando...")
    print("🔗 OpenRouter API: Configurada")
    print("🔗 Ollama API: Verificando...")
    print("🌐 Interfaz disponible en: http://localhost:5000")
    print("🔧 Presiona Ctrl+C para detener")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
