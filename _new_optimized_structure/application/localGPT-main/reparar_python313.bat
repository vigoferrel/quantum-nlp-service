@echo off
title LocalGPT - Reparacion Python 3.13
echo ========================================
echo  LOCALGPT - REPARACION PYTHON 3.13
echo ========================================
echo.
echo PROBLEMA DETECTADO:
echo - Python 3.13 es muy nuevo
echo - Muchos paquetes ML no soportan 3.13 aun
echo - sentence-transformers y langchain fallan
echo.
echo SOLUCION:
echo - Instalar versiones mas nuevas/compatibles
echo - Configuracion conservadora (solo CPU)
echo - Modelos mas simples
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version
echo.

echo ========================================
echo      APLICANDO SOLUCION PYTHON 3.13
echo ========================================
echo.

python reparar_python313.py

echo.
echo ========================================
echo       INSTRUCCIONES IMPORTANTES
echo ========================================
echo.
echo 1. Si muchos paquetes fallaron:
echo    - Considera instalar Python 3.11
echo    - Es mas compatible con ML/AI
echo.
echo 2. Si algunos paquetes funcionan:
echo    - Usa solo modo CPU
echo    - python ingest.py --device_type cpu
echo    - python run_localGPT.py --device_type cpu
echo.
echo 3. Probar instalacion:
echo    python test_python313.py
echo.
pause
