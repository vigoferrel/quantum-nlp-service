@echo off
title QBTC LocalGPT-WebAgent Sistema Unificado
color 0A
echo.
echo ========================================================================
echo                QBTC LocalGPT-WebAgent Sistema Unificado
echo ========================================================================
echo.
echo  🧠 LocalGPT: Busqueda privada en documentos locales
echo  🌍 WebAgent: Navegacion web inteligente y autonoma  
echo  🔄 Hibrido: Combina lo mejor de ambos mundos
echo.
echo  🔒 Privacidad Total + 🤖 IA Avanzada = 🚀 Sistema Definitivo
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

:menu
echo Selecciona una opcion:
echo.
echo 1. 🚀 Iniciar Sistema Unificado (Puerto 5112)
echo 2. 📊 Solo LocalGPT (Puerto 5111) 
echo 3. 🌐 Solo WebAgent (Puerto 5113)
echo 4. 📁 Abrir carpeta de documentos
echo 5. 🔧 Instalar dependencias
echo 6. 🧹 Limpiar base de datos
echo 7. 📖 Mostrar ayuda
echo 8. 🚪 Salir
echo.
set /p choice="Ingresa tu opcion (1-8): "

if "%choice%"=="1" goto unified
if "%choice%"=="2" goto localgpt
if "%choice%"=="3" goto webagent
if "%choice%"=="4" goto open_docs
if "%choice%"=="5" goto install_deps
if "%choice%"=="6" goto clean_db
if "%choice%"=="7" goto help
if "%choice%"=="8" goto exit
echo Opcion invalida. Intenta de nuevo.
goto menu

:unified
echo.
echo 🚀 Iniciando Sistema Unificado LocalGPT-WebAgent...
echo.
echo ✨ Caracteristicas disponibles:
echo    - Busqueda en documentos locales (LocalGPT)
echo    - Navegacion web inteligente (WebAgent)  
echo    - Modo hibrido combinado
echo    - Interfaz moderna y responsive
echo    - APIs REST completas
echo.
echo 📍 Accede en: http://localhost:5112
echo 📊 API Stats: http://localhost:5112/api/stats
echo 🛑 Para detener: Ctrl+C
echo.
python unified_app.py
echo.
echo Sistema unificado detenido.
pause
goto menu

:localgpt
echo.
echo 📚 Iniciando solo LocalGPT...
echo.
echo 📍 Accede en: http://localhost:5111
echo 🛑 Para detener: Ctrl+C
echo.
if exist "..\..\..\vigosueldo\localGPT-main\localGPTUI\localGPTUI.py" (
    cd ..\..\..\vigosueldo\localGPT-main\localGPTUI
    python localGPTUI.py
    cd "%~dp0"
) else (
    echo ❌ LocalGPT no encontrado en la ruta esperada
    echo Verifica que el proyecto LocalGPT este disponible
)
echo.
pause
goto menu

:webagent
echo.
echo 🌐 Iniciando solo WebAgent...
echo.
echo 📍 Accede en: http://localhost:5113
echo 🛑 Para detener: Ctrl+C
echo.
if exist "..\WebWalker\src\app.py" (
    cd ..\WebWalker\src
    streamlit run app.py --server.port 5113
    cd "%~dp0"
) else (
    echo ❌ WebAgent no encontrado en la ruta esperada
    echo Verifica que el proyecto WebAgent este disponible
)
echo.
pause
goto menu

:open_docs
echo.
echo 📁 Abriendo carpeta de documentos...
if not exist "SOURCE_DOCUMENTS" mkdir SOURCE_DOCUMENTS
explorer SOURCE_DOCUMENTS
echo.
echo ✅ Carpeta abierta. Copia tus documentos aqui.
echo Formatos soportados: PDF, TXT, DOC, DOCX, CSV, MD, PY, JS, HTML, CSS
echo.
pause
goto menu

:install_deps
echo.
echo 🔧 Instalando dependencias del sistema unificado...
echo.
echo Instalando paquetes de Python...
pip install -r requirements.txt
echo.
echo ✅ Dependencias instaladas.
echo.
pause
goto menu

:clean_db
echo.
echo 🧹 Limpiando bases de datos...
echo.
set /p confirm="¿Estas seguro? Esto eliminara todos los datos (s/N): "
if /i "%confirm%"=="s" (
    if exist "unified_documents.db" del unified_documents.db
    if exist "fallback_documents.db" del fallback_documents.db
    if exist "documents.db" del documents.db
    echo ✅ Bases de datos limpiadas.
) else (
    echo ❌ Operacion cancelada.
)
echo.
pause
goto menu

:help
echo.
echo 📖 AYUDA - Sistema Unificado LocalGPT-WebAgent
echo ================================================================
echo.
echo 🧠 LOCALGPT (Busqueda Local):
echo    - Sube documentos a SOURCE_DOCUMENTS/
echo    - Busca informacion de forma privada
echo    - Todo funciona offline
echo    - Formatos: PDF, TXT, DOC, CSV, MD, PY, JS, etc.
echo.
echo 🌐 WEBAGENT (Navegacion Web):
echo    - Explora sitios web de forma autonoma
echo    - Extrae informacion actualizada
echo    - Navega por enlaces y botones
echo    - Captura screenshots
echo.
echo 🔄 MODO HIBRIDO:
echo    - Combina busqueda local + web
echo    - Validacion cruzada de informacion
echo    - Resultados mas completos
echo.
echo 🎯 EJEMPLOS DE USO:
echo    Local: "Resume el documento sobre IA"
echo    Web: "Precio actual de Bitcoin en CoinGecko"
echo    Hibrido: "Compara datos locales con info web"
echo.
echo ⌨️ ATAJOS DE TECLADO:
echo    Ctrl+U: Subir archivos
echo    Ctrl+R: Actualizar pagina
echo    Escape: Enfocar busqueda
echo    1/2/3: Cambiar modo
echo.
echo 🔧 CONFIGURACION:
echo    Puerto unificado: 5112
echo    Base de datos: unified_documents.db
echo    Logs: Consola del navegador
echo.
pause
goto menu

:exit
echo.
echo 👋 ¡Gracias por usar el Sistema Unificado!
echo.
echo 🚀 Desarrollado por QBTC-VIGOLEONROCKS-UNIFIED
echo 💻 La proxima generacion de busqueda inteligente
echo.
echo ¿Te gusto el sistema? ⭐ Dale una estrella en GitHub!
echo.
pause
exit /b 0
