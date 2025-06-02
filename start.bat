@echo off
setlocal

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in the PATH.
    pause
    exit /b 1
)

:: active la venv si pas fait
call .venv\Scripts\activate.bat

echo.
echo ===================================
lanceur de l'application...
echo ===================================
python gui.py

pause