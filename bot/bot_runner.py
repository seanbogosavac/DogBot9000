import logging
import os
from logging.handlers import RotatingFileHandler
from .bot_instance import bot
from .loops import daily_pistouche


logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    # Log file path and create handler (with rotation)
    log_path = os.path.join(os.path.dirname(__file__), "log.txt")
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)

    # Configure logging
    logging.basicConfig(
        handlers=[handler],
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Start bot
    daily_pistouche.start()
    logger.info("DogBot9000 up and running")
