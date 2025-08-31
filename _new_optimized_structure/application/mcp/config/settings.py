#!/usr/bin/env python3
"""
⚙️ CONFIGURACIÓN DEL SISTEMA MCP - VIGOLEONROCKS
Configuración centralizada del sistema
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

class Environment(Enum):
    """Entornos de ejecución"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    host: str = "localhost"
    port: int = 5432
    name: str = "vigoleonrocks"
    user: str = "postgres"
    password: str = ""
    pool_size: int = 10
    max_overflow: int = 20

@dataclass
class APIConfig:
    """Configuración de API"""
    host: str = "localhost"
    port: int = 5001
    debug: bool = False
    cors_origins: list = None
    rate_limit: int = 1000
    timeout: int = 30

@dataclass
class MCPConfig:
    """Configuración MCP"""
    host: str = "localhost"
    port: int = 5002
    protocol_version: str = "2024-11-05"
    max_connections: int = 100
    heartbeat_interval: int = 30

@dataclass
class MonitoringConfig:
    """Configuración de monitoreo"""
    enabled: bool = True
    metrics_port: int = 9090
    health_check_interval: int = 30
    alert_thresholds: Dict[str, float] = None

@dataclass
class NotificationConfig:
    """Configuración de notificaciones"""
    email_enabled: bool = False
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    webhook_urls: list = None

@dataclass
class SecurityConfig:
    """Configuración de seguridad"""
    secret_key: str = ""
    jwt_expiration: int = 3600
    api_key_expiration: int = 86400
    max_login_attempts: int = 5
    password_min_length: int = 8

@dataclass
class VigoleonrocksConfig:
    """Configuración específica de Vigoleonrocks"""
    model_name: str = "vigoleonrocks_optimized"
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    quantum_enabled: bool = True
    memory_26d_enabled: bool = True

class Settings:
    """Configuración principal del sistema"""
    
    def __init__(self, env: Environment = None):
        self.environment = env or self._get_environment()
        self.config_file = f"config/{self.environment.value}.json"
        
        # Configuraciones por defecto
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.mcp = MCPConfig()
        self.monitoring = MonitoringConfig()
        self.notifications = NotificationConfig()
        self.security = SecurityConfig()
        self.vigoleonrocks = VigoleonrocksConfig()
        
        # Cargar configuración
        self._load_config()
        self._load_environment_variables()
    
    def _get_environment(self) -> Environment:
        """Obtener entorno desde variable de entorno"""
        env_str = os.getenv("VIGOLEONROCKS_ENV", "development").lower()
        
        try:
            return Environment(env_str)
        except ValueError:
            return Environment.DEVELOPMENT
    
    def _load_config(self):
        """Cargar configuración desde archivo"""
        config_path = Path(self.config_file)
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Aplicar configuración
                self._apply_config(config_data)
                
            except Exception as e:
                print(f"⚠️ Error cargando configuración: {e}")
    
    def _load_environment_variables(self):
        """Cargar variables de entorno"""
        # Database
        if os.getenv("DB_HOST"):
            self.database.host = os.getenv("DB_HOST")
        if os.getenv("DB_PORT"):
            self.database.port = int(os.getenv("DB_PORT"))
        if os.getenv("DB_NAME"):
            self.database.name = os.getenv("DB_NAME")
        if os.getenv("DB_USER"):
            self.database.user = os.getenv("DB_USER")
        if os.getenv("DB_PASSWORD"):
            self.database.password = os.getenv("DB_PASSWORD")
        
        # API
        if os.getenv("API_HOST"):
            self.api.host = os.getenv("API_HOST")
        if os.getenv("API_PORT"):
            self.api.port = int(os.getenv("API_PORT"))
        if os.getenv("API_DEBUG"):
            self.api.debug = os.getenv("API_DEBUG").lower() == "true"
        
        # MCP
        if os.getenv("MCP_HOST"):
            self.mcp.host = os.getenv("MCP_HOST")
        if os.getenv("MCP_PORT"):
            self.mcp.port = int(os.getenv("MCP_PORT"))
        
        # Security
        if os.getenv("SECRET_KEY"):
            self.security.secret_key = os.getenv("SECRET_KEY")
        
        # Notifications
        if os.getenv("SMTP_HOST"):
            self.notifications.smtp_host = os.getenv("SMTP_HOST")
        if os.getenv("SMTP_USER"):
            self.notifications.smtp_user = os.getenv("SMTP_USER")
        if os.getenv("SMTP_PASSWORD"):
            self.notifications.smtp_password = os.getenv("SMTP_PASSWORD")
    
    def _apply_config(self, config_data: Dict[str, Any]):
        """Aplicar configuración desde diccionario"""
        # Database
        if "database" in config_data:
            db_config = config_data["database"]
            for key, value in db_config.items():
                if hasattr(self.database, key):
                    setattr(self.database, key, value)
        
        # API
        if "api" in config_data:
            api_config = config_data["api"]
            for key, value in api_config.items():
                if hasattr(self.api, key):
                    setattr(self.api, key, value)
        
        # MCP
        if "mcp" in config_data:
            mcp_config = config_data["mcp"]
            for key, value in mcp_config.items():
                if hasattr(self.mcp, key):
                    setattr(self.mcp, key, value)
        
        # Monitoring
        if "monitoring" in config_data:
            monitoring_config = config_data["monitoring"]
            for key, value in monitoring_config.items():
                if hasattr(self.monitoring, key):
                    setattr(self.monitoring, key, value)
        
        # Notifications
        if "notifications" in config_data:
            notification_config = config_data["notifications"]
            for key, value in notification_config.items():
                if hasattr(self.notifications, key):
                    setattr(self.notifications, key, value)
        
        # Security
        if "security" in config_data:
            security_config = config_data["security"]
            for key, value in security_config.items():
                if hasattr(self.security, key):
                    setattr(self.security, key, value)
        
        # Vigoleonrocks
        if "vigoleonrocks" in config_data:
            vigoleonrocks_config = config_data["vigoleonrocks"]
            for key, value in vigoleonrocks_config.items():
                if hasattr(self.vigoleonrocks, key):
                    setattr(self.vigoleonrocks, key, value)
    
    def save_config(self, filename: str = None):
        """Guardar configuración actual"""
        if not filename:
            filename = self.config_file
        
        config_data = {
            "environment": self.environment.value,
            "database": asdict(self.database),
            "api": asdict(self.api),
            "mcp": asdict(self.mcp),
            "monitoring": asdict(self.monitoring),
            "notifications": asdict(self.notifications),
            "security": asdict(self.security),
            "vigoleonrocks": asdict(self.vigoleonrocks)
        }
        
        # Crear directorio si no existe
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, default=str)
    
    def get_database_url(self) -> str:
        """Obtener URL de conexión a base de datos"""
        return f"postgresql://{self.database.user}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.name}"
    
    def is_development(self) -> bool:
        """Verificar si es entorno de desarrollo"""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Verificar si es entorno de producción"""
        return self.environment == Environment.PRODUCTION
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Obtener resumen de configuración"""
        return {
            "environment": self.environment.value,
            "api_url": f"http://{self.api.host}:{self.api.port}",
            "mcp_url": f"http://{self.mcp.host}:{self.mcp.port}",
            "database_host": self.database.host,
            "monitoring_enabled": self.monitoring.enabled,
            "notifications_enabled": self.notifications.email_enabled,
            "quantum_enabled": self.vigoleonrocks.quantum_enabled
        }

# Instancia global de configuración
settings = Settings()
