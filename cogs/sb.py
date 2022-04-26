import discord
import typing 
from discord.ext import commands
import requests
from os import getenv
import traceback

class sb(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	

	@commands.command()
	async def sb(self, ctx, IGN: typing.Optional[str]):
		if(IGN == None):
			IGN=ctx.author.nick
			if(IGN == None):
					await ctx.send("Nickname not set, using username instead.",delete_after=1)
					IGN=ctx.author.name

		try:
   
			FETCHING=discord.Embed(description="Fetching data from API", color=0xff0000)
			msg = await ctx.send(embed=FETCHING)
			

			try: #Check if the user exists.
				mojangapi = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{IGN}",headers={'Cache-Control': 'no-cache'}).json()
				UUID = mojangapi["id"]
				IGN = mojangapi["name"]
			except Exception: 
				await msg.delete()
				await ctx.send("Please enter a valid username.")
				return 0
   
			try: #Check if the user has a profile.
				APIKEY = getenv('APIKEY')
				slothpixel = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{IGN}?key{APIKEY}",headers={'Cache-Control': 'no-cache'}).json()
				PROFILE = slothpixel["cute_name"]
			except Exception:
				await msg.delete()
				await ctx.send("The user does not have a profile.")
				return 0

			slothpixel = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{IGN}/{PROFILE}?key={APIKEY}",headers={'Cache-Control': 'no-cache'}).json()
			senither = requests.get(f"https://hypixel-api.senither.com/v1/profiles/{UUID}/{PROFILE}?key={APIKEY}",headers={'Cache-Control': 'no-cache'}).json()
		
			MEMBERS = slothpixel["members"][UUID]
			ATB = MEMBERS["attributes"]
			STRENGHT = "{:,}".format(ATB["strength"])
			CRIT_DAMAGE = "{:,}".format(ATB["crit_damage"])
			CRIT_CHANCE = "{:,}".format(ATB["crit_chance"])
			HEALTH = "{:,}".format(ATB["health"])
			DEFENSE = "{:,}".format(ATB["defense"])

			try:
				BANK = "{:,}".format(round(senither["data"]["coins"]["bank"]))
			except Exception:
				BANK = "0"
			try:
				PURSE = "{:,}".format(round(senither["data"]["coins"]["purse"]))
			except Exception:
				PURSE = "0"
    
			ZSLAYER = round(senither["data"]["slayers"]["bosses"]["revenant"]["level"],2)
			SSLAYER = round(senither["data"]["slayers"]["bosses"]["tarantula"]["level"],2)
			WSLAYER = round(senither["data"]["slayers"]["bosses"]["sven"]["level"],2)
			ESLAYER = round(senither["data"]["slayers"]["bosses"]["enderman"]["level"],2)
   
			SOULS = senither["data"]["fairy_souls"]
   
			SAVERAGE = round(senither["data"]["skills"]["average_skills"],2)
			WEIGHT = round(senither["data"]["weight"])
			COMBAT = round(senither["data"]["skills"]["combat"]["level"],2)
   
			PETN = MEMBERS["active_pet"]["name"]
			PETL = MEMBERS["active_pet"]["level"]
			PETR = MEMBERS["active_pet"]["rarity"].title()
			PET = f"[Lvl {PETL}] " f"{PETN} " f"-{PETR}"

			
			embed=discord.Embed(title=f"{IGN} ({PROFILE})", color=0x2ecc71,timestamp=ctx.message.created_at,url=f"https://sky.shiiyu.moe/stats/{IGN}/{PROFILE}")
			embed.set_thumbnail(url=f"https://cravatar.eu/helmavatar/{IGN}/600.png")
			embed.add_field(name=f"<:sbhp:875406119990857738>{HEALTH}     <:sbdefense:875405977178996806>{DEFENSE}     <:sbstrength:875406038692691971>{STRENGHT}     <:sbcc:875406019684085792>{CRIT_CHANCE}     <:sbcd:875405999811481721>{CRIT_DAMAGE}", value="\u200B", inline=False)
			embed.add_field(name=f"<:sbfairy:875407537212653618>{SOULS}/228 \n<:sbcombat:875408914689183914>Combat {COMBAT} \n<:sbpets:875409370198970388>{PET}" , value="\u200B", inline=False)
			embed.add_field(name=f"<:sbslayer:875405312130166844>  Slayers:     <:sbrevs:875403994749612052>{ZSLAYER}     <:sbspider:875406772511338506>{SSLAYER}     <:sbsven:875404023308636171>{WSLAYER}     <:sbvoid:875404075338956860>{ESLAYER}", value="\u200B", inline=False)
			embed.add_field(name=f"⚒ Avg Skill Level: {SAVERAGE}     <:sbweight:875408638053871667> Weight: {WEIGHT}     \n<:sbbank:875401498459250698>{BANK}     <:sbpurse:875400824845647914>{PURSE}", value="\u200B", inline=False)
			embed.set_footer(text="The stats do not include potion effects!")
			await msg.delete()
			await ctx.send(embed=embed)
   
   
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
	bot.add_cog(sb(bot))

