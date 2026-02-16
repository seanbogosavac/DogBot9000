from .bot_instance import bot
from .loops import daily_pistouche


@bot.event
async def on_ready():
    daily_pistouche.start()
    print("DogBot9000 up and running")
