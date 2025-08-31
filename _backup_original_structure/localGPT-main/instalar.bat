@echo off
echo ========================================
echo    INSTALADOR DE LOCALGPT PARA WINDOWS
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.10+ desde https://python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

echo.
echo Ejecutando instalador de Python...
python install_localgpt.py

echo.
echo Presiona cualquier tecla para continuar...
pause
