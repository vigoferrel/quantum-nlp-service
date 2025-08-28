#!/usr/bin/env python3
"""
📦 EXPORTS CENTRALIZADOS - VIGOLEONROCKS MCP
Interfaces públicas y APIs del sistema
"""

# Core exports
from mcp.core.server import mcp_server, MCPServer
from mcp.core.manager import service_manager, ServiceManager
from mcp.core.logging import mcp_logger, MCPLogger, setup_mcp_logger

# Config exports
from mcp.config.settings import settings, Settings

# Main system
from mcp.main import VigoleonrocksMCPSystem

# Version info
__version__ = "1.0.0"
__author__ = "Vigoleonrocks Team"
__description__ = "Sistema MCP para Vigoleonrocks - #1 Mundial"

# Public API
__all__ = [
    # Core components
    "mcp_server",
    "MCPServer", 
    "service_manager",
    "ServiceManager",
    "mcp_logger",
    "MCPLogger",
    "setup_mcp_logger",
    
    # Configuration
    "settings",
    "Settings",
    
    # Main system
    "VigoleonrocksMCPSystem",
    
    # Version info
    "__version__",
    "__author__",
    "__description__"
]

def get_system_info():
    """Obtener información del sistema"""
    return {
        "name": "Vigoleonrocks MCP",
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "status": "running" if mcp_server.is_running else "stopped",
        "services_count": len(service_manager.services),
        "config": settings.get_config_summary()
    }

def get_api_endpoints():
    """Obtener endpoints de la API"""
    return {
        "mcp_server": f"http://{settings.mcp.host}:{settings.mcp.port}",
        "api_server": f"http://{settings.api.host}:{settings.api.port}",
        "monitoring": f"http://{settings.api.host}:{settings.monitoring.metrics_port}" if settings.monitoring.enabled else None
    }

def get_service_health():
    """Obtener estado de salud de servicios"""
    return service_manager.get_service_health()

def get_system_stats():
    """Obtener estadísticas del sistema"""
    return {
        "mcp_server": mcp_server.get_stats(),
        "service_manager": service_manager.get_service_stats(),
        "config": settings.get_config_summary()
    }
