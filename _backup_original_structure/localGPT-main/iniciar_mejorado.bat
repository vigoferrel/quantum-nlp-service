@echo off
title LocalGPT - Inicio Mejorado
echo ========================================
echo         LOCALGPT - INICIO MEJORADO
echo ========================================
echo.
echo ✅ Interfaz web mejorada
echo ✅ Modo fallback automático
echo ✅ Manejo robusto de errores
echo ✅ Diseño moderno y responsivo
echo.

cd /d "%~dp0"

:menu
echo Selecciona una opcion:
echo.
echo 1. Interfaz Web Mejorada (RECOMENDADO)
echo 2. Procesar documentos (ingest.py)
echo 3. Chat en consola (run_localGPT.py)
echo 4. API Backend (run_localGPT_API.py)
echo 5. Ver archivos en SOURCE_DOCUMENTS
echo 6. Limpiar base de datos
echo 7. Salir
echo.
set /p choice="Ingresa tu opcion (1-7): "

if "%choice%"=="1" goto web_ui
if "%choice%"=="2" goto ingest
if "%choice%"=="3" goto console
if "%choice%"=="4" goto api
if "%choice%"=="5" goto show_docs
if "%choice%"=="6" goto clean_db
if "%choice%"=="7" goto exit
goto menu

:web_ui
echo.
echo 🚀 Iniciando interfaz web mejorada...
echo.
echo ✨ Características:
echo    - Diseño moderno y responsivo
echo    - Modo offline automático si API falla
echo    - Manejo robusto de errores
echo    - Soporte para múltiples formatos
echo.
echo 📍 Se abrirá en: http://localhost:5111
echo 🛑 Para detener: Ctrl+C
echo.
cd localGPTUI
python localGPTUI.py
cd ..
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:ingest
echo.
echo 📄 Procesando documentos...
echo (Esto puede tomar varios minutos la primera vez)
if exist "ingest_adaptive.py" (
    python ingest_adaptive.py
) else (
    python ingest.py
)
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:console
echo.
echo 💬 Iniciando LocalGPT en modo consola...
echo (Escribe 'exit' para salir)
if exist "run_adaptive.py" (
    python run_adaptive.py
) else (
    python run_localGPT.py
)
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:api
echo.
echo 🔌 Iniciando API Backend...
echo Esto debe ejecutarse ANTES de la interfaz web
echo Puerto: 5110
echo Para detener: Ctrl+C
python run_localGPT_API.py
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:show_docs
echo.
echo 📁 Archivos en SOURCE_DOCUMENTS:
echo ==============================
dir SOURCE_DOCUMENTS /b
echo.
echo Total de archivos:
dir SOURCE_DOCUMENTS /b | find /c /v ""
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:clean_db
echo.
echo 🧹 Limpiando bases de datos...
if exist "chroma_db" rmdir /s /q chroma_db
if exist "DB" rmdir /s /q DB
if exist "documents.db" del documents.db
if exist "fallback_documents.db" del fallback_documents.db
echo ✅ Bases de datos limpiadas
echo.
echo Presiona cualquier tecla para volver al menu...
pause
goto menu

:exit
echo.
echo 👋 ¡Hasta luego!
echo Gracias por usar LocalGPT
pause
exit /b 0
