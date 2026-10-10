@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")
echo PRIVATE CLIENT PORTAL - LOCAL 127.0.0.1:8790
echo OPEN ON THIS COMPUTER ONLY / ТОЛЬКО ЛОКАЛЬНО
%PY% client_portal.py --port 8790
if errorlevel 1 pause
