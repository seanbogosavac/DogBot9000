import logging
import os
from logging.handlers import RotatingFileHandler
from .bot_instance import bot
from .loops import daily_pistouche


# Configure logging
log_path = os.path.join(os.path.dirname(__file__), "log.txt")
handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@bot.event
async def on_ready():
    daily_pistouche.start()
    logging.info("DogBot9000 up and running")

