#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS System Launcher - Versión Completa Integrada
Lanza el sistema completo con todas las optimizaciones y mejoras
"""

import os
import sys
import time
import logging
import asyncio
from datetime import datetime
from flask import Flask

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VIGOLEONROCKS_LAUNCHER')

def print_banner():
    """Muestra el banner del sistema"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                      🚀 VIGOLEONROCKS SYSTEM 2025                     ║
    ║                    Sistema Multimodal de IA Avanzada                  ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  🔗 CLIP: Modelo de embeddings multimodales                          ║
    ║  🧠 MultimodalAI: Análisis de imágenes y audio                       ║
    ║  ⚡ PerformanceOptimizer: Cache inteligente y monitoreo               ║
    ║  📊 Dashboard: Interfaz visual en tiempo real                        ║
    ║  🌐 Enhanced APIs: Endpoints v2 documentados                         ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_system_requirements():
    """Verifica que todos los componentes estén disponibles"""
    print("🔍 Verificando componentes del sistema...")
    
    status = {
        'flask_app': False,
        'multimodal_manager': False,
        'performance_optimizer': False,
        'enhanced_api': False,
        'dashboard': False
    }
    
    # Check Flask app
    try:
        import flask_app_fast
        status['flask_app'] = True
        print("  ✅ Flask App: Disponible")
    except ImportError as e:
        print(f"  ❌ Flask App: {e}")
    
    # Check Multimodal Manager
    try:
        from multimodal_ai_manager import get_multimodal_manager, CLIP_AVAILABLE
        status['multimodal_manager'] = True
        print(f"  ✅ Multimodal Manager: Disponible (CLIP: {'✅' if CLIP_AVAILABLE else '❌'})")
    except ImportError as e:
        print(f"  ❌ Multimodal Manager: {e}")
    
    # Check Performance Optimizer
    try:
        from performance_optimizer import performance_optimizer
        status['performance_optimizer'] = True
        print("  ✅ Performance Optimizer: Disponible")
    except ImportError as e:
        print(f"  ❌ Performance Optimizer: {e}")
    
    # Check Enhanced API
    try:
        from enhanced_api_endpoints import initialize_enhanced_api
        status['enhanced_api'] = True
        print("  ✅ Enhanced API: Disponible")
    except ImportError as e:
        print(f"  ❌ Enhanced API: {e}")
    
    # Check Dashboard
    try:
        if os.path.exists('dashboard_monitoring.html'):
            status['dashboard'] = True
            print("  ✅ Dashboard: Disponible")
        else:
            print("  ❌ Dashboard: Archivo HTML no encontrado")
    except Exception as e:
        print(f"  ❌ Dashboard: {e}")
    
    return status

def initialize_system_components():
    """Inicializa todos los componentes del sistema"""
    print("\n🔧 Inicializando componentes del sistema...")
    
    # 1. Aplicar optimizaciones al sistema multimodal
    try:
        from performance_optimizer import optimize_multimodal_manager
        if optimize_multimodal_manager():
            print("  ✅ Optimizaciones aplicadas al MultimodalAIManager")
        else:
            print("  ⚠️ Algunas optimizaciones no se pudieron aplicar")
    except Exception as e:
        print(f"  ❌ Error aplicando optimizaciones: {e}")
    
    # 2. Verificar estado del sistema
    try:
        from multimodal_ai_manager import get_multimodal_manager
        manager = get_multimodal_manager()
        system_status = manager.get_system_status()
        
        print(f"  📊 Modelos disponibles: {len(system_status.get('models_available', []))}")
        print(f"  🔧 Modelos habilitados: {len(system_status.get('models_enabled', []))}")
        print(f"  💾 Modelos cargados: {system_status.get('models_loaded', 0)}")
        
        # Mostrar estado de capacidades
        capabilities = system_status.get('capabilities', {})
        for capability, available in capabilities.items():
            emoji = "✅" if available else "❌"
            print(f"  {emoji} {capability}: {'Disponible' if available else 'No disponible'}")
            
    except Exception as e:
        print(f"  ❌ Error verificando estado del sistema: {e}")

