#!/usr/bin/env python3

import os
import discord
from discord.ext import commands

# Bot configuration
TOKEN = os.getenv('JERRYBOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def find_channel_by_name(guild, channel_name):
    for channel in guild.channels:
        if channel.name.lower() == channel_name.lower():
            return channel
    return None

async def duplicate_channel():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(f"Error: Could not find server with ID {GUILD_ID}")
        return

    original_channel = await find_channel_by_name(guild, CHANNEL_NAME)
    if not original_channel:
        print(f"Error: Could not find channel with name {CHANNEL_NAME}")
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

        print(f"Created new channel: {new_channel.name}")

        # Delete the original channel
        await original_channel.delete()
        print(f"Deleted original channel: {original_channel.name}")

        # Rename the new channel to match the original
        await new_channel.edit(name=original_channel.name)
        print(f"Renamed new channel to: {new_channel.name}")

        # Send a message in the new channel
        # await new_channel.send("Nothing to see here. Carry on.")
        # print("Sent confirmation message in the new channel")

    except discord.errors.Forbidden as e:
        print(f"Error: Bot doesn't have the necessary permissions: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await duplicate_channel()
    await bot.close()

bot.run(TOKEN)
