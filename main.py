import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os import getenv
import logging

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True



bot = commands.Bot(command_prefix=getenv('PREFIX'), case_insensitive=True, intents=intents)
bot.remove_command('help')

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		bot.load_extension("cogs." + f[:-3])

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

@bot.command()
async def reload(ctx):
    if(getenv('ID') == str(ctx.author.id)):
        for f in os.listdir("./cogs"): 
            if f.endswith(".py"):
                bot.reload_extension("cogs." + f[:-3])
        clearConsole()
        await ctx.reply("Reloaded!")
    else:
        await ctx.reply("Only Developers can use this command.")
    
    
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_ready():
    clearConsole()
    print('Logged in as', bot.user.name)
    print("Servers:",len(bot.guilds))
    print("\n".join(guild.name for guild in bot.guilds))
    

bot.run(getenv('TOKEN'))

	
