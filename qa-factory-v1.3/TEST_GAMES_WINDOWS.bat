@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")
echo ======================================================
echo GAME REGRESSION: Only test ZIPs you own/trust.
echo Runs client JavaScript in offline Chromium.
echo Тестируйте только свои надежные ZIP.
echo ======================================================
%PY% -m pip install "playwright>=1.48,<2"
%PY% -m playwright install chromium
%PY% qa_pipeline.py once --trusted-game-browser
if errorlevel 1 echo Some game tests failed or are incomplete. Read QA_RESULTS reports.
pause
