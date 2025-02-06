import subprocess
def noreg():
    try:
        subprocess.Popen(
            ["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System", "/v", "DisableRegistryTools", "/t", "REG_DWORD", "/d", "1", "/f"],
            creationflags=subprocess.CREATE_NO_WINDOW, 
            shell=True
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return

def yesreg():
    try:
        subprocess.Popen(
            ["powershell", "-Command", "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'DisableRegistryTools' -Value 0"],
            creationflags=subprocess.CREATE_NO_WINDOW, 
            shell=True
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return
