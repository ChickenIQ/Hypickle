import discord
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def help(self, ctx):
		embed=discord.Embed(title=f"Support Server", description=f"**Commands:**",color=0x2ecc71,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
		embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/36390285/Logo.png?width=64")
		embed.add_field(name=f"\u200B", value=f"**Skyblock:**", inline=False)
		embed.add_field(name=f"•Nw|Networth", value=f"Displays the networth of a player", inline=False)
		embed.add_field(name=f"•A", value=f"\u200B", inline=False)
		embed.set_footer(text="[To report bugs create a ticket in the Support Server]")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Help(bot))
