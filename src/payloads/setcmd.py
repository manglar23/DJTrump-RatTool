import subprocess
def nocmd():
 try:
  subprocess.run(["reg","add",r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System","/v","DisableCMD","/t","REG_DWORD","/d","1","/f"],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except subprocess.CalledProcessError as e:
  if e.returncode==1:return

def yescmd():
 try:
  subprocess.run(["reg","delete",r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System","/v","DisableCMD","/f"],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except subprocess.CalledProcessError as e:
  if e.returncode==1:return
