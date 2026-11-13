@echo off
title Load Balancer Project
cd /d "%~dp0"

echo Installing dependencies...
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo Starting Server 1...
start "Server 1" cmd /k "cd /d ""%~dp0"" && py server.py --name Server-1 --port 5001"

echo Starting Server 2...
start "Server 2" cmd /k "cd /d ""%~dp0"" && py server.py --name Server-2 --port 5002"

echo Starting Server 3...
start "Server 3" cmd /k "cd /d ""%~dp0"" && py server.py --name Server-3 --port 5003"

timeout /t 4 /nobreak >nul

echo Starting Load Balancer...
start "Load Balancer" cmd /k "cd /d ""%~dp0"" && py load_balancer.py"

timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:8000/dashboard"

echo Project started!
