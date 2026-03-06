@echo off
title CS2 Report Tool - Calibration
echo ============================================
echo     CS2 REPORT TOOL - Calibration Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed!
    echo  Download it from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

:: Install dependencies
echo  Checking dependencies...
python -m pip install -r "%~dp0requirements.txt" --quiet
if errorlevel 1 (
    echo  ERROR: Failed to install dependencies.
    echo  Try running: python -m pip install pyautogui pynput
    pause
    exit /b 1
)
echo  Ready.
echo.

:: Launch calibration
python "%~dp0calibrate.py"
pause
