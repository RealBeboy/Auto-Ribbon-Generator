@echo off
echo Installing dependencies for your Python script...

REM Check if pip is available
python -m ensurepip --default-pip

REM Upgrade pip to the latest version
python -m pip install --upgrade pip

REM Install Pillow for image handling
python -m pip install pillow

REM tkinter is built-in, no installation needed, but notify the user
echo tkinter is built-in and requires no installation.

REM Notify completion
echo All dependencies have been installed. Press any key to exit...
pause
