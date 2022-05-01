import discord
import typing 
from discord.ext import commands
import requests
from os import getenv
import traceback
from numerize import numerize

class name_history(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	

	@commands.command(aliases=['nh',"namehistory", "names"])
	async def name_history(self, ctx, IGN: typing.Optional[str]):
		if(IGN == None): #Check if the user has entered a username.
			IGN=ctx.author.nick
			if(IGN == None): #Check if the user does not have a nickname.
					IGN=ctx.author.name


		try:

			embed=discord.Embed(description=f"Fetching data from API for User: {IGN}", color=0xff0000)
			msg = await ctx.send(embed=embed)
			try: #Check if the user exists.
				slothpixel = requests.get(f"https://api.slothpixel.me/api/players/{IGN}").json()
				UUID = slothpixel["uuid"]
				IGN = slothpixel["username"]
				NAME_HISTORY = reversed(slothpixel["name_history"])
    

			except Exception: 
				embed=discord.Embed(description=f"Please enter a valid username", color=0xff0000)
				await msg.edit(embed=embed)
				return 0


			NAME_HISTORY = "\n".join(NAME_HISTORY)
			

			
			embed=discord.Embed(title=f"{IGN}", color=0x2ecc71,timestamp=ctx.message.created_at,url=f"https://namemc.com/profile/{IGN}")
			embed.set_thumbnail(url=f"https://cravatar.eu/helmavatar/{IGN}/600.png")
			embed.add_field(name="Name History:", value=NAME_HISTORY, inline=False)
			embed.set_footer(text=f"UUID: {UUID}")
			await msg.edit(embed=embed)
   
   
		#Catch all errors
		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support Server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the Support Server] ")
			await msg.edit(embed=embed)
			print(traceback.print_exc())



def setup(bot):
	bot.add_cog(name_history(bot))