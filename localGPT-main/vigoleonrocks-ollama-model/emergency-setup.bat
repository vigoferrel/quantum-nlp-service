@echo off
REM VIGOLEONROCKS OLLAMA - CONFIGURACION DE EMERGENCIA
REM Script para crear modelo que funcione en sistemas con memoria limitada

echo ================================================================================
echo VIGOLEONROCKS OLLAMA - CONFIGURACION DE EMERGENCIA
echo Creando modelo minimo funcional para sistemas limitados
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

REM Eliminar modelos existentes
echo %INFO% Eliminando modelos anteriores...
ollama rm vigoleonrocks >nul 2>&1
ollama rm vigoleonrocks-ultra >nul 2>&1
ollama rm vigoleonrocks-lightweight >nul 2>&1
ollama rm vigoleonrocks-optimized >nul 2>&1

REM Crear modelo minimal
echo %INFO% Creando modelo VIGOLEONROCKS minimal (4K tokens)...
ollama create vigoleonrocks -f Modelfile-minimal

if errorlevel 1 (
    echo %ERROR% Error creando modelo minimal
    echo %INFO% Intentando con configuracion aun mas basica...
    
    REM Crear Modelfile temporal ultra-basico
    echo FROM llama3.2 > Modelfile-temp
    echo PARAMETER num_ctx 2048 >> Modelfile-temp
    echo PARAMETER num_predict 1024 >> Modelfile-temp
    echo PARAMETER num_batch 64 >> Modelfile-temp
    echo PARAMETER temperature 0.1 >> Modelfile-temp
    echo SYSTEM "Eres VIGOLEONROCKS, IA cuantico-cognitiva avanzada." >> Modelfile-temp
    
    ollama create vigoleonrocks -f Modelfile-temp
    del Modelfile-temp
    
    if errorlevel 1 (
        echo %ERROR% Error critico - no se puede crear modelo
        pause
        exit /b 1
    )
)

echo %SUCCESS% Modelo VIGOLEONROCKS creado exitosamente

REM Probar modelo con prompt muy simple
echo %INFO% Probando modelo con prompt basico...
echo Hola | ollama run vigoleonrocks

if errorlevel 1 (
    echo %ERROR% Error probando modelo
    echo %INFO% Modelo creado pero puede tener problemas de memoria
) else (
    echo %SUCCESS% Modelo funcionando correctamente
)

echo.
echo ================================================================================
echo VIGOLEONROCKS CONFIGURADO (MODO EMERGENCIA)
echo ================================================================================
echo Configuracion: Minimal (4K tokens o menos)
echo Memoria requerida: ~2-4GB
echo.
echo COMANDOS DISPONIBLES:
echo   ollama run vigoleonrocks                    # Ejecutar modelo
echo   echo "pregunta simple" ^| ollama run vigoleonrocks  # Prueba rapida
echo.
echo NOTA: Este es un modelo reducido para sistemas con memoria limitada.
echo Para mejor rendimiento, considera aumentar la RAM del sistema.
echo ================================================================================

pause