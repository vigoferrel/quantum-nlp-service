@echo off
title LocalGPT - Instalador Definitivo
echo ========================================
echo  LOCALGPT - INSTALADOR DEFINITIVO
echo ========================================
echo.
echo Esta version NUNCA falla completamente
echo Siempre produce una version funcional
echo.
echo CARACTERISTICAS:
echo - Maneja TODOS los errores posibles
echo - Continua instalacion aunque fallen paquetes
echo - Se adapta automaticamente a Python 3.13
echo - Crea configuracion dinamica
echo - Scripts adaptativos segun disponibilidad
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo.
    echo SOLUCION:
    echo 1. Instala Python 3.10+ desde python.org
    echo 2. Marca "Add Python to PATH"
    echo 3. Reinicia y ejecuta de nuevo
    echo.
    pause
    exit /b 1
)

echo Python encontrado!
python --version
echo.

echo ========================================
echo     EJECUTANDO INSTALADOR DEFINITIVO
echo ========================================
echo.

python instalar_definitivo.py

echo.
echo ========================================
echo          INSTALACION FINALIZADA
echo ========================================
echo.
echo SIGUIENTES PASOS:
echo 1. python ingest_adaptive.py
echo 2. python run_adaptive.py
echo.
echo O usa el menu: iniciar.bat
echo.
pause
