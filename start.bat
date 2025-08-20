@echo off
echo Super Kamen Bot - Japanese AI Chatbot
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/downloads/
    pause
    exit /b 1
)

REM Check if Ollama is running
ollama list >nul 2>&1
if errorlevel 1 (
    echo Warning: Ollama is not running
    echo Please start Ollama first:
    echo   1. Install Ollama from https://ollama.ai/download
    echo   2. Run: ollama serve
    echo.
    set /p choice="Continue anyway? (y/N): "
    if /i not "%choice%"=="y" (
        exit /b 1
    )
)

REM Check if requirements are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing essential requirements...
    python -m pip install -r requirements-minimal.txt
    if errorlevel 1 (
        echo Error: Failed to install essential requirements
        echo.
        echo Try running: install-essential.bat
        pause
        exit /b 1
    )
)

REM Start the application
echo Starting Super Kamen Bot...
echo.
echo The web interface will open in your browser
echo Press Ctrl+C to stop the application
echo.

python -m streamlit run main.py

pause
