from calendar import c
from discord.ext import commands

class ping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def ping(self, ctx):
		await ctx.reply(f'Ping: {round (self.bot.latency * 1000)} ms')

def setup(bot):
	bot.add_cog(ping(bot))
