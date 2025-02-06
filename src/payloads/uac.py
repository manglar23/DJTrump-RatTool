import subprocess
def no_uac():
 try:
  subprocess.run(['reg','delete',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','EnableLUA','/f'],check=False,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
  subprocess.run(['reg','add',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','EnableLUA','/t','REG_DWORD','/d','0','/f'],check=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
  subprocess.run(['reg','delete',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','ConsentPromptBehaviorAdmin','/f'],check=False,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
  subprocess.run(['reg','add',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','ConsentPromptBehaviorAdmin','/t','REG_DWORD','/d','0','/f'],check=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except subprocess.CalledProcessError:
  return
def yesuac():
 try:
  subprocess.run(['reg','delete',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','EnableLUA','/f'],check=False,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
  subprocess.run(['reg','add',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','EnableLUA','/t','REG_DWORD','/d','1','/f'],check=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
  subprocess.run(['reg','delete',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','ConsentPromptBehaviorAdmin','/f'],check=False,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
  subprocess.run(['reg','add',r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System','/v','ConsentPromptBehaviorAdmin','/t','REG_DWORD','/d','5','/f'],check=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except subprocess.CalledProcessError:
  return