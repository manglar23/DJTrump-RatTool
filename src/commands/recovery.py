import discord
import threading 
from discord.ext import commands
import os
import subprocess
 
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