@echo off
:: Check if Python is already installed
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo Python is already installed.
    pause
    exit /b
)

:: Set Python installation URL (latest version)
set PYTHON_URL=https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

:: Set download directory
set DOWNLOAD_DIR=%TEMP%\python_installer

:: Create directory to store the installer
if not exist %DOWNLOAD_DIR% mkdir %DOWNLOAD_DIR%

:: Download Python installer
echo Downloading Python...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%PYTHON_URL%', '%DOWNLOAD_DIR%\python_installer.exe')"

:: Run the installer silently with options
echo Installing Python...
start /wait %DOWNLOAD_DIR%\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

:: Cleanup
del %DOWNLOAD_DIR%\python_installer.exe
echo Python installation complete.

pause
