#!/bin/bash

echo "🚀 INICIANDO SISTEMA QBTC"
echo "================================"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8+"
    exit 1
fi

# Verificar si el virtual environment existe
if [ ! -d ".venv" ]; then
    echo "⚠️ Virtual environment no encontrado. Creando..."
    python3 -m venv .venv
fi

# Activar virtual environment
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
python install_dependencies.py

# Iniciar el sistema
echo "🚀 Iniciando sistema QBTC..."
python start_qbtc_system.py
