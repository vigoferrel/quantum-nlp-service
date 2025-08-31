@echo off
echo ==============================================
echo    LOCALGPT MEJORADO - INICIADOR AUTOMATICO
echo ==============================================
echo.

cd /d "%~dp0"

echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado. Instala Python 3.8 o superior.
    pause
    exit /b 1
)

echo [2/5] Verificando dependencias...
python -c "import flask, requests, sqlite3" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias necesarias...
    pip install flask requests werkzeug
)

echo [3/5] Verificando estructura de directorios...
if not exist "localGPTUI\static" mkdir "localGPTUI\static"
if not exist "localGPTUI\static\css" mkdir "localGPTUI\static\css"
if not exist "localGPTUI\static\js" mkdir "localGPTUI\static\js"
if not exist "localGPTUI\uploads" mkdir "localGPTUI\uploads"

echo [4/5] Preparando archivos...
if not exist "localGPTUI\static\favicon.ico" (
    echo. > "localGPTUI\static\favicon.ico"
)

echo [5/5] Iniciando LocalGPT UI Mejorado...
echo.
echo =====================================================
echo   LocalGPT UI se iniciara en: http://127.0.0.1:5111
echo =====================================================
echo.
echo Caracteristicas del UI Mejorado:
echo  ✓ Modo offline automatico
echo  ✓ Manejo de errores mejorado  
echo  ✓ Interfaz mas intuitiva
echo  ✓ Estadisticas en tiempo real
echo  ✓ Soporte para multiples formatos
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python localGPTUI\localGPTUI_fixed.py --port 5111 --host 127.0.0.1

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo iniciar el servidor mejorado.
    echo Intentando con el servidor original...
    python localGPTUI\localGPTUI.py --port 5111 --host 127.0.0.1
)

pause
