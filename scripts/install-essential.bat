@echo off
echo Super Kamen Bot - Essential Package Installer
echo ==============================================

echo Installing essential packages first...
python -m pip install -r requirements-minimal.txt

if errorlevel 1 (
    echo Error: Failed to install essential packages
    pause
    exit /b 1
)

echo.
echo Essential packages installed successfully!
echo.
echo You can now test basic functionality with:
echo   python demo.py
echo.
echo To install optional audio packages, run:
echo   pip install openai-whisper sounddevice soundfile
echo.
echo To install TTS (may have compatibility issues):
echo   pip install TTS
echo.

set /p choice="Start the demo now? (y/N): "
if /i "%choice%"=="y" (
    python demo.py
)

pause
