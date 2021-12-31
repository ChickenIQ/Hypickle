import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()


bot = commands.Bot(command_prefix=getenv('PREFIX'), case_insensitive=True)
bot.remove_command('help')
bot.sniped_messages = {}

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)

# Help command
@bot.command()
async def help(ctx):
    await ctx.reply('Why tf do you need help?')
 

# Snipe Command
 
@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.red(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")
    
    await ctx.channel.send(embed=embed)


bot.run(getenv('TOKEN'))


