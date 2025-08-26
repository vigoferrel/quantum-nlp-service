@echo off
chcp 65001 >nul
echo 🚀 INICIANDO SISTEMA QBTC
echo ================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.8+
    pause
    exit /b 1
)

REM Verificar si el virtual environment existe
if not exist ".venv" (
    echo ⚠️ Virtual environment no encontrado. Creando...
    python -m venv .venv
)

REM Activar virtual environment
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
echo 📦 Verificando dependencias...
python install_dependencies.py

REM Iniciar el sistema
echo 🚀 Iniciando sistema QBTC...
python start_simple.py

pause
