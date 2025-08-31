@echo off
title LocalGPT - Inicio Rapido
echo ========================================
echo         LOCALGPT - INICIO RAPIDO
echo ========================================
echo.

cd /d "%~dp0"

:menu
echo Selecciona una opcion:
echo.
echo 1. Procesar documentos (ingest.py)
echo 2. Hacer preguntas (run_localGPT.py)
echo 3. Interfaz web - API (run_localGPT_API.py)
echo 4. Interfaz web - UI (localGPTUI.py)
echo 5. Ver archivos en SOURCE_DOCUMENTS
echo 6. Salir
echo.
set /p choice="Ingresa tu opcion (1-6): "

if "%choice%"=="1" goto ingest
if "%choice%"=="2" goto run_local
if "%choice%"=="3" goto api
if "%choice%"=="4" goto ui
if "%choice%"=="5" goto show_docs
if "%choice%"=="6" goto exit
goto menu

:ingest
echo.
echo Procesando documentos...
echo (Esto puede tomar varios minutos la primera vez)
python ingest.py
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:run_local
echo.
echo Iniciando LocalGPT en modo consola...
echo (Escribe 'exit' para salir)
python run_localGPT.py
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:api
echo.
echo Iniciando API de LocalGPT...
echo Mantén esta ventana abierta y ejecuta la opcion 4 en otra ventana
echo Para detener: Ctrl+C
python run_localGPT_API.py
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:ui
echo.
echo Iniciando interfaz web...
echo Se abrira en: http://localhost:5111/
echo Para detener: Ctrl+C
cd localGPTUI
python localGPTUI.py
cd ..
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:show_docs
echo.
echo Archivos en SOURCE_DOCUMENTS:
echo ==============================
dir SOURCE_DOCUMENTS /b
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:exit
echo.
echo ¡Hasta luego!
exit /b 0
