import os
import random
import discord
from discord.ext import tasks
from .bot_instance import bot


@tasks.loop(hours=24)
async def daily_pistouche():
    channel = bot.get_channel(os.getenv("DISCORD_CHANNEL"))
    if channel is None:
        try:
            channel = await bot.fetch_channel(os.getenv("DISCORD_CHANNEL"))
        except Exception as e:
            print(f"Failed to fetch channel: {e}")
            return
    
    folder_path = os.path.join(os.path.dirname(__file__), "../pic")
    images = [f for f in os.listdir(folder_path)]
    
    if not images:
        print("No images found in ../pic")
        return
    
    # Pick random image
    image_path = os.path.join(folder_path, random.choice(images))
    
    try:
        await channel.send(file=discord.File(image_path))
        print(f"Sent image: {image_path}")
    except Exception as e:
        print(f"Failed to send image: {e}")
