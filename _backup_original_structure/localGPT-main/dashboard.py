"""
Dashboard de monitoreo en tiempo real para el sistema CIO
Visualización interactiva de métricas y evaluaciones
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from supabase_client import get_all_evaluations_async, get_evaluation_async

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardHandler(BaseHTTPRequestHandler):
    """Handler para el servidor web del dashboard"""

    def do_GET(self):
        """Maneja peticiones GET"""
        parsed_url = urlparse(self.path)

        if parsed_url.path == '/':
            self._serve_dashboard()
        elif parsed_url.path == '/api/evaluations':
            self._serve_evaluations()
        elif parsed_url.path == '/api/metrics':
            self._serve_metrics()
        elif parsed_url.path.startswith('/api/evaluation/'):
            evaluation_id = parsed_url.path.split('/')[-1]
            self._serve_single_evaluation(evaluation_id)
        elif parsed_url.path == '/health':
            self._serve_health()
        else:
            self._serve_404()

    def _serve_dashboard(self):
        """Sirve el dashboard HTML"""
        html = self._generate_dashboard_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def _serve_evaluations(self):
        """Sirve todas las evaluaciones"""
        try:
            evaluations = asyncio.run(get_all_evaluations_async())
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(evaluations, default=str).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def _serve_metrics(self):
        """Sirve métricas en tiempo real"""
        try:
            # Simular métricas en tiempo real
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "active_evaluations": 1,
                "total_evaluations": 5,
                "average_score": 82.5,
                "system_health": "healthy"
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def _serve_single_evaluation(self, evaluation_id: str):
        """Sirve una evaluación específica"""
        try:
            evaluation = asyncio.run(get_evaluation_async(evaluation_id))
            if evaluation:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(evaluation, default=str).encode())
            else:
                self.send_error(404, "Evaluation not found")
        except Exception as e:
            self.send_error(500, str(e))

    def _serve_health(self):
        """Sirve estado de salud"""
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time()
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(health).encode())

    def _serve_404(self):
        """Sirve página 404"""
        self.send_error(404, "Not Found")

    def _generate_dashboard_html(self) -> str:
        """Genera el HTML del dashboard"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIO Dashboard - Evaluación Orgánica</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            color: white;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .evaluations-list {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .evaluation-item {
            border-bottom: 1px solid #eee;
            padding: 15px 0;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .evaluation-item:hover {
            background: #f8f9fa;
        }
        .evaluation-item:last-child {
            border-bottom: none;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status-completed {
            background: #d4edda;
            color: #155724;
        }
        .status-running {
            background: #fff3cd;
            color: #856404;
        }
        .status-error {
            background: #f8d7da;
            color: #721c24;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            margin: 10px;
        }
        .refresh-btn:hover {
            background: #5a6fd8;
        }
        .chart-container {
            height: 300px;
            margin: 20px 0;
            background: #f8f9fa;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 CIO Dashboard</h1>
            <p>Evaluación Orgánica vs Kimi-K2-Instruct</p>
            <button class="refresh-btn" onclick="refreshData()">Actualizar</button>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Evaluaciones Totales</h3>
                <div class="metric-value" id="total-evaluations">-</div>
                <p>Evaluaciones completadas</p>
            </div>

            <div class="metric-card">
                <h3>Puntuación Promedio</h3>
                <div class="metric-value" id="average-score">-</div>
                <p>vs Kimi-K2-Instruct</p>
            </div>

            <div class="metric-card">
                <h3>Estado del Sistema</h3>
                <div class="metric-value" id="system-health">-</div>
                <p>Salud actual</p>
            </div>

            <div class="metric-card">
                <h3>Última Actualización</h3>
                <div class="metric-value" id="last-update">-</div>
                <p>Hace <span id="time-ago">-</span></p>
            </div>
        </div>

        <div class="chart-container">
            <p>Gráfico de comparación CIO vs Kimi-K2 (próximamente)</p>
        </div>

        <div class="evaluations-list">
            <h2>Evaluaciones Recientes</h2>
            <div id="evaluations-container">
                <p>Cargando evaluaciones...</p>
            </div>
        </div>
    </div>

    <script>
        let lastUpdateTime = new Date();

        async function refreshData() {
            try {
                // Actualizar métricas
                const metricsResponse = await fetch('/api/metrics');
                const metrics = await metricsResponse.json();

                document.getElementById('total-evaluations').textContent = metrics.total_evaluations;
                document.getElementById('average-score').textContent = metrics.average_score + '%';
                document.getElementById('system-health').textContent = metrics.system_health;

                lastUpdateTime = new Date(metrics.timestamp);
                updateTimeAgo();

                // Actualizar evaluaciones
                const evaluationsResponse = await fetch('/api/evaluations');
                const evaluations = await evaluationsResponse.json();

                const container = document.getElementById('evaluations-container');
                if (evaluations.length === 0) {
                    container.innerHTML = '<p>No hay evaluaciones disponibles</p>';
                } else {
                    container.innerHTML = evaluations.map(eval => `
                        <div class="evaluation-item" onclick="showEvaluationDetails('${eval.evaluation_id}')">
                            <strong>${eval.evaluation_id}</strong>
                            <span class="status-badge status-completed">Completado</span>
                            <br>
                            <small>${new Date(eval.timestamp).toLocaleString()}</small>
                            <br>
                            <small>Duración: ${eval.duration?.toFixed(2) || 'N/A'}s</small>
                        </div>
                    `).join('');
                }

            } catch (error) {
                console.error('Error actualizando datos:', error);
                document.getElementById('evaluations-container').innerHTML =
                    '<p>Error al cargar evaluaciones</p>';
            }
        }

        function updateTimeAgo() {
            const now = new Date();
            const diff = Math.floor((now - lastUpdateTime) / 1000);

            let timeAgo;
            if (diff < 60) {
                timeAgo = `${diff}s`;
            } else if (diff < 3600) {
                timeAgo = `${Math.floor(diff / 60)}m`;
            } else {
                timeAgo = `${Math.floor(diff / 3600)}h`;
            }

            document.getElementById('time-ago').textContent = timeAgo;
            document.getElementById('last-update').textContent = lastUpdateTime.toLocaleTimeString();
        }

        function showEvaluationDetails(evaluationId) {
            alert(`Detalles de evaluación: ${evaluationId}\\n(Implementación pendiente)`);
        }

        // Actualizar cada 30 segundos
        setInterval(refreshData, 30000);

        // Cargar datos iniciales
        refreshData();
    </script>
</body>
</html>
        """

class DashboardServer:
    """Servidor del dashboard de monitoreo"""

    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        """Inicia el servidor del dashboard"""
        try:
            self.server = HTTPServer((self.host, self.port), DashboardHandler)
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()

            logger.info(f"Dashboard iniciado en http://{self.host}:{self.port}")

            # Abrir en el navegador
            webbrowser.open(f"http://{self.host}:{self.port}")

        except Exception as e:
            logger.error(f"Error iniciando dashboard: {e}")

    def stop(self):
        """Detiene el servidor del dashboard"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("Dashboard detenido")

def main():
    """Función principal para iniciar el dashboard"""
    dashboard = DashboardServer()
    dashboard.start()

    try:
        print("Dashboard ejecutándose. Presiona Ctrl+C para detener.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        dashboard.stop()

if __name__ == "__main__":
    main()
