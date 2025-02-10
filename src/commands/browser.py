from webbrowser import open
import discord
async def search(ctx, *, query):
    url = f"https://www.bing.com/search?q={'+'.join(query.split())}"
    open(url)
    embed = discord.Embed(title="Search", description=f"Searching for: `{query}`", color=discord.Color.blue())
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.send(embed=embed)
async def openurl(ctx, url):
    open(url)
    embed = discord.Embed(title="Opening URL", description=f"[{url}]({url})", color=discord.Color.green())
    await ctx.send(embed=embed)