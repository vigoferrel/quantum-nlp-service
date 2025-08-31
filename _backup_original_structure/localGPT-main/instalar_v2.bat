@echo off
echo ========================================
echo    INSTALADOR LOCALGPT v2.0 - WINDOWS
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo SOLUCION:
    echo 1. Descarga Python desde: https://python.org
    echo 2. Durante instalacion marca "Add Python to PATH"
    echo 3. Reinicia el sistema
    echo 4. Ejecuta este instalador de nuevo
    echo.
    pause
    exit /b 1
)

echo Python encontrado!
python --version

echo.
echo ========================================
echo  EJECUTANDO INSTALADOR MEJORADO...
echo ========================================
echo.
echo Este instalador:
echo - Maneja errores comunes de Windows
echo - Instala paquetes de forma segura
echo - Evita problemas con CUDA/GPU
echo - Crea configuracion optimizada
echo.

python install_localgpt_fixed.py

echo.
echo ========================================
echo         INSTALACION FINALIZADA
echo ========================================
echo.
echo Proximos pasos:
echo 1. Ejecuta: iniciar.bat
echo 2. Selecciona "Procesar documentos"
echo 3. Luego "Hacer preguntas"
echo.
pause
