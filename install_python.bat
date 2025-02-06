@echo off
cls
set "url=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
set "installer=python-3.12.3-amd64.exe"
set "dir=%~dp0"

NET SESSION >nul 2>&1
if %errorlevel% NEQ 0 (
    echo This script is requesting elevated permissions...
    powershell -Command "Start-Process '%~0' -Verb runAs"
    exit /b
)
echo Downloading Python 3.12.3 installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%url%', '%dir%%installer%')"
echo Opening Python 3.12.3 installer...
start "" "%dir%%installer%"
pause