import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()


bot = commands.Bot(command_prefix=getenv('PREFIX'), case_insensitive=True)
bot.remove_command('help')
snipe_message_author = {}
snipe_message_content = {}
snipe_message_time = {}


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
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    snipe_message_time[message.guild.id] = message.created_at
 
 
@bot.command()
async def snipe(ctx):
    channel = ctx.channel
    guild = ctx.guild
    try:
        content = snipe_message_content[channel.id]
        author = snipe_message_author[channel.id]
        time = snipe_message_time[guild.id]
        embed = discord.Embed(description=content, color=discord.Color.red(), timestamp=time)
        embed.set_author(name=f"{author}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Deleted in #{channel.name}")
        await ctx.send(embed = embed)
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")


bot.run(getenv('TOKEN'))
