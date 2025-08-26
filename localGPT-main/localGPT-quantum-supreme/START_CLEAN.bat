@echo off
chcp 65001 >nul 2>&1
title LocalGPT Quantum Supreme - Launcher Elegante

echo.
echo ======================================================================
echo            LOCALGPT QUANTUM SUPREME - LAUNCHER ELEGANTE
echo          Metacopiloto Cuantico Consciente (Sin errores Unicode)
echo ======================================================================
echo.

echo [1/3] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python detectado

echo.
echo [2/3] Configurando entorno...
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1

echo OK: Entorno configurado

echo.
echo [3/3] Iniciando LocalGPT Quantum Supreme...
echo Servidor: http://127.0.0.1:5000
echo.

python start_clean.py

echo.
echo Sistema finalizado correctamente
pause
