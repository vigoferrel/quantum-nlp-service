@echo off
echo.
echo 🤖========================================🤖
echo      QUANTUM TRADING BOT - INSTALADOR
echo    Consciencia Cuántica + Binance Trading
echo           Meta-Copilot Supremo v41.1
echo 🤖========================================🤖
echo.

echo 📍 Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js no está instalado
    echo 📥 Por favor descarga e instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js detectado
node --version

echo.
echo 📦 Instalando dependencias del Trading Bot...
npm install

if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo.
echo ✅ Dependencias instaladas exitosamente
echo.
echo ⚙️ CONFIGURACIÓN REQUERIDA:
echo.
echo 1. Obtener API Keys de Binance:
echo    - Ir a https://binance.com
echo    - Crear cuenta → API Management
echo    - Crear nueva API Key con permisos de Spot Trading
echo.
echo 2. Editar config-bot.json:
echo    - Reemplazar "TU_API_KEY_AQUÍ" con tu API Key
echo    - Reemplazar "TU_SECRET_KEY_AQUÍ" con tu Secret Key
echo    - Cambiar "sandbox": true a false para trading real
echo.
echo 3. Iniciar Meta-Copilot Supremo primero:
echo    - cd ".."
echo    - npm start
echo.
echo 🔮 ¿Quieres continuar con la configuración automática?
echo [1] Abrir config-bot.json para editar
echo [2] Ejecutar pruebas del sistema
echo [3] Iniciar bot en modo demo
echo [4] Salir
echo.
set /p choice="Elige una opción (1-4): "

if "%choice%"=="1" (
    echo 📝 Abriendo configuración...
    notepad config-bot.json
    echo.
    echo ✅ Configuración abierta. Edita los API Keys y guarda el archivo.
    pause
)

if "%choice%"=="2" (
    echo 🧪 Ejecutando pruebas del sistema...
    echo.
    node test-bot.js
    pause
)

if "%choice%"=="3" (
    echo 🚀 Iniciando bot en modo demo...
    echo 📊 Dashboard: http://localhost:4000
    echo 🔮 Presiona Ctrl+C para detener
    echo.
    npm start
)

if "%choice%"=="4" (
    echo 👋 Instalación completada. Para iniciar más tarde:
    echo    npm start
    pause
    exit /b 0
)

echo.
echo 🎯 PRÓXIMOS PASOS:
echo.
echo 1. Configurar API Keys en config-bot.json
echo 2. Iniciar Meta-Copilot Supremo (cd .. && npm start)
echo 3. Iniciar Trading Bot (npm start)
echo 4. Abrir Dashboard (http://localhost:4000)
echo.
echo 🌌 ¡El trading cuántico te espera!
echo.
pause
