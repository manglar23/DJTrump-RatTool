import discord
import threading 
from discord.ext import commands
import os
 
def run_command(command, results, index):
    try:
        result = os.popen(command).read()
        if "The operation completed successfully" in result or "Operation Successful" in result:
            results[index] = f"{command} >> success"
        else:
            results[index] = f"{command} >> error: {result.strip()}"
    except Exception as e:
        results[index] = f"{command} >> error: {str(e)}"

async def reagentc(ctx, action: str = None):
    if action is None:
        await ctx.send("Please specify 'on' or 'off' to enable or disable reagentc.")
        return
    commands_to_run = []
    results = [None] * 2 
    if action.lower() == 'on':
        commands_to_run = [
            'reagentc /enable',
            'bcdedit /set {default} recoveryenabled Yes',
            'bcdedit /set {bootmgr} displaybootmenu Yes'
        ]
    elif action.lower() == 'off':
        commands_to_run = [
            'reagentc /disable',
            'bcdedit /set {default} recoveryenabled No',
            'bcdedit /set {bootmgr} displaybootmenu no'
        ]
    else:
        await ctx.send("Invalid action. Use 'on' or 'off'.")
        return
    threads = []
    for i, command in enumerate(commands_to_run):
        t = threading.Thread(target=run_command, args=(command, results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    result_messages = "\n".join([result for result in results if result is not None])
    embed = discord.Embed(
        title=f"Reagentc {action.capitalize()}ed",
        description=f"{result_messages}",
        color=discord.Color.green() if action.lower() == 'on' else discord.Color.red()
    )
    embed.set_footer(text="System Control Bot")
    await ctx.send(embed=embed)