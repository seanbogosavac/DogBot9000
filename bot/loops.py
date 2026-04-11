import datetime
import os
import random
import discord
from discord.ext import tasks
from .bot_instance import bot


@tasks.loop(time=datetime.time(hour=9, minute=0))
async def daily_pistouche():
    # Retrieving channel and raising error if unavailable
    channel = bot.get_channel(os.getenv("DISCORD_CHANNEL"))
    if channel is None:
        try:
            channel = await bot.fetch_channel(os.getenv("DISCORD_CHANNEL"))
        except Exception as e:
            print(f"Failed to fetch channel: {e}")
            return
    
    # Choosing between regular dog or secret dog
    if random.randint(1, 50) == 1:
        message = "LEGENDARY PULL! YOU GOT A SECRET DOG"
        folder_path = folder_path = os.path.join(os.path.dirname(__file__), "../pic/secret")
    else:
        message = ""
        folder_path = folder_path = os.path.join(os.path.dirname(__file__), "../pic")

    # [Both cases] Picking random images in the chosen folder
    images = [f for f in os.listdir(folder_path)]
    if not images:
        print("No images found in ../pic")
        return
    image_path = os.path.join(folder_path, random.choice(images))
    
    # Sending actual message
    try:
        await channel.send(
            content=message,
            file=discord.File(image_path)
        )
        print(f"Sent image: {image_path}")
    except Exception as e:
        print(f"Failed to send image: {e}")
