@echo off
echo === Launching Git Bash for VIGOLEONROCKS Deployment ===
echo.
echo Current directory: %CD%
echo Script: deploy-gitbash.sh
echo.
echo Instructions:
echo 1. Git Bash will open in this directory
echo 2. Run: chmod +x deploy-gitbash.sh
echo 3. Run: ./deploy-gitbash.sh
echo.
pause
echo Starting Git Bash...

REM Try different possible Git Bash locations
if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" --cd="%CD%"
) else if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
    "C:\Program Files (x86)\Git\bin\bash.exe" --cd="%CD%"
) else if exist "C:\Git\bin\bash.exe" (
    "C:\Git\bin\bash.exe" --cd="%CD%"
) else (
    echo Git Bash not found in common locations.
    echo Please open Git Bash manually and navigate to: %CD%
    echo Then run: chmod +x deploy-gitbash.sh && ./deploy-gitbash.sh
    pause
)
