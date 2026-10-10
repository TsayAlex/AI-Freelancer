@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")
echo =======================================================
echo QA FACTORY v1.3 - STATIC AUTOPILOT + RELEASE GATE
echo Put owned ZIP archives into QA_INBOX.
echo Разместите ZIP проектов в QA_INBOX.
echo Press Ctrl+C to stop. / Ctrl+C - остановить.
echo =======================================================
%PY% qa_pipeline.py watch --inbox QA_INBOX --output QA_RESULTS --interval 30
if errorlevel 1 pause
