import discord
import typing 
from discord.ext import commands
import requests
from os import getenv
import traceback

class nw(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	

	@commands.command()
	async def nw(self, ctx, IGN: typing.Optional[str]):
		try:
			SKYHELPERAPI=getenv("SKYHELPERTOAPIKEY")
			if(SKYHELPERAPI == None):
				await ctx.send("To use this command, the host of the bot must set the SKYHELPERAPI environment variable.")
				return 0
			if(IGN == None):
				IGN=ctx.author.nick
				if(IGN == None):
						await ctx.send("Nickname not set, using username instead.",delete_after=1)
						IGN=ctx.author.name


			FETCHING=discord.Embed(description="Fetching data from API", color=0xff0000)
			msg = await ctx.send(embed=FETCHING)
			

			APIKEY = getenv('APIKEY')
			slothpixel = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{IGN}?key{APIKEY}",headers={'Cache-Control': 'no-cache'}).json()			
			try: #Check if the user exists.
				if slothpixel["error"] != None:
					await msg.delete()
					await ctx.send("Please enter a valid username.")
					return 0
			except Exception:
				pass

			
			try: #Get profile ID.
				ID = slothpixel["id"]
			except Exception:
				await msg.delete()
				await ctx.send("The user does not have a profile.")
				return 0

			
			SKYHELPERTOKEN=getenv('SKYHELPERTOKEN')
			#Basic temporary implementation.
			API = requests.get(f"{SKYHELPERAPI}/v1/profile/{IGN}/{ID}?key={SKYHELPERTOKEN}",headers={'Cache-Control': 'no-cache'}).json()	
			IGN	= API["data"]["username"]
			NETWORTH = "{:,}".format(round(API["data"]["networth"]["total_networth"]))   
   
			await msg.delete()
			await ctx.send(f"{IGN}'s networth is {NETWORTH} coins.")


			




		#Catch all errors
		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the support server] ")
			await msg.delete()
			await ctx.send(embed=embed)
			print(traceback.print_exc())



def setup(bot):
	bot.add_cog(nw(bot))
