from webbrowser import open
import random
import asyncio
async def search(ctx, *, query):
 await ctx.send(f"Searching for: {query}")
 open(f"https://www.bing.com/search?q={'+'.join(query.split())}")
async def openurl(ctx, url):
 await ctx.send(f"Opening URL: {url}")
 open(url)