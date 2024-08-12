#!/usr/bin/env python3

import discord
from discord.ext import commands
import os
import datetime
from pathlib import Path


# Bot configuration
JERRYBOT_TOKEN = os.getenv('JERRYBOT_TOKEN')
# CHANNEL_NAME = os.getenv('CHANNEL_NAME')
SERVER_ID = os.getenv('SERVER_ID')
JERRYBOT_DEBUG = os.getenv('JERRYBOT_DEBUG', 'False').lower() == 'true'
NAMES_PATH = os.getenv('NAMES_PATH', os.getcwd())


# Beware some type issues sckank found on Win11. Maybe.
if isinstance(SERVER_ID, str):
   try:
      SERVER_ID = int(SERVER_ID)
   except:
      log("Could not convert the SERVER_ID to an int. It sucks")
      log(f"SERVER_ID is a {type(SERVER_ID)}")

# Set up intents
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

'''
Adding rudimentary channel name rotation, sloppily using files for state in case the host system is hit by a struggle bus
'''
# Fetch the new channel name from new-names list (grab from top) and remove that line once read.
# Return NoneType if the file is empty, the name code needs to check for this and insert the default name if NoneType is returned
def get_new_name():
    try:
        file_path = os.path.join(NAMES_PATH, "new-names")
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            if not lines:
                log(f"Error: File is empty: {file_path}")
                return None
            top_line = lines[0].strip(" \t\n-#")
            file.seek(0)
            file.writelines(lines[1:])
            file.truncate()
        return top_line.replace(" ", "-")
    except FileNotFoundError:
        log(f"Error: File not found: {file_path}")
        return None

# Check the current channel name, at least according to the state file
def get_curr_name():
    try:
        file_path = os.path.join(NAMES_PATH, "curr-name")
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            if not lines:
                log(f"Error: Current name state file is empty: {file_path}")
                return None
            current_name = lines[0].strip()
        return current_name
    except FileNotFoundError:
        log(f"Error: Current name state file not found: {file_path}")
        return None

# Write to file, used to write both the current name to currname (for sloppy state purposes) and to the used names list, 
# mostly for funsies.
# os.path.join(NAMES_PATH, "new-names")

def file_write(file_path, content, mode):
    with open(file_path, mode) as file:
        file.write(content + '\n')

def log(message):
    if JERRYBOT_DEBUG:
        print(message)

def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def find_channel_by_name(guild, channel_name):
    return discord.utils.get(guild.channels, name=channel_name)

async def duplicate_channel():
    guild = bot.get_guild(SERVER_ID)
    if not guild:
        log(f"Error: Could not find server with ID {SERVER_ID}")
        return

    current_channel = get_curr_name()
    original_channel = await find_channel_by_name(guild, current_channel)
    if not original_channel:
        log(f"Error: Could not find channel with name {current_channel}")
        return

    try:
        # Get the new name modifier
        name_insert = get_new_name()
        if name_insert is None:
            new_name = "venting-deleted-nightly-stay-professional"
        else:
            new_name = "venting-" + name_insert + "-stay-professional"


        # Create a new channel with the same settings
        new_channel = await guild.create_text_channel(
            name=f"{original_channel.name}_sweeping",
            category=original_channel.category,
            position=original_channel.position,
            topic=original_channel.topic,
            slowmode_delay=original_channel.slowmode_delay,
            nsfw=original_channel.nsfw,
            overwrites=original_channel.overwrites
        )

        log(f"Created new channel: {new_channel.name}")

        # Write orignal name to used-names
        file_write(os.path.join(NAMES_PATH, "used-names"), "Cleaning up {original_channel.name} at {get_time()}", "a")

        # Delete the original channel
        await original_channel.delete()
        log(f"Deleted original channel: {original_channel.name}")

        # Rename the new channel to match the original
        await new_channel.edit(name=new_name)
        log(f"Renamed new channel to: {new_name}")

        # Overwrite the curr_name file with the new current channel name for the next run
        file_write(os.path.join(NAMES_PATH, "curr-name"), new_name, "w")

        # Send a message in the new channel (uncomment to send messages after tidying) 
        # message = "Nothing to see here. Carry on."
        # await new_channel.send(message)
        # log(f"Sent message in the new channel: {message}")

    except discord.errors.Forbidden as e:
        log(f"Error: Bot doesn't have the necessary permissions: {e}")
    except Exception as e:
        log(f"An error occurred: {e}")

@bot.event
async def on_ready():
    log(f'{bot.user} has connected to Discord!')
    await duplicate_channel()
    await bot.close()

bot.run(JERRYBOT_TOKEN)
