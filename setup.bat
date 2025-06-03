@echo off
SETLOCAL ENABLEEXTENSIONS
color 0A

echo.
echo 
===================================
Initializing the environment...
echo ===================================
echo.

:: crée un dossier temporaire
set "TEMP_DIR=%TEMP%\git_python_install"
mkdir "%TEMP_DIR%" >nul 2>&1

:: verifie si python est installé
where python >nul 2>nul
if errorlevel 1 (
    echo [INFO] Python isnt downloaded. Downloading python3.12.1
    powershell -Command "invoke-webrequest -uri 'https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe' -OutFile '%TEMP_DIR%\python_installer.exe'"
    echo [INFO] Downloading python3.12.1 installer...
    "%TEMP_DIR%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)

:: verifie si git est installer
where git >nul 2>nul
if errorlevel 1 (
    echo [INFO] Git isnt downloaded. Downloading git
    powershell -Command "Invoke-WebRequest -Uri https://github.Com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe -OutFile '%TEMP_DIR%\git_installer.exe'"
    echo [INFO] Downloading git installer...
    "%TEMP_DIR%\git_installer.exe" /VERYSILENT /NORESTART
)

:: clone le repo

echo.
echo [INFO] Cloning the repository...
git clone https://github.com/geoffroy-sdp/Nizua_BotLobby

:: verifie si il est cloner
if not exist "Nizua_BotLobby" (
    echo [ERREUR] Le clone du repository a echoue.
    pause
    exit /b 1
)

echo [INFO] Repository cloned successfully.

:: se deplace dans le dossier du projet
cd Nizua_BotLobby
echo [INFO] Navigating to the project directory...

:: Vérifie si python est installé apres l'installation
where python >nul 2>nul
if errorlevel 1 (
    echo [ERREUR] python isnt downloaded.
    pause
    exit /b 1
)

:: crée un .venv
python -m venv .venv

:: active le .venv
 call .venv\Scripts\activate.bat

:: met a jour pip
echo.
echo [INFO] Mise a jour de pip...
python -m pip install --upgrade pip

:: installe les dépendances
pip install customtkinter vgamepad

echo.
echo ====================================
echo Environnement initialise avec succes.
echo ====================================

::Lancement auto de start.bat
echo.
if exist "start.bat" (
    echo [INFO] Lancement de start.bat...
    start /B start.bat
) else (
    echo [ERREUR] start.bat n'existe pas.
    pause
    exit /b 1
)

pause