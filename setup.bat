@echo off
SETLOCAL ENABLEEXTENSIONS
color 0A

echo.
echo ===================================
echo Initializing the environment...
echo ===================================
echo.

:: Crée un dossier temporaire
set "TEMP_DIR=%TEMP%\git_python_install"
mkdir "%TEMP_DIR%" >nul 2>&1

:: Vérifie si Python est installé
where python >nul 2>nul
if errorlevel 1 (
    echo [INFO] Python n'est pas installé. Téléchargement de Python 3.12.1...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe' -OutFile '%TEMP_DIR%\python_installer.exe'"
    if not exist "%TEMP_DIR%\python_installer.exe" (
        echo [ERREUR] Échec du téléchargement de Python.
    )
    echo [INFO] Installation de Python...
    "%TEMP_DIR%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if errorlevel 1 (
        echo [ERREUR] L'installation de Python a échoué.
        pause
        exit /b 1
    )
)

:: Vérifie si Git est installé
where git >nul 2>nul
if errorlevel 1 (
    echo [INFO] Git n'est pas installé. Téléchargement de Git...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe' -OutFile '%TEMP_DIR%\git_installer.exe'"
    if not exist "%TEMP_DIR%\git_installer.exe" (
        echo [ERREUR] Échec du téléchargement de Git.
    )
    echo [INFO] Installation de Git...
    "%TEMP_DIR%\git_installer.exe" /VERYSILENT /NORESTART
    if errorlevel 1 (
        echo [ERREUR] L'installation de Git a échoué.
        pause
        exit /b 1
    )
)

:: Clone le repo
echo.
echo [INFO] Clonage du dépôt...
git clone https://github.com/geoffroy-sdp/Nizua_BotLobby >nul 2>&1
if not exist "Nizua_BotLobby" (
    echo [ERREUR] Le clonage du dépôt a échoué.
    pause
    exit /b 1
)
echo [INFO] Dépôt cloné avec succès.

:: Se déplace dans le dossier
cd Nizua_BotLobby || (
    echo [ERREUR] Impossible d'entrer dans le dossier du projet.
    pause
    exit /b 1
)
echo [INFO] Navigation vers le répertoire du projet réussie.

:: Vérifie Python encore une fois
where python >nul 2>nul
if errorlevel 1 (
    echo [ERREUR] Python n'est toujours pas détecté après l'installation.
    pause
    exit /b 1
)

:: Crée un environnement virtuel
echo [INFO] Création de l'environnement virtuel...
python -m venv .venv
if not exist ".venv\Scripts\activate.bat" (
    echo [ERREUR] L'environnement virtuel n'a pas été créé.
    pause
    exit /b 1
)

:: Active l'environnement virtuel
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel.
    pause
    exit /b 1
)

:: Mise à jour de pip
echo.
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERREUR] Échec de la mise à jour de pip.
    pause
    exit /b 1
)

:: Installation des dépendances
echo.
echo [INFO] Installation des dépendances Python...
pip install customtkinter vgamepad
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation des dépendances.
    pause
    exit /b 1
)

echo.
echo ====================================
echo Environnement initialisé avec succès.
echo ====================================
echo.

:: Lancement auto de start.bat
if exist "start.bat" (
    echo [INFO] Lancement de start.bat...
    start /B start.bat
) else (
    echo [ERREUR] start.bat n'existe pas dans le répertoire.
    pause
    exit /b 1
)

pause
