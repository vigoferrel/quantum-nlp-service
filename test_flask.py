#!/usr/bin/env python3
"""
Test simple para VIGOLEONROCKS Flask
"""

import os
import sys
import time
import logging
from flask import Flask, jsonify, send_from_directory

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """Página principal - usando archivo real"""
    try:
        html_file = 'vigoleonrocks_corporate_ui.html'
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"✅ Sirviendo {html_file} - {len(content)} bytes")
                return content
        else:
            logger.error(f"❌ Archivo no encontrado: {html_file}")
            return f"<h1>Error: {html_file} no encontrado</h1><p>Archivos disponibles:</p><ul>" + \
                   "".join([f"<li>{f}</li>" for f in os.listdir('.') if f.endswith('.html')]) + "</ul>"
    except Exception as e:
        logger.error(f"Error leyendo archivo: {e}")
        return f"<h1>Error del servidor: {e}</h1>"

@app.route('/ui')
def ui():
    """Interfaz conversacional"""
    try:
        html_file = 'vigoleonrocks_corporate_ui_enhanced.html'
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"<h1>💬 Interfaz Conversacional</h1><p>Archivo {html_file} no encontrado</p><a href='/'>Volver</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

@app.route('/quantum')
def quantum():
    """Quantum Command Center"""
    try:
        html_file = 'vigoleonrocks_quantum_command_center.html'
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"<h1>🎯 Quantum Command Center</h1><p>Archivo {html_file} no encontrado</p><a href='/'>Volver</a>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

@app.route('/api/status')
def status():
    """API Status"""
    return jsonify({
        "status": "operational",
        "service": "VIGOLEONROCKS Test",
        "uptime": time.time(),
        "files_found": [f for f in os.listdir('.') if f.endswith('.html')]
    })

@app.route('/test')
def test():
    """Página de test simple"""
    return """
    <h1>🧪 VIGOLEONROCKS Test</h1>
    <p>Si ves esto, el servidor Flask funciona correctamente!</p>
    <ul>
        <li><a href="/">🏠 Home</a></li>
        <li><a href="/ui">💬 UI</a></li>
        <li><a href="/quantum">🎯 Quantum</a></li>
        <li><a href="/api/status">📊 Status</a></li>
    </ul>
    <p>Directorio actual: {}</p>
    <p>Archivos HTML encontrados:</p>
    <ul>{}</ul>
    """.format(
        os.getcwd(),
        "".join([f"<li>{f}</li>" for f in os.listdir('.') if f.endswith('.html')])
    )

if __name__ == '__main__':
    logger.info("🧪 Iniciando VIGOLEONROCKS Test Server")
    logger.info(f"📁 Directorio de trabajo: {os.getcwd()}")
    
    # Verificar archivos HTML
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    logger.info(f"📄 Archivos HTML encontrados: {html_files}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
