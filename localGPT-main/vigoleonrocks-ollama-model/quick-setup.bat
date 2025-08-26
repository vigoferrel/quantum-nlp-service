@echo off
REM VIGOLEONROCKS OLLAMA - CONFIGURACION RAPIDA Y SIMPLE
REM Script simplificado para crear modelo ultra-optimizado

echo ================================================================================
echo VIGOLEONROCKS OLLAMA - CONFIGURACION RAPIDA
echo Creando modelo ultra-optimizado con 1M tokens
echo ================================================================================

setlocal enabledelayedexpansion

set "SUCCESS=[SUCCESS]"
set "ERROR=[ERROR]"
set "INFO=[INFO]"

REM Verificar Ollama
echo %INFO% Verificando Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Ollama no esta instalado
    echo Descarga desde: https://ollama.ai
    pause
    exit /b 1
)

REM Verificar si Ollama esta ejecutandose
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo %INFO% Iniciando Ollama...
    start /b ollama serve
    timeout /t 5 /nobreak >nul
)

echo %SUCCESS% Ollama verificado

REM Eliminar modelo existente
echo %INFO% Eliminando modelo anterior si existe...
ollama rm vigoleonrocks >nul 2>&1

REM Crear modelo ultra-optimizado
echo %INFO% Creando modelo VIGOLEONROCKS ultra-optimizado...
ollama create vigoleonrocks -f Modelfile-ultra

if errorlevel 1 (
    echo %ERROR% Error creando modelo
    pause
    exit /b 1
)

echo %SUCCESS% Modelo VIGOLEONROCKS creado exitosamente

REM Probar modelo
echo %INFO% Probando modelo...
echo Hola VIGOLEONROCKS, confirma que funcionas correctamente. | ollama run vigoleonrocks

if errorlevel 1 (
    echo %ERROR% Error probando modelo
) else (
    echo %SUCCESS% Modelo funcionando correctamente
)

echo.
echo ================================================================================
echo VIGOLEONROCKS CONFIGURADO EXITOSAMENTE
echo ================================================================================
echo Configuracion: Ultra-optimizada (1M tokens)
echo.
echo COMANDOS DISPONIBLES:
echo   ollama run vigoleonrocks                    # Ejecutar modelo
echo   python run-tests.py                        # Ejecutar pruebas
echo.
echo EJECUTAR PRUEBAS:
echo   python run-tests.py                        # Prueba rapida
echo   python test-suite.py                       # Suite completa
echo   test-runner.bat quick                      # Prueba con script
echo ================================================================================

pause