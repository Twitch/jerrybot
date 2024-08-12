#!/usr/bin/env python3

import discord
from discord.ext import commands
import os

# Bot configuration
JERRYBOT_TOKEN = os.getenv('JERRYBOT_TOKEN')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
JERRYBOT_DEBUG = os.getenv('JERRYBOT_DEBUG', 'False').lower() == 'true'
SERVER_ID = os.getenv('SERVER_ID')


# Beware some type issues sckank found on Win11. Maybe.
if isinstance(SERVER_ID, str):
   try:
      SERVER_ID = int(SERVER_ID)
   except:
      print("Could not convert the SERVER_ID to an int. It sucks")
      print(f"SERVER_ID is a {type(SERVER_ID)}")


# Set up intents
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

def log(message):
    if JERRYBOT_DEBUG:
        print(message)

async def find_channel_by_name(guild, channel_name):
    return discord.utils.get(guild.channels, name=channel_name)

async def duplicate_channel():
    guild = bot.get_guild(SERVER_ID)
    if not guild:
        log(f"Error: Could not find server with ID {SERVER_ID}")
        return

    original_channel = await find_channel_by_name(guild, CHANNEL_NAME)
    if not original_channel:
        log(f"Error: Could not find channel with name {CHANNEL_NAME}")
        return

    try:
        # Create a new channel with the same settings
        new_channel = await guild.create_text_channel(
            name=f"{original_channel.name}_temp",
            category=original_channel.category,
            position=original_channel.position,
            topic=original_channel.topic,
            slowmode_delay=original_channel.slowmode_delay,
            nsfw=original_channel.nsfw,
            overwrites=original_channel.overwrites
        )

        log(f"Created new channel: {new_channel.name}")

        # Delete the original channel
        await original_channel.delete()
        log(f"Deleted original channel: {original_channel.name}")

        # Rename the new channel to match the original
        await new_channel.edit(name=original_channel.name)
        log(f"Renamed new channel to: {new_channel.name}")

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
