#!/usr/bin/env python3
"""
Quick QBTC Setup - Configuración rápida del sistema
Guarda este archivo como: quick_setup.py
"""

import os
import json
from pathlib import Path

def create_qbtc_structure():
    """Crear estructura básica de QBTC"""
    
    base_dir = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED")
    
    # Estructura de directorios
    directories = [
        "conversations/sessions",
        "conversations/history", 
        "conversations/analytics",
        "quantum_states/coherence",
        "quantum_states/entanglement",
        "quantum_states/resonance",
        "models/kimi",
        "models/quantum",
        "models/hybrid",
        "data/training",
        "data/embeddings",
        "data/cache",
        "logs/system",
        "logs/conversations",
        "logs/quantum",
        "config",
        "backup",
        "tools",
        "docs"
    ]
    
    print("🚀 QBTC Quick Setup - Iniciando...")
    print("=" * 50)
    
    # Crear directorios
    print("📁 Creando estructura de directorios...")
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    # Crear archivo de configuración básico
    config_data = {
        "system": {
            "name": "QBTC Unified Quantum System",
            "version": "1.0.0",
            "author": "VIGOLEONROCKS",
            "base_dir": str(base_dir)
        },
        "quantum_engine": {
            "base_frequency": 432.0,
            "coherence_threshold": 0.7
        },
        "kimi_integration": {
            "model_path": str(base_dir / "Kimi-K2-main"),
            "enabled": (base_dir / "Kimi-K2-main").exists()
        }
    }
    
    print("\n⚙️ Creando configuración...")
    config_file = base_dir / "config" / "qbtc_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {config_file}")
    
    # Crear README básico
    readme_content = f"""# QBTC Unified Quantum System

## Directorio Base
{base_dir}

## Estructura Creada
- ✅ Conversaciones: {base_dir}/conversations/
- ✅ Estados Cuánticos: {base_dir}/quantum_states/
- ✅ Modelos: {base_dir}/models/
- ✅ Datos: {base_dir}/data/
- ✅ Logs: {base_dir}/logs/
- ✅ Configuración: {base_dir}/config/

## Próximos Pasos
1. Crea los archivos principales de código Python
2. Ejecuta el sistema completo
3. Configura la integración con Kimi-K2

## Archivos Necesarios
- qbtc_conversational_agent.py (Agente principal)
- qbtc_utilities.py (Utilidades)
- qbtc_config.py (Configuración avanzada)

Generado por Quick Setup v1.0
"""
    
    print("\n📝 Creando documentación...")
    readme_file = base_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"   ✅ {readme_file}")
    
    # Crear script de inicio básico
    start_script = f"""@echo off
echo.
echo =====================================
echo  QBTC Unified Quantum System
echo =====================================
echo.
echo Directorio: {base_dir}
echo.

cd /d "{base_dir}"

if exist "qbtc_conversational_agent.py" (
    echo Iniciando agente conversacional...
    python qbtc_conversational_agent.py
) else (
    echo.
    echo ⚠️  Archivo principal no encontrado
    echo Por favor, crea primero: qbtc_conversational_agent.py
    echo.
)

echo.
pause
"""
    
    print("\n🚀 Creando script de inicio...")
    start_file = base_dir / "start_qbtc.bat"
    with open(start_file, 'w') as f:
        f.write(start_script)
    print(f"   ✅ {start_file}")
    
    print("\n" + "=" * 50)
    print("🎉 QBTC Quick Setup Completado!")
    print("=" * 50)
    print(f"📁 Base: {base_dir}")
    print("📖 Lee: README.md para más información")
    print("🚀 Ejecuta: start_qbtc.bat para iniciar")
    print("\n✨ ¡Sistema listo para desarrollo!")

if __name__ == "__main__":
    create_qbtc_structure()
