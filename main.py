import os
from bot.bot_runner import bot


bot.run(os.getenv("DISCORD_TOKEN"))
