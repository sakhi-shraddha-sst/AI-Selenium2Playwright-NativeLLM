@echo off
title Selenium to Playwright converter by local LLM

echo 🚀 Initializing Selenium to Playwright converter by local LLM...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install it to continue.
    pause
    exit /b 1
)

:: Check for Flask
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing dependencies (Flask, requests)...
    pip install flask requests
)

:: Start Backend
echo ⚙️ Starting Backend Server...
start /b python app.py

:: Wait for server
timeout /t 3 /nobreak >nul

:: Open UI
echo 🌐 Opening UI...
start http://localhost:5001

echo ✅ System running. Close this window to stop.
pause
