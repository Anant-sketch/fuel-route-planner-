@echo off
title Fuel Route Planner - Anant Sharma
cd /d "%~dp0"
echo ======================================================================
echo              FUEL ROUTE PLANNER - ANANT SHARMA
echo ======================================================================
echo.
echo Starting Django Server on http://127.0.0.1:8000 ...
echo Press Ctrl+C in this window to stop the server.
echo.
start http://127.0.0.1:8000/
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
pause
