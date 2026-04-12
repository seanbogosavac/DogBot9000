import logging
import os
from logging.handlers import RotatingFileHandler
from .bot_instance import bot
from .loops import daily_pistouche


# Fail fast if required folders are missing
base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
required = [os.path.join(base, "pic"), os.path.join(base, "pic", "secret")]

if not all(os.path.isdir(p) for p in required):
    logging.error(f"Missing folders: {[p for p in required if not os.path.isdir(p)]}")
    raise SystemExit(1)

# Configure logging
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(log_dir, exist_ok=True) # Creates logs folder if it doesn't exist
log_path = os.path.join(log_dir, "log.txt")
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
