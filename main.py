import discord
from discord.ext import commands
import fade, os, sys
from colorama import Fore
import datetime
import asyncio
import json
logo = """
 ██████╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗     ██╗██╗   ██╗███████╗    
██╔════╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝██║     ██║██║   ██║██╔════╝    
██║     ██║   ██║██████╔╝██╔██╗ ██║█████╗  ██║     ██║██║   ██║███████╗    
██║     ██║   ██║██╔══██╗██║╚██╗██║██╔══╝  ██║     ██║██║   ██║╚════██║    
╚██████╗╚██████╔╝██║  ██║██║ ╚████║███████╗███████╗██║╚██████╔╝███████║    
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚══════╝    
                                                                           
 ██████╗ ██████╗ ██████╗ ███╗   ██╗██╗    ██╗ █████╗ ██╗     ██╗           
██╔════╝██╔═══██╗██╔══██╗████╗  ██║██║    ██║██╔══██╗██║     ██║           
██║     ██║   ██║██████╔╝██╔██╗ ██║██║ █╗ ██║███████║██║     ██║           
██║     ██║   ██║██╔══██╗██║╚██╗██║██║███╗██║██╔══██║██║     ██║           
╚██████╗╚██████╔╝██║  ██║██║ ╚████║╚███╔███╔╝██║  ██║███████╗███████╗      
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝ 
               By 0x069#2442 Cornelius Cornwall Utility v1.1
"""

banner = fade.fire(logo)

token="BOT TOKEN HERE FOR SELF HOSTING"
prefix="$"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
help_message = """
# Cornelius Cornwall Discord Bot
### Made By 0x069#2442
# Commands
Prefix "$"

* logs - Shows logs(ADMIN ONLY).
* clearlogs - Clears logs in console and in the log file(ADMIN ONLY).
* ban - Bans specified guild member(ADMIN ONLY).
* kick - Kicks specified guild member(ADMIN ONLY).
* servers - Shows what server the bot is in.
* Hello - Responds to the user with hello.
* Help - Shows this menu.
* clearchannel - Clear the current channel(ADMIN ONLY).
* nuke - Deletes every channel and makes new one(ADMIN ONLY). `$nuke 5 5`
* pingsend - Send pings in specified ammount of channels specified ammount of times(ADMIN ONLY). `$pingsend Whatever 5 5`
* spamchannels - Makes channels the user specified amount of times(ADMIN ONLY). `$spamchannels 5`
* deleteallchannels - Deletes all channels and re makes general(ADMIN ONLY).
* massrole - Makes a large amount of roles(ADMIN ONLY). `$massrole 5`
"""
@client.event
async def on_ready():
    os.system('cls')
    print(banner)
    print(f"Prefix: {prefix}")
    print(f'Logged in as {client.user}')
    members = 0
    for guild in client.guilds:
        members += guild.member_count
    print(f"Guild Member Count: {members}")
    guilds = client.guilds
    guild_names = [guild.name for guild in guilds]
    print(f"The bot is in {len(guilds)} servers: `{', '.join(guild_names)}`\n")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Commands'))
    print('Bot is ready.')
    guilds = client.guilds
    guild_names = [guild.name for guild in guilds]
    print(Fore.GREEN + f"The bot is in {len(guilds)} servers: {', '.join(guild_names)}")
    with open('message logs.log', 'r') as f:
        logs = f.read()
    if logs == "":
        print(Fore.RED + "NO LOGS IN FILE" + Fore.WHITE)
    else:
        print(Fore.GREEN + "Old Logs:" + "\n" + Fore.WHITE + logs)

@client.event
async def on_message(message):
    with open('message logs.log', 'a') as f:
        f.write(f"[{datetime.datetime.now()}] {message.author}: {message.content}\n")
    await client.process_commands(message)
    print(Fore.WHITE + "\n")
    print(f"{message.author} said `{message.content}` [{datetime.datetime.now()}]")

