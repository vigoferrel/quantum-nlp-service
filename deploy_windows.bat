@echo off
REM 🚀 VIGOLEONROCKS - Deployment Script para Windows
REM Configurado para: srv984842.hstgr.cloud (72.60.61.49)

echo 🚀 VIGOLEONROCKS - Deployment para VPS
echo 📍 VPS: srv984842.hstgr.cloud (72.60.61.49)
echo 🔗 Dokploy: http://72.60.61.49:3000
echo ────────────────────────────────────────────────────────────────

REM Configurar variables de entorno
set DOKPLOY_API_TOKEN=ZXMnrmGIywiZwTVTRKuQwAhiuSAgxzXnJSGBDNIWdnPSdjVFvFJYpFpQmvTiIygK
set POSTGRES_PASSWORD=quantum2024
set SECRET_KEY=vigoleonrocks_human_2024_secure_key
set OPENROUTER_API_KEY=

echo ✅ Variables de entorno configuradas
echo 🔑 API Token: %DOKPLOY_API_TOKEN%
echo 🗄️ PostgreSQL Password: %POSTGRES_PASSWORD%
echo 🔐 Secret Key: %SECRET_KEY%

REM Verificar que Python esté disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Ejecutar el script de deployment
echo.
echo 🚀 Iniciando deployment...
echo.
python deploy_vps.py

REM Verificar resultado
if errorlevel 1 (
    echo.
    echo ❌ Deployment falló
    echo Revisa los logs arriba para más detalles
) else (
    echo.
    echo 🎉 Deployment completado exitosamente!
    echo.
    echo 📍 URL de la aplicación: http://72.60.61.49
    echo 🔗 Dashboard Dokploy: http://72.60.61.49:3000
    echo 📊 API Status: http://72.60.61.49/api/status
    echo 🌐 Dominio: https://vigoleonrocks.com (después de DNS)
)

echo.
echo Presiona cualquier tecla para continuar...
pause >nul