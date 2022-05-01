import discord
from datetime import datetime
from discord.ext import commands
from discord.ui import Select, View
import requests
from os import getenv
import traceback
OPI = getenv('OPI')

class leaderboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def leaderboard(self, ctx):
		try:
			embed=discord.Embed(description=f"Fetching data from the API", color=0xff0000)
			msg = await ctx.send(embed=embed)
			DATA = requests.get(f"https://api.invite.observer/v1/leaderboards?type=alltime&gamemode=skywars&stat=experience&from=1&to=10&key={OPI}").json()
			PLAYERS = DATA["leaderboards"]
	
			def convert(xp):
				return (xp - 15000) / 10000. + 12

			NAMES=[]
			EXP=[]
			LEVEL=[]
			INFO=[]
			RANK=[]
   
			for data in PLAYERS:
				EXP.append(data["value"])
				NAMES=(str(data).split("] ", 1)[1][:-2])
				INFO.append(NAMES)
				RANK.append("#" + str(data["rank"]))

			for level in EXP:
				LEVEL.append(str(round(convert(level),2)))
    
			RANK = "\n".join(RANK)
			INFO = "\n".join(INFO)
			LEVEL = "\n".join(LEVEL)

			embed=discord.Embed(title="```SkyWars Leaderboard Top #10 | Experience```", color=0x2ecc71)
			embed.add_field(name="Ranking", value=RANK, inline=True)
			embed.add_field(name="Players", value=INFO, inline=True)
			embed.add_field(name="Level", value=LEVEL, inline=True)
			await msg.edit(embed=embed)
	
		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support Server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the Support Server] ")
			await msg.edit(embed=embed)
			print(traceback.print_exc())
def setup(bot):
	bot.add_cog(leaderboard(bot))