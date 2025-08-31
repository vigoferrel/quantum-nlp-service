#!/usr/bin/env python3
"""
🎯 PUNTO DE ENTRADA PRINCIPAL - VIGOLEONROCKS MCP
Sistema principal del Model Context Protocol
"""

import asyncio
import signal
import sys
from pathlib import Path

# Agregar directorio padre al path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from mcp.core.server import mcp_server
    from mcp.core.manager import service_manager
    from mcp.core.logging import mcp_logger
    from mcp.config.settings import settings
except ImportError:
    # Fallback para desarrollo
    from core.server import mcp_server
    from core.manager import service_manager
    from core.logging import mcp_logger
    from config.settings import settings

class VigoleonrocksMCPSystem:
    """Sistema principal MCP de Vigoleonrocks"""
    
    def __init__(self):
        self.is_running = False
        self.tasks = []
        
    async def initialize(self):
        """Inicializar el sistema"""
        mcp_logger.info("🚀 Inicializando sistema Vigoleonrocks MCP")
        
        # Configurar signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Mostrar configuración
        config_summary = settings.get_config_summary()
        mcp_logger.info("⚙️ Configuración del sistema:", config_summary)
        
        # Registrar servicios base
        await self._register_base_services()
        
        # Iniciar servicios
        await self._start_services()
        
        mcp_logger.info("✅ Sistema inicializado correctamente")
    
    async def _register_base_services(self):
        """Registrar servicios base"""
        mcp_logger.info("📝 Registrando servicios base...")
        
        # Importar servicios
        try:
            from mcp.services.vigoleonrocks_service import vigoleonrocks_service
            from mcp.services.monitor_service import monitor_service
            
            # Registrar servicios
            service_manager.register_service("vigoleonrocks", vigoleonrocks_service)
            service_manager.register_service("monitor", monitor_service)
            
            # Registrar servicios en el servidor MCP
            mcp_server.register_service("vigoleonrocks", vigoleonrocks_service)
            mcp_server.register_service("monitor", monitor_service)
            
            mcp_logger.info("✅ Servicios base registrados")
            
        except ImportError as e:
            mcp_logger.error(f"❌ Error importando servicios: {e}")
            mcp_logger.info("⚠️ Continuando sin servicios adicionales")
    
    async def _start_services(self):
        """Iniciar servicios"""
        mcp_logger.info("🔄 Iniciando servicios...")
        
        # Iniciar todos los servicios
        results = await service_manager.start_all_services()
        
        for service_name, success in results.items():
            if success:
                mcp_logger.info(f"✅ Servicio iniciado: {service_name}")
            else:
                mcp_logger.error(f"❌ Error iniciando servicio: {service_name}")
        
        # Iniciar monitor de health checks
        health_check_task = asyncio.create_task(
            service_manager.start_health_check_monitor()
        )
        self.tasks.append(health_check_task)
        
        mcp_logger.info("✅ Servicios iniciados")
    
    async def start(self):
        """Iniciar el sistema"""
        try:
            await self.initialize()
            
            self.is_running = True
            mcp_logger.info("🏆 Sistema Vigoleonrocks MCP ejecutándose")
            
            # Iniciar servidor MCP
            server_task = asyncio.create_task(
                mcp_server.start(settings.mcp.host, settings.mcp.port)
            )
            self.tasks.append(server_task)
            
            # Mantener el sistema ejecutándose
            while self.is_running:
                await asyncio.sleep(1)
                
        except Exception as e:
            mcp_logger.error(f"❌ Error en el sistema: {e}")
            await self.shutdown()
    
    async def shutdown(self):
        """Apagar el sistema"""
        mcp_logger.info("🛑 Apagando sistema Vigoleonrocks MCP...")
        
        self.is_running = False
        
        # Detener servidor MCP
        mcp_server.stop()
        
        # Detener monitor de health checks
        service_manager.stop_health_check_monitor()
        
        # Detener todos los servicios
        await service_manager.stop_all_services()
        
        # Cancelar tareas pendientes
        for task in self.tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        mcp_logger.info("✅ Sistema apagado correctamente")
    
    def _signal_handler(self, signum, frame):
        """Manejar señales del sistema"""
        mcp_logger.info(f"📡 Señal recibida: {signum}")
        asyncio.create_task(self.shutdown())

async def main():
    """Función principal"""
    system = VigoleonrocksMCPSystem()
    
    try:
        await system.start()
    except KeyboardInterrupt:
        mcp_logger.info("⌨️ Interrupción de teclado recibida")
    except Exception as e:
        mcp_logger.error(f"❌ Error fatal: {e}")
    finally:
        await system.shutdown()

if __name__ == "__main__":
    # Configurar logging
    mcp_logger.info("🎯 Iniciando Vigoleonrocks MCP System")
    
    # Ejecutar sistema
    asyncio.run(main())
