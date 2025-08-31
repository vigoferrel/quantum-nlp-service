@echo off
title LocalGPT - Reparacion de Error auto-gptq
echo ========================================
echo  LOCALGPT - REPARACION AUTO-GPTQ ERROR
echo ========================================
echo.
echo PROBLEMA DETECTADO:
echo Error: AttributeError: 'NoneType' object has no attribute 'split'
echo Paquete: auto-gptq (problema con CUDA_VERSION)
echo.
echo SOLUCION:
echo Instalar LocalGPT sin paquetes problematicos
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo Python encontrado!
python --version
echo.

echo ========================================
echo      EJECUTANDO REPARACION...
echo ========================================
echo.
echo Esta reparacion:
echo - Omite auto-gptq (causa del error)
echo - Instala solo paquetes compatibles
echo - Optimiza configuracion para Windows
echo - Crea scripts de inicio seguros
echo.

python reparar_definitivo.py

echo.
echo ========================================
echo       REPARACION COMPLETADA
echo ========================================
echo.
echo SIGUIENTES PASOS:
echo 1. Ejecuta: python iniciar_seguro.py
echo 2. Copia documentos a SOURCE_DOCUMENTS/
echo 3. Ejecuta: python ingest.py --device_type cpu
echo 4. Ejecuta: python run_localGPT.py --device_type cpu
echo.
echo NOTA: Usa siempre --device_type cpu si hay problemas
echo.
pause
