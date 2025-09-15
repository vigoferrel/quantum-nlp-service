#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Aplicación Principal
Aplicación Flask usando el App Factory con todos los componentes integrados
"""

import os
import sys
import time
from app_factory import create_app, get_app_info, health_check
from config import get_config, print_config_summary

def main():
    """Función principal para ejecutar VIGOLEONROCKS"""
    
    print("🚀 Iniciando VIGOLEONROCKS Sistema Multimodal")
    print("=" * 60)
    
    # Determinar entorno
    environment = os.environ.get('FLASK_ENV', 'development')
    print(f"📍 Entorno: {environment}")
    
    # Crear aplicación
    print("🔧 Creando aplicación Flask...")
    app = create_app(environment)
    
    with app.app_context():
        config = app.config.get('CONFIG_OBJECT')
        
        # Mostrar información de la aplicación
        print("\n📊 Información de la Aplicación:")
        app_info = get_app_info(app)
        for key, value in app_info.items():
            print(f"  {key}: {value}")
        
        # Health check inicial
        print("\n🏥 Health Check Inicial:")
        health = health_check(app)
        print(f"  Estado: {health['status']}")
        
        for component, status in health.get('checks', {}).items():
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {component}")
        
        print("\n🌐 URLs Disponibles:")
        print(f"  🏠 Página Principal: http://{config.HOST}:{config.PORT}/")
        print(f"  📊 Dashboard: http://{config.HOST}:{config.PORT}/dashboard")
        print(f"  🏢 Corporate: http://{config.HOST}:{config.PORT}/corporate")
        print(f"  💬 Chat UI: http://{config.HOST}:{config.PORT}/ui")
        print(f"  📚 API v2 Docs: http://{config.HOST}:{config.PORT}/api/v2/docs")
        print(f"  💚 Health Check: http://{config.HOST}:{config.PORT}/api/v2/system/health")
        
        print("\n" + "=" * 60)
        print("✅ VIGOLEONROCKS está listo y funcionando!")
        print("💡 Presiona Ctrl+C para detener el servidor")
        print("=" * 60)
    
    try:
        # Ejecutar servidor
        if environment == 'production':
            # En producción, usar un servidor WSGI apropiado
            print("🚀 Ejecutando en modo producción...")
            print("💡 Considera usar waitress, gunicorn o uWSGI para producción")
            
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True,
            use_reloader=False  # Evitar problemas con threads daemon
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo VIGOLEONROCKS...")
        print("¡Gracias por usar VIGOLEONROCKS! 🚀")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando el servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_with_waitress():
    """Ejecutar con waitress para producción"""
    try:
        from waitress import serve
        
        print("🚀 Iniciando servidor Waitress para producción...")
        app = create_app('production')
        config = app.config.get('CONFIG_OBJECT')
        
        serve(
            app,
            host=config.HOST,
            port=config.PORT,
            threads=config.WORKERS,
            connection_limit=100,
            cleanup_interval=30,
            channel_timeout=120
        )
        
    except ImportError:
        print("❌ Waitress no está instalado. Instálalo con: pip install waitress")
        print("Ejecutando con servidor de desarrollo...")
        main()
    except Exception as e:
        print(f"❌ Error ejecutando Waitress: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="VIGOLEONROCKS Sistema Multimodal")
    parser.add_argument(
        '--production',
        action='store_true',
        help='Ejecutar con servidor Waitress para producción'
    )
    parser.add_argument(
        '--env',
        choices=['development', 'production', 'testing'],
        default='development',
        help='Entorno de ejecución'
    )
    
    args = parser.parse_args()
    
    # Configurar variables de entorno
    os.environ['FLASK_ENV'] = args.env
    
    if args.production:
        os.environ['FLASK_ENV'] = 'production'
        run_with_waitress()
    else:
        main()
