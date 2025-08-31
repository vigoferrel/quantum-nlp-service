@echo off
echo.
echo ========================================
echo   VIGOLEONROCKS v2.0 - Website Launcher
echo ========================================
echo.
echo Launching VIGOLEONROCKS v2.0 website...
echo.

REM Open the HTML file directly
start "" "%~dp0index_v2_updated.html"

echo Website opened in your default browser!
echo.
echo Features available:
echo   - Interactive Quantum Demo
echo   - Real-time performance metrics
echo   - Academic paper v2.0 details
echo   - Multimodal AI capabilities showcase
echo.
echo Press any key to start a local HTTP server (optional)...
pause

REM Try to start a local server
echo.
echo Starting local HTTP server...
python -m http.server 8000
