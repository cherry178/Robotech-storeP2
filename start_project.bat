@echo off
REM Robotech Store - Complete Project Startup Script (Windows)
REM This script starts all necessary services for the Robotech Store project

echo 🚀 Starting Robotech Store Project...
echo ========================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Colors (Windows CMD doesn't support ANSI colors well, so we'll use plain text)

echo [INFO] Checking MySQL connection...
mysql -u root -e "SELECT 1;" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] MySQL is running and accessible
) else (
    echo [WARNING] MySQL is not accessible
    echo [INFO] Please ensure MySQL is installed and running
    echo [INFO] Start MySQL from Windows Services panel
    echo.
)

echo [INFO] Starting Flask backend server...

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo [INFO] Using virtual environment
    call venv\Scripts\activate.bat
    set PYTHON_CMD=python
) else (
    echo [INFO] Using system Python
    set PYTHON_CMD=python
)

REM Install/update dependencies
echo [INFO] Installing/updating dependencies...
pip install -r ..\requirements.txt >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Dependencies installed
) else (
    echo [WARNING] Could not install dependencies (continuing anyway)
)

REM Start Flask server
echo [INFO] Starting Flask server on port 8888...
start /B %PYTHON_CMD% app.py > ..\backend.log 2>&1

REM Wait a bit and check if it's running
timeout /t 5 /nobreak >nul

REM Check if port 8888 is in use
netstat -an | find "8888" | find "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Flask backend started successfully
    echo [INFO] Backend URL: http://localhost:8888
) else (
    echo [ERROR] Failed to start Flask backend
    goto :error
)

REM Go back to project root
cd ..

REM Check if there's a frontend to start
if exist package.json (
    echo [INFO] Frontend package.json found - starting frontend server...
    if exist node_modules (
        start /B npm start > frontend.log 2>&1
        timeout /t 10 /nobreak >nul
        netstat -an | find "3000" | find "LISTENING" >nul
        if %errorlevel% equ 0 (
            echo [SUCCESS] Frontend server started on port 3000
        )
    )
) else if exist index.html (
    echo [INFO] Starting simple HTTP server for frontend...
    start /B python -m http.server 7000 > frontend.log 2>&1
    timeout /t 3 /nobreak >nul
    netstat -an | find "7000" | find "LISTENING" >nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] Frontend HTTP server started on port 7000
    )
)

REM Show status
echo.
echo ========================================
echo [SUCCESS] Robotech Store is now running!
echo.
echo 🌐 Available URLs:
echo    Backend API:  http://localhost:8888
netstat -an | find "7000" | find "LISTENING" >nul
if %errorlevel% equ 0 (
    echo    Frontend:      http://localhost:7000
)
netstat -an | find "3000" | find "LISTENING" >nul
if %errorlevel% equ 0 (
    echo    Frontend:      http://localhost:3000
)
echo.
echo 📝 Test the following:
echo    Home:          http://localhost:8888/
echo    Products:      http://localhost:8888/products
echo    Cart:          http://localhost:8888/cart
echo    Orders:        http://localhost:8888/orders
echo.
echo [INFO] Press Ctrl+C in the command prompt to stop services
echo ========================================
echo.
echo [INFO] Services are running in the background.
echo [INFO] Close this window to keep them running.
pause
goto :eof

:error
echo.
echo [ERROR] Failed to start essential services.
echo [ERROR] Check the logs (backend.log, frontend.log) for details.
pause
exit /b 1
