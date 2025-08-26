#!/usr/bin/env python3
"""
🔐 SISTEMA DE AUTENTICACIÓN API
Sistema de claves API para acceso externo a Vigoleonrocks
"""

import hashlib
import secrets
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class APIAuthSystem:
    """Sistema de autenticación API para Vigoleonrocks"""
    
    def __init__(self, keys_file: str = "api_keys.json"):
        self.keys_file = keys_file
        self.api_keys = {}
        self.load_keys()
    
    def load_keys(self):
        """Cargar claves API desde archivo"""
        try:
            with open(self.keys_file, 'r') as f:
                data = json.load(f)
                self.api_keys = data.get('keys', {})
            logger.info(f"✅ Cargadas {len(self.api_keys)} claves API")
        except FileNotFoundError:
            logger.info("📝 Archivo de claves API no encontrado, creando nuevo")
            self.create_default_keys()
        except Exception as e:
            logger.error(f"❌ Error cargando claves API: {e}")
            self.create_default_keys()
    
    def save_keys(self):
        """Guardar claves API en archivo"""
        try:
            data = {'keys': self.api_keys}
            with open(self.keys_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("✅ Claves API guardadas")
        except Exception as e:
            logger.error(f"❌ Error guardando claves API: {e}")
    
    def create_default_keys(self):
        """Crear claves API por defecto"""
        # Clave de prueba
        test_key = self.generate_api_key(
            user_name="Usuario de Prueba",
            user_email="test@vigoleonrocks.com",
            permissions=["text", "multimodal"],
            rate_limit=100
        )
        
        # Clave de desarrollador
        dev_key = self.generate_api_key(
            user_name="Desarrollador",
            user_email="dev@vigoleonrocks.com",
            permissions=["text", "multimodal", "quantum", "admin"],
            rate_limit=1000
        )
        
        self.save_keys()
    
    def generate_api_key(self, user_name: str, user_email: str, 
                        permissions: List[str], rate_limit: int = 100) -> str:
        """Generar nueva clave API"""
        
        # Generar clave API
        api_key = f"vk_live_{secrets.token_hex(32)}"
        
        # Crear registro de clave
        self.api_keys[api_key] = {
            "user_name": user_name,
            "user_email": user_email,
            "permissions": permissions,
            "rate_limit": rate_limit,
            "usage_count": 0,
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        logger.info(f"✅ Nueva clave API generada para {user_name}")
        return api_key
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validar clave API"""
        if api_key not in self.api_keys:
            return False
        
        key_data = self.api_keys[api_key]
        
        # Verificar si está activa
        if not key_data.get('is_active', True):
            return False
        
        # Verificar límite de uso
        if key_data.get('usage_count', 0) >= key_data.get('rate_limit', 100):
            return False
        
        # Incrementar uso
        key_data['usage_count'] = key_data.get('usage_count', 0) + 1
        key_data['last_used'] = datetime.now().isoformat()
        
        return True
    
    def check_permission(self, api_key: str, permission: str) -> bool:
        """Verificar permiso específico"""
        if not self.validate_api_key(api_key):
            return False
        
        key_data = self.api_keys[api_key]
        permissions = key_data.get('permissions', [])
        
        return permission in permissions or "admin" in permissions

# Instancia global
api_auth = APIAuthSystem()

def create_api_key_for_user(user_name: str, user_email: str, 
                           permissions: List[str] = ["text", "multimodal"],
                           rate_limit: int = 100) -> str:
    """Crear clave API para usuario externo"""
    return api_auth.generate_api_key(user_name, user_email, permissions, rate_limit)

def validate_api_request(api_key: str, required_permission: str) -> bool:
    """Validar solicitud API"""
    return api_auth.check_permission(api_key, required_permission)

if __name__ == "__main__":
    # Demo del sistema
    print("🔐 SISTEMA DE AUTENTICACIÓN API - DEMO")
    print("=" * 50)
    
    # Crear clave para usuario externo
    external_key = create_api_key_for_user(
        user_name="Usuario Externo",
        user_email="externo@empresa.com",
        permissions=["text", "multimodal"],
        rate_limit=50
    )
    
    print(f"✅ Clave API generada: {external_key}")
    
    # Validar clave
    if validate_api_request(external_key, "text"):
        print("✅ Permiso de texto validado")
    
    if validate_api_request(external_key, "quantum"):
        print("✅ Permiso cuántico validado")
    else:
        print("❌ Sin permiso cuántico")
    
    # Mostrar información
    # The original code had get_key_info, but it's not defined in the new_code.
    # For now, we'll just print the raw key data.
    print(f"📊 Información de clave (raw): {api_auth.api_keys.get(external_key)}")
    
    api_auth.save_keys()
