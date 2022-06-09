import discord
import typing 
import datetime
from discord.ext import commands
from discord.ui import Select, View
import requests
from os import getenv
import traceback
OPI = getenv('OPI')
APIKEY = getenv('APIKEY')

class monthly(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=["month"])
	async def monthly(self, ctx, IGN: typing.Optional[str]):
		if(IGN == None): #Check if the user has entered a username.
			IGN=ctx.author.nick
			if(IGN == None): #Check if the user does not have a nickname.
					IGN=ctx.author.name

		try:
			embed=discord.Embed(description=f"Fetching data from the API for: {IGN}", color=0xff0000)
			msg = await ctx.send(embed=embed)
   
			try: #Check if the user exists.
				mojangapi = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{IGN}").json()
				UUID = mojangapi["id"]
				IGN = mojangapi["name"]
			except Exception: 
				embed=discord.Embed(description=f"Please enter a valid username", color=0xff0000)
				await msg.edit(embed=embed)
				return 0

			API = requests.get(f"https://api.invite.observer/v1/monthly?uuid={UUID}&key={OPI}").json()
			slothpixel = requests.get(f"https://api.slothpixel.me/api/players/{IGN}?key={APIKEY}").json()
			today = slothpixel["stats"]["SkyWars"]
			month = API["monthly"]["timestamp"]
			date = str(datetime.datetime.fromtimestamp(month / 1000.0).strftime('%y-%m-%d'))
			sw = API["monthly"]["stats"]["skywars"]
			a1 = sw["souls"]
			a2 = sw["wins"]
			a3 = sw["losses"]
			a4 = sw["kills"]
			a5 = sw["deaths"]
			b1 = today["souls"]
			b2 = today["wins"]
			b3 = today["losses"]
			b4 = today["kills"]
			b5 = today["deaths"]

			embed=discord.Embed(title="Skywars monthly compare", color=0x2ecc71)
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/855023851855544321/897893382028918864/Skywars.png")
			embed.add_field(name="\u200b", value="Souls:\nWins:\nLosses:\nKills:\nDeaths:", inline=True)
			embed.add_field(name=date, value=f"{a1} \n {a2} \n {a3} \n {a4} \n {a5}", inline=True)
			embed.add_field(name="Now", value=f"{b1} \n {b2} \n {b3} \n {b4} \n {b5}", inline=True)
			await msg.edit(embed=embed)

		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the support server] ")
			await msg.edit(embed=embed)
			print(traceback.print_exc())
def setup(bot):
	bot.add_cog(monthly(bot))
 