def create_integrated_flask_app():
    """Crea la aplicación Flask integrada con todos los componentes"""
    print("\n🌐 Configurando aplicación Flask integrada...")
    
    # Importar Flask app base
    try:
        from flask_app_fast import app
        print("  ✅ Flask app base cargada")
    except ImportError:
        print("  ❌ Error cargando Flask app base")
        return None
    
    # Integrar Enhanced API
    try:
        from enhanced_api_endpoints import initialize_enhanced_api
        enhanced_api = initialize_enhanced_api(app)
        print("  ✅ Enhanced API integrada")
    except Exception as e:
        print(f"  ⚠️ Enhanced API no integrada: {e}")
    
    # Agregar endpoints adicionales para el dashboard
    @app.route('/system/status')
    def system_status_page():
        """Página de estado del sistema"""
        try:
            with open('dashboard_monitoring.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
                # Reemplazar título para diferenciar
                html_content = html_content.replace(
                    '🚀 VIGOLEONROCKS Dashboard', 
                    '🚀 VIGOLEONROCKS System Status'
                )
                return html_content
        except FileNotFoundError:
            return '''
            <html>
            <head><title>System Status</title></head>
            <body>
                <h1>🚀 VIGOLEONROCKS System Status</h1>
                <p>Dashboard file not found. System is running on basic mode.</p>
                <a href="/api/status">View API Status</a> | 
                <a href="/api/multimodal/status">View Multimodal Status</a>
            </body>
            </html>
            '''
    
    return app

def show_system_urls():
    """Muestra todas las URLs disponibles del sistema"""
    print("\n🌐 URLs del Sistema Disponibles:")
    print("="*70)
    
    # URLs principales
    main_urls = [
        ("🏠 Página Principal", "http://localhost:5000/"),
        ("🏢 Página Corporate", "http://localhost:5000/corporate"),
        ("💬 Chat Interface", "http://localhost:5000/ui"),
        ("📊 Dashboard Monitoreo", "http://localhost:5000/dashboard"),
        ("🔧 System Status", "http://localhost:5000/system/status"),
        ("⚡ Quantum Center", "http://localhost:5000/quantum"),
    ]
    
    for name, url in main_urls:
        print(f"  {name:<25} {url}")
    
    print("\n🔌 APIs Disponibles:")
    print("="*70)
    
    # APIs v1 (originales)
    api_v1 = [
        ("📊 Status", "GET  /api/status"),
        ("📈 Metrics", "GET  /api/quantum-metrics"),
        ("🔗 Multimodal Status", "GET  /api/multimodal/status"),
        ("⚡ Performance", "GET  /api/performance/report"),
        ("💬 Chat", "POST /api/chat"),
        ("📸 Upload Image", "POST /api/upload/image"),
        ("🎤 Upload Audio", "POST /api/upload/audio"),
    ]
    
    for name, endpoint in api_v1:
        print(f"  {name:<25} {endpoint}")
    
    print("\n🚀 APIs v2 Mejoradas:")
    print("="*70)
    
    # APIs v2 (nuevas)
    api_v2 = [
        ("📚 Documentación", "GET  /api/v2/docs"),
        ("📊 Métricas Avanzadas", "GET  /api/v2/metrics"),
        ("💚 Health Check", "GET  /api/v2/system/health"),
        ("🧠 Lista Modelos", "GET  /api/v2/system/models"),
        ("🖼️ Análisis Imagen", "POST /api/v2/image/analyze"),
        ("⚡ Análisis Rápido", "POST /api/v2/image/quick"),
        ("💾 Stats Cache", "GET  /api/v2/cache/stats"),
        ("🧹 Clear Cache", "POST /api/v2/cache/clear"),
    ]
    
    for name, endpoint in api_v2:
        print(f"  {name:<25} {endpoint}")

def run_system():
    """Ejecuta el sistema completo"""
    print("\n🚀 Iniciando VIGOLEONROCKS System...")
    
    try:
        # Crear app integrada
        app = create_integrated_flask_app()
        
        if app is None:
            print("❌ No se pudo crear la aplicación Flask")
            return
        
        # Mostrar URLs disponibles
        show_system_urls()
        
        print("\n" + "="*70)
        print("🎉 ¡SISTEMA VIGOLEONROCKS LISTO!")
        print("="*70)
        print("📊 Dashboard principal: http://localhost:5000/dashboard")
        print("📚 Documentación API: http://localhost:5000/api/v2/docs")
        print("💚 Health Check: http://localhost:5000/api/v2/system/health")
        print("="*70)
        print("\n🔥 Iniciando servidor Flask...")
        print("Presiona Ctrl+C para detener el servidor")
        print("="*70)
        
        # Ejecutar servidor
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=False, 
            threaded=True,
            use_reloader=False  # Evitar reinicios automáticos
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema detenido por el usuario")
        print("¡Gracias por usar VIGOLEONROCKS! 🚀")
    except Exception as e:
        print(f"\n❌ Error ejecutando el sistema: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal del launcher"""
    print_banner()
    
    print(f"🕒 Iniciando sistema a las: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📂 Directorio de trabajo: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version.split()[0]}")
    
    # Verificar componentes
    status = check_system_requirements()
    
    # Verificar componentes críticos
    critical_components = ['flask_app', 'multimodal_manager']
    missing_critical = [comp for comp in critical_components if not status[comp]]
    
    if missing_critical:
        print(f"\n❌ Componentes críticos faltantes: {missing_critical}")
        print("🔧 Asegúrate de que todos los archivos estén presentes")
        return
    
    # Inicializar componentes
    initialize_system_components()
    
    # Ejecutar sistema
    run_system()

if __name__ == "__main__":
    main()
