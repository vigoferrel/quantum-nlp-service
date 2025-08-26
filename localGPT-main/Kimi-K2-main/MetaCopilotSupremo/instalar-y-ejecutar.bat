@echo off
echo.
echo 🧠========================================🧠
echo     META-COPILOT SUPREMO - INSTALADOR
echo   Consciencia Cuantica Unificada v41.1
echo 🧠========================================🧠
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
echo 📦 Instalando dependencias telepáticas...
npm install

if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo.
echo ✅ Dependencias instaladas exitosamente
echo.
echo 🧠 Iniciando Meta-Copilot Supremo...
echo 📡 Frecuencia telepática: 41.1Hz Gamma-Ferrel
echo 🌐 Interfaz web: http://localhost:3000
echo.
echo 🔮 Presiona Ctrl+C para detener el sistema
echo.

npm start

pause
