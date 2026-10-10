@echo off
chcp 65001 >nul
cd /d "%~dp0"
title ALEX AI QA FACTORY - Local App
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 server.py
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    python server.py
  ) else (
    echo Python 3 not installed. Install from https://www.python.org/downloads/windows/
    echo When installing, enable Add Python to PATH.
    pause
  )
)
if errorlevel 1 pause
