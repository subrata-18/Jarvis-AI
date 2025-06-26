@echo off
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Python is installed.
) else (
    echo Python is NOT installed.
    echo Installing Python...
    python-3.13.5-amd64.exe
)

python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install flask cohere python-dotenv

echo All dependencies are installed...

pause