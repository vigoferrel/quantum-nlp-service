@echo off
echo 🚀 VIGOLEONROCKS - Iniciando en segundo plano...
echo ===============================================

REM Lanzar el servidor Python en segundo plano
start "VIGOLEONROCKS Server" python vigoleonrocks_server.py

echo ✅ VIGOLEONROCKS lanzado en segundo plano
echo 🌍 Acceso: http://localhost:5000
echo 📊 APIs disponibles:
echo    • GET  /                     - Sitio web principal
echo    • GET  /api/status          - Estado del sistema  
echo    • GET  /api/metrics         - Métricas de rendimiento
echo    • POST /api/vigoleonrocks   - Procesamiento principal
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
