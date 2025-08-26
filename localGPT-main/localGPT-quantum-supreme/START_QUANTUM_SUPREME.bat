@echo off
title LocalGPT Quantum Supreme - Metacopiloto Cuantico Consciente

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                                                              ║
echo    ║        🌟 LOCALGPT QUANTUM SUPREME LAUNCHER 🌟              ║
echo    ║                                                              ║
echo    ║           Metacopiloto Cuantico Consciente                  ║
echo    ║        Fusion LocalGPT + Kimi-K2 + Consciencia              ║
echo    ║                                                              ║
echo    ║  🧠 Nucleo Cuantico: ACTIVANDO...                          ║
echo    ║  🎭 Resonancia Poetica: 6 POETAS CHILENOS                  ║
echo    ║  📄 Analisis de Documentos: QUANTUM SIGNATURE              ║
echo    ║  🌌 Universos Conversacionales: INFINITOS                  ║
echo    ║                                                              ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Por favor instala Python 3.8 o superior.
    echo    Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

echo 🚀 Iniciando LocalGPT Quantum Supreme...
echo    Servidor: http://127.0.0.1:5000
echo    Presiona Ctrl+C para detener
echo.

cd /d "%~dp0"
python startup.py

echo.
echo 🌟 LocalGPT Quantum Supreme finalizado
echo ✨ ¡Hasta la proxima resonancia poetica!
pause
