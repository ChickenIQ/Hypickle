import discord
from discord.ext import commands
snipe_message_author = {}
snipe_message_content = {}
snipe_message_time = {}

class Snipe(commands.Cog):
    
    def __init__(self, bot):
        bot = bot

        
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        snipe_message_time[message.guild.id] = message.created_at

 
    @commands.command() 
    async def snipe(self,ctx):
        channel = ctx.channel
        guild = ctx.guild
        try:
            
            content = snipe_message_content[channel.id]
            author = snipe_message_author[channel.id]
            time = snipe_message_time[guild.id]
            embed = discord.Embed(description=content, color=0xff0000, timestamp=time)
            embed.set_author(name=f"{author}", icon_url=author.avatar_url)
            embed.set_footer(text=f"Deleted in #{channel.name}")
            await ctx.send(embed = embed)
            
            
        except Exception as ext:
             await ctx.channel.send("Couldn't find a message to snipe!")
                       


def setup(bot):
	bot.add_cog(Snipe(bot))
 
 
