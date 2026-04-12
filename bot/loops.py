import datetime
import os
import random
import logging
import discord
from discord.ext import tasks
from .bot_instance import bot


logger = logging.getLogger(__name__)


@tasks.loop(time=datetime.time(hour=9, minute=0))
async def daily_pistouche():
    logger.info("daily_pistouche triggered")

    # Retrieving channel
    channel_id = os.getenv("DISCORD_CHANNEL")
    channel = bot.get_channel(int(channel_id)) if channel_id else None

    if channel is None:
        logger.debug("Channel not found in cache, fetching from API...")
        try:
            channel = await bot.fetch_channel(int(channel_id))
            logger.info(f"Channel fetched successfully: {channel_id}")
        except Exception as e:
            logger.error(f"Failed to fetch channel {channel_id}: {e}")
            return
    else:
        logger.debug(f"Channel retrieved from cache: {channel_id}")

    # Random roll
    roll = random.randint(1, 50)
    logger.debug(f"Roll result: {roll}")

    if roll == 1:
        message = "LEGENDARY PULL! YOU GOT A SECRET DOG"
        folder_path = os.path.join(os.path.dirname(__file__), "../pic/secret")
        logger.info("Secret dog triggered!")
    else:
        message = ""
        folder_path = os.path.join(os.path.dirname(__file__), "../pic")

    logger.debug(f"Using folder: {folder_path}")

    # Validate folder
    if not os.path.exists(folder_path):
        logger.error(f"Folder does not exist: {folder_path}")
        return

    images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not images:
        logger.warning(f"No images found in folder: {folder_path}")
        return

    image_file = random.choice(images)
    image_path = os.path.join(folder_path, image_file)

    logger.info(f"Selected image: {image_file}")

    # Sending message
    try:
        await channel.send(
            content=message,
            file=discord.File(image_path)
        )
        logger.info(f"Sent image successfully: {image_file}")
    except Exception:
        logger.exception(f"Failed to send image: {image_file}")
