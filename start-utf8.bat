@echo off
echo Setting up UTF-8 environment for Super Kamen Bot...

REM Set UTF-8 code page
chcp 65001 >nul

REM Set Python environment variables
set PYTHONIOENCODING=utf-8
set LANG=en_US.UTF-8
set LC_ALL=en_US.UTF-8

echo ✅ Environment configured for Japanese text support

REM Start the application
echo Starting Super Kamen Bot...
C:/Etudes/Super-Kamen-Bot/.venv/Scripts/python.exe -m streamlit run main.py --server.port 8503

pause
