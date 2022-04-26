from discord.ext import commands
import os
from dotenv import load_dotenv
from os import getenv

load_dotenv()

bot = commands.Bot(command_prefix=getenv('PREFIX'), case_insensitive=True)
bot.remove_command('help')

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		bot.load_extension("cogs." + f[:-3])

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)

bot.run(getenv('TOKEN'))

	