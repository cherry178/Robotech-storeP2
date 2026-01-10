@echo off

REM Robotech Store - Enhanced Startup Script
echo 🚀 Starting Robotech Store...
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if the comprehensive startup script exists
if exist start_project.bat (
    echo Using comprehensive startup script...
    call start_project.bat
) else (
    echo ⚠️  Comprehensive startup script not found.
    echo Starting basic HTTP server on port 8000...
    echo.
    python -m http.server 8000
    pause
)
