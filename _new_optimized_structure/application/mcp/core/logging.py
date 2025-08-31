#!/usr/bin/env python3
"""
📝 SISTEMA DE LOGGING MCP - VIGOLEONROCKS
Sistema de logging estructurado y centralizado
"""

import logging
import json
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import threading
from enum import Enum

class LogLevel(Enum):
    """Niveles de logging"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class MCPLogHandler:
    """Handler base para logging MCP"""
    
    def __init__(self, level: LogLevel = LogLevel.INFO):
        self.level = level
        self.formatter = None
    
    def set_formatter(self, formatter):
        """Establecer formateador"""
        self.formatter = formatter
    
    def emit(self, record):
        """Emitir log (debe ser implementado por subclases)"""
        raise NotImplementedError

class ConsoleLogHandler(MCPLogHandler):
    """Handler para consola con colores"""
    
    def __init__(self, level: LogLevel = LogLevel.INFO):
        super().__init__(level)
        self.colors = {
            LogLevel.DEBUG: "\033[36m",    # Cyan
            LogLevel.INFO: "\033[32m",     # Green
            LogLevel.WARNING: "\033[33m",  # Yellow
            LogLevel.ERROR: "\033[31m",    # Red
            LogLevel.CRITICAL: "\033[35m"  # Magenta
        }
        self.reset_color = "\033[0m"
    
    def emit(self, record):
        """Emitir log a consola"""
        if record.levelno >= self.level.value:
            color = self.colors.get(LogLevel(record.levelname), "")
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            
            message = f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}{self.reset_color}"
            
            if hasattr(record, 'context') and record.context:
                context_str = json.dumps(record.context, indent=2)
                message += f"\n{color}Context: {context_str}{self.reset_color}"
            
            print(message, file=sys.stderr)

class FileLogHandler(MCPLogHandler):
    """Handler para archivo JSON"""
    
    def __init__(self, filename: str, level: LogLevel = LogLevel.INFO):
        super().__init__(level)
        self.filename = filename
        self.lock = threading.Lock()
        
        # Crear directorio si no existe
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    def emit(self, record):
        """Emitir log a archivo JSON"""
        if record.levelno >= self.level.value:
            log_entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            
            if hasattr(record, 'context') and record.context:
                log_entry["context"] = record.context
            
            with self.lock:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + '\n')

class MCPLogger:
    """Logger principal MCP"""
    
    def __init__(self, name: str = "vigoleonrocks-mcp"):
        self.name = name
        self.handlers: List[MCPLogHandler] = []
        self.context: Dict[str, Any] = {}
        self.lock = threading.Lock()
    
    def add_handler(self, handler: MCPLogHandler):
        """Agregar handler"""
        with self.lock:
            self.handlers.append(handler)
    
    def set_context(self, context: Dict[str, Any]):
        """Establecer contexto global"""
        with self.lock:
            self.context.update(context)
    
    def clear_context(self):
        """Limpiar contexto"""
        with self.lock:
            self.context.clear()
    
    def _log(self, level: LogLevel, message: str, context: Dict[str, Any] = None):
        """Método interno de logging"""
        # Combinar contexto global y específico
        full_context = self.context.copy()
        if context:
            full_context.update(context)
        
        # Crear record
        record = logging.LogRecord(
            name=self.name,
            level=level.value,
            pathname="",
            lineno=0,
            msg=message,
            args=(),
            exc_info=None
        )
        
        # Agregar contexto al record
        record.context = full_context
        
        # Emitir a todos los handlers
        with self.lock:
            for handler in self.handlers:
                try:
                    handler.emit(record)
                except Exception as e:
                    # Fallback a stderr si hay error
                    print(f"Error en handler de logging: {e}", file=sys.stderr)
    
    def debug(self, message: str, context: Dict[str, Any] = None):
        """Log de debug"""
        self._log(LogLevel.DEBUG, message, context)
    
    def info(self, message: str, context: Dict[str, Any] = None):
        """Log de info"""
        self._log(LogLevel.INFO, message, context)
    
    def warning(self, message: str, context: Dict[str, Any] = None):
        """Log de warning"""
        self._log(LogLevel.WARNING, message, context)
    
    def error(self, message: str, context: Dict[str, Any] = None):
        """Log de error"""
        self._log(LogLevel.ERROR, message, context)
    
    def critical(self, message: str, context: Dict[str, Any] = None):
        """Log crítico"""
        self._log(LogLevel.CRITICAL, message, context)
    
    def log_request(self, method: str, params: Dict[str, Any], response: Any = None, error: str = None):
        """Log específico para requests"""
        context = {
            "type": "request",
            "method": method,
            "params": params
        }
        
        if response:
            context["response"] = response
        
        if error:
            context["error"] = error
            self.error(f"Request failed: {method}", context)
        else:
            self.info(f"Request completed: {method}", context)
    
    def log_service_event(self, service_name: str, event: str, details: Dict[str, Any] = None):
        """Log específico para eventos de servicios"""
        context = {
            "type": "service_event",
            "service": service_name,
            "event": event
        }
        
        if details:
            context.update(details)
        
        self.info(f"Service event: {service_name} - {event}", context)
    
    def log_performance(self, operation: str, duration: float, context: Dict[str, Any] = None):
        """Log específico para métricas de rendimiento"""
        perf_context = {
            "type": "performance",
            "operation": operation,
            "duration_ms": round(duration * 1000, 2)
        }
        
        if context:
            perf_context.update(context)
        
        if duration > 1.0:  # Más de 1 segundo
            self.warning(f"Slow operation: {operation} ({duration:.2f}s)", perf_context)
        else:
            self.debug(f"Operation completed: {operation} ({duration:.2f}s)", perf_context)

# Configuración global del logger
def setup_mcp_logger(name: str = "vigoleonrocks-mcp", 
                    console_level: LogLevel = LogLevel.INFO,
                    file_level: LogLevel = LogLevel.DEBUG,
                    log_file: str = "logs/vigoleonrocks-mcp.json"):
    """Configurar logger MCP global"""
    
    logger = MCPLogger(name)
    
    # Handler de consola
    console_handler = ConsoleLogHandler(console_level)
    logger.add_handler(console_handler)
    
    # Handler de archivo
    file_handler = FileLogHandler(log_file, file_level)
    logger.add_handler(file_handler)
    
    return logger

# Instancia global del logger
mcp_logger = setup_mcp_logger()
