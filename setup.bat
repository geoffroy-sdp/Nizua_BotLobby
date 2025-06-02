@echo off
echo.
echo 
===================================
Initializing the environment...
echo ===================================

:: Vérifie si python est installé

where python >nul 2>nul
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH.
    pause
    exit /b 1
)

:: crée un .venv
python -m venv .venv

:: active le .venv
 call .venv\Scripts\activate.bat

:: met a jour pip
echo.
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip

:: installe les dépendances
pip install customtkinter vgamepad

echo.
echo ====================================
echo Environnement initialisé avec succès.
echo ====================================
pause