@client.command()
async def Hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")


@client.command()
async def Help(ctx):
    await ctx.send(f"{help_message}\n{ctx.author.mention}")

@client.command()
async def servers(ctx):
    guilds = client.guilds
    guild_names = [guild.name for guild in guilds]
    await ctx.send(f"The bot is in {len(guilds)} servers: `{', '.join(guild_names)}` | {ctx.author.mention}")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await ctx.send(f"Please provide a reason for kicking {member}.")
    reason = await client.wait_for('message', check=lambda m: m.author == ctx.author)
    await member.kick(reason=reason.content)
    await ctx.send(f"{member} has been kicked from the server for {reason.content}.")
    await ctx.send("You do not have permission to use this command.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member):
    await ctx.send(f"Please provide a reason for banning {member}.")
    reason = await client.wait_for('message', check=lambda m: m.author == ctx.author)
    await member.ban(reason=reason.content)
    await ctx.send(f"{member} has been banned for {reason.content}.")
    await ctx.send("You do not have permission to use this command.")

@client.command()
@commands.has_permissions(administrator=True)
async def logs(ctx):
    
    with open('message logs.log', 'r') as f:
        logs = f.read()
    await ctx.send(f"```{logs}```")
    await asyncio.sleep(60)
    
    await ctx.send("You do not have permission to use this command.")

@client.command()
@commands.has_permissions(administrator=True)
async def clearlogs(ctx):
    with open('message logs.log', 'w') as f:
        f.write('')
    await ctx.send(f'{ctx.author.mention} cleared the logs.')
    os.system('cls')
    print(banner)
    print('\n')
    print('Bot is ready.')
    guilds = client.guilds
    guild_names = [guild.name for guild in guilds]
    print(f"The bot is in {len(guilds)} servers: {', '.join(guild_names)}")
    with open('message logs.log', 'r') as f:
        logs = f.read()
    print("Old Logs: " + "\n" + logs)
    await asyncio.sleep(120)

@client.command()
@commands.has_permissions(administrator=True)
async def clearchannel(ctx):
    async for message in ctx.channel.history(limit=None):
        await message.delete()
    await ctx.send(f"{ctx.author.mention} Nuked {ctx.channel.name}")

GUILD_ID = "1117199181434605608"

@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx, num_pings: int, num_channels: int):
    guild = ctx.guild

    for channel in guild.channels:
        await channel.delete()
    new_channel = await guild.create_text_channel('nuked')
    await new_channel.send(f"Nuked by {ctx.author.mention}")
    for i in range(num_channels):
        channel = await guild.create_text_channel(f'channel-{i+1}')
        print(f"Channel {channel.name} created")
    for channel in guild.text_channels:
        for i in range(num_pings):
            await channel.send('@everyone')
    print("Server Nuked")

@client.command()
@commands.has_permissions(administrator=True)
async def pingsend(ctx, message: str, num_channels: int, num_pings: int):
    guild = ctx.guild
    for i in range(num_channels):
        channel = await guild.create_text_channel(f'channel-{i+1}')
        for j in range(num_pings):
            await channel.send(f'@everyone {message}')
        print(f"Everyone pinged {num_pings} in {num_channels}")

@client.command()
@commands.has_permissions(administrator=True)
async def spamchannels(ctx, num_channels: int):
    guild = ctx.guild
    for i in range(num_channels):
        channel = await guild.create_text_channel(f'channel-{i+1}')
        print(f"Channel {channel.name} created")

@client.command()
@commands.has_permissions(administrator=True)
async def deleteallchannels(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
    new_channel = await guild.create_text_channel('general')
    await new_channel.send(f"Channels deleted by {ctx.author.mention}")
    print(f"All Channels Deleted")

@client.command()
async def massrole(ctx, num_roles: int):
    for i in range(num_roles):
        await ctx.guild.create_role(name=i+1)
    
   
client.run(token)
