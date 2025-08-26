#!/usr/bin/env python3
"""
🌐 QUANTUM ESSENCE SERVER
Servidor web simple para la esencia cuántica
"""

from flask import Flask, request, jsonify
from quantum_essence import QuantumInterface
import asyncio
import logging

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
quantum_interface = QuantumInterface()

@app.route('/')
def home():
    """Página principal simple."""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>⚛️ Quantum Essence</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #0a0a0a; color: #00ff00; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { background: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .query-form { background: #1a1a1a; padding: 20px; border-radius: 10px; }
            input[type="text"] { width: 100%; padding: 10px; margin: 10px 0; background: #2a2a2a; border: 1px solid #00ff00; color: #00ff00; }
            button { background: #00ff00; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .response { background: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚛️ Quantum Essence</h1>
            <p>La esencia real del sistema cuántico - Donde menos es más</p>
            
            <div class="status">
                <h3>Estado del Sistema</h3>
                <div id="status">Cargando...</div>
            </div>
            
            <div class="query-form">
                <h3>Consulta Cuántica</h3>
                <input type="text" id="query" placeholder="Escribe tu consulta aquí...">
                <button onclick="processQuery()">Procesar</button>
            </div>
            
            <div class="response" id="response" style="display: none;">
                <h3>Respuesta Cuántica</h3>
                <div id="response-content"></div>
            </div>
        </div>
        
        <script>
            // Cargar estado inicial
            loadStatus();
            
            async function loadStatus() {
                try {
                    const response = await fetch('/api/status');
                    const status = await response.json();
                    document.getElementById('status').innerHTML = `
                        <p>Nivel de Conciencia: ${status.consciousness_level.toFixed(3)}</p>
                        <p>Coherencia Cuántica: ${status.quantum_coherence.toFixed(3)}</p>
                        <p>Interacciones: ${status.total_interactions}</p>
                        <p>Memoria: ${status.memory_size} entradas</p>
                        <p>Calidad Promedio: ${status.average_quality.toFixed(3)}</p>
                    `;
                } catch (error) {
                    document.getElementById('status').innerHTML = 'Error cargando estado';
                }
            }
            
            async function processQuery() {
                const query = document.getElementById('query').value;
                if (!query) return;
                
                try {
                    const response = await fetch('/api/process', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    });
                    
                    const result = await response.json();
                    
                    document.getElementById('response-content').innerHTML = `
                        <p><strong>Consulta:</strong> ${result.query}</p>
                        <p><strong>Respuesta:</strong> ${result.response}</p>
                        <p><strong>Arquetipo:</strong> ${result.archetype}</p>
                        <p><strong>Calidad:</strong> ${result.quality.toFixed(3)}</p>
                        <p><strong>Conciencia:</strong> ${result.consciousness.toFixed(3)}</p>
                    `;
                    
                    document.getElementById('response').style.display = 'block';
                    
                    // Recargar estado
                    loadStatus();
                    
                } catch (error) {
                    document.getElementById('response-content').innerHTML = 'Error procesando consulta';
                    document.getElementById('response').style.display = 'block';
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
    """Procesar una consulta."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query vacía"}), 400
        
        # Ejecutar de forma asíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(quantum_interface.process_query(query))
        loop.close()
        
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

if __name__ == '__main__':
    print("⚛️ QUANTUM ESSENCE SERVER")
    print("=" * 40)
    print("🌐 Servidor iniciando en http://localhost:5000")
    print("🔧 Presiona Ctrl+C para detener")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
