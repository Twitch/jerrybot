#!/usr/bin/env python3

import discord
from discord.ext import commands
import os
import re
import datetime
from pathlib import Path


# Check for existing environment variables, prompt user for anything that's missing
# Note: This doesn't account for the fact that the default channel name isn't needed after the
# initial instantiation, because the name is stored inside of the curr-name file. 
# to-do or something.
def get_env(var_name, default=None, lower=False):
    val = os.getenv(var_name)
    if val is None:
        if default is not None:
            val = default
        else:
            print(f"There is no environment variable set for {var_name}. You should set this persistently with the following command:")
            print(f"export {var_name}=your_value")
            print(f"Otherwise you will be asked to provide these values each time the script is executed.")
            val = input(f"Please provide a value for {var_name}: ")
    if lower:
        val = val.lower()
        os.environ[var_name] = val
    return val

# Bot configuration
JERRYBOT_TOKEN = get_env('JERRYBOT_TOKEN')
JERRYBOT_SERVER_ID = get_env('JERRYBOT_SERVER_ID')
JERRYBOT_NAMES_PATH = get_env('JERRYBOT_NAMES_PATH', os.getcwd())
JERRYBOT_DEBUG = get_env('JERRYBOT_DEBUG', 'False', True)
JERRYBOT_DEFAULT_NAME = get_env('JERRYBOT_DEFAULT_NAME', None, True)

# Beware some type issues sckank found on Win11. Maybe.
if isinstance(JERRYBOT_SERVER_ID, str):
   try:
      JERRYBOT_SERVER_ID = int(JERRYBOT_SERVER_ID)
   except:
      log("Could not convert the SERVER_ID to an int. It sucks")
      log(f"JERRYBOT_SERVER_ID is a {type(JERRYBOT_SERVER_ID)}")

# Set up intents
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

'''
Adding rudimentary channel name rotation, sloppily using files for state in case the host system is hit by a struggle bus
'''

# Discord happily accepts crazy names and shortens them to single dashes for you.
# This can lead to the current channel state file and the actual channel name being out of sync
# Trying to fix that by trimming/fixing the name before we try to set it.
# to-do: Go find the actual channel name that was set via the channel objects and write that to the state file
# but this check still makes sense to leave.
def friendly_name(content):
    content = re.sub(r'\s+', '-', content)
    content = re.sub(r'-+', '-', content)
    return content

# Fetch the new channel name from new-names list (grab from top) and remove that line once read.
# Return NoneType if the file is empty, the name code needs to check for this and insert the default name if NoneType is returned
def get_new_name():
    try:
        file_path = os.path.join(JERRYBOT_NAMES_PATH, "new-names")
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            if not lines:
                log(f"Error: File is empty: {file_path}")
                return None
            top_line = lines[0].strip(" \t\n-#")
            file.seek(0)
            file.writelines(lines[1:])
            file.truncate()
        return friendly_name(top_line)
    except FileNotFoundError:
        log(f"Error: File not found: {file_path}")
        return None

# Check the current channel name, at least according to the state file/env var
async def get_curr_name():
    try:
        file_path = os.path.join(JERRYBOT_NAMES_PATH, "curr-name")
        log(f"curr-file is {file_path}")
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            if not lines:
                log(f"Error: Current name state file is empty: {file_path}, using your default: {JERRYBOT_DEFAULT_NAME}")
                current_name = JERRYBOT_DEFAULT_NAME.strip()
                return current_name
            current_name = lines[0].strip()
        return current_name
    except FileNotFoundError:
        log(f"Error: Current name state file not found: {file_path}")
        return None

# Write to file, used to write both the current name to currname (for sloppy state purposes) and to the used names list, 
# mostly for funsies.
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
    guild = bot.get_guild(JERRYBOT_SERVER_ID)
    if not guild:
        log(f"Error: Could not find server with ID {JERRYBOT_SERVER_ID}")
        return

# Get the current channel name from state file, or sub in the environment variable's default value
    current_channel = await get_curr_name()
    original_channel = await find_channel_by_name(guild, current_channel)
    if not original_channel:
        log(f"Error: Could not find channel with name {current_channel}")
        return

    try:
        # Get the new name modifier
        name_insert = get_new_name()
        if name_insert is None:
            new_name = JERRYBOT_DEFAULT_NAME
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
        file_write(os.path.join(JERRYBOT_NAMES_PATH, "used-names"), f"Cleaning up {original_channel.name} at {get_time()}", "a")

        # Delete the original channel
        await original_channel.delete()
        log(f"Deleted original channel: {original_channel.name}")

        # Rename the new channel to match the original
        await new_channel.edit(name=new_name)
        log(f"Renamed new channel to: {new_name}")

        # Overwrite the curr_name file with the new current channel name for the next run
        file_write(os.path.join(JERRYBOT_NAMES_PATH, "curr-name"), new_name, "w")

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
