import discord
import typing
from discord.ext import commands
import requests
from os import getenv
import traceback
from numerize import numerize
class nw(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(aliases=['networth'])
	async def nw(self, ctx, IGN: typing.Optional[str], PROFILE: typing.Optional[str]):
		try:
			SKYHELPERAPI=getenv("SKYHELPERAPI")

			if(SKYHELPERAPI != None): #Check if the  SkyHelper API key is set.
				if(IGN == None): #Check if the user has entered a username.
					IGN=ctx.author.nick
					if(IGN == None): #Check if the user does not have a nickname.
							IGN=ctx.author.name


				embed=discord.Embed(description=f"Fetching data from API for User: {IGN}", color=0xff0000)
				msg = await ctx.send(embed=embed)


				APIKEY = getenv('APIKEY')
				if(PROFILE == None): #Check if the user has entered a profile.
					slothpixel = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{IGN}?key={APIKEY}").json()
					PROFILE = slothpixel["cute_name"]
				else:
					slothpixel = requests.get(f"https://api.slothpixel.me/api/skyblock/profile/{IGN}/{PROFILE}?key={APIKEY}").json()
					PROFILE = PROFILE.title()
				try:
					if slothpixel["error"] != None: #Check if the user exists.
						embed=discord.Embed(description=f"Please enter a valid username", color=0xff0000)
						await msg.edit(embed=embed)
						return 0
				except Exception:
					pass


				try: #Get profile ID.
					ID = slothpixel["id"]
				except Exception:
					embed=discord.Embed(description=f"The user does not have a profile.", color=0xff0000)
					await msg.edit(embed=embed)
					return 0


				SKYHELPERTOKEN = getenv('SKYHELPERTOKEN')
				API = requests.get(f"{SKYHELPERAPI}/v1/profile/{IGN}/{ID}?key={SKYHELPERTOKEN}").json()
				IGN	= API["data"]["username"]


				try:
					NETWORTH = numerize.numerize(API["data"]["networth"]["total_networth"])
					NETWORTH_PURSE = numerize.numerize(API["data"]["networth"]["purse"])
					NETWORTH_BANK = numerize.numerize(API["data"]["networth"]["bank"])
					TYPES=API["data"]["networth"]["types"]
				except Exception:
					embed=discord.Embed(description=f"The player has the API disabled.", color=0xff0000)
					await msg.edit(embed=embed)
					return 0



				#Armor
				try:
					ITEMS_ARMOR = []
					ARMOR = numerize.numerize(TYPES["armor"]["total"])
					ARMOR_TOP = TYPES["armor"]["top_items"]
					for item in ARMOR_TOP:
						if item.get("recomb", False):
							ITEMS_ARMOR.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_ARMOR.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))
					ITEMS_ARMOR = "\n".join(ITEMS_ARMOR)

				except Exception:
					ARMOR = "0"
					ITEMS_ARMOR = "N/A"



				#Wardrobe
				try:
					WARDROBE_TOP = []
					WARDROBE=numerize.numerize(TYPES["wardrobe_inventory"]["total"])
					WARDROBE_TOP = TYPES["wardrobe_inventory"]["top_items"]

					ITEMS_WARDROBE = []
					ITEMS_WARDROBE_COUNT2=len(WARDROBE_TOP) -4

					if ITEMS_WARDROBE_COUNT2 < 1:
						ITEMS_WARDROBE_COUNT = ""
					else:
						ITEMS_WARDROBE_COUNT= "..." + str(ITEMS_WARDROBE_COUNT2) + " more items"

					for item in WARDROBE_TOP:
						if item.get("recomb", False):
							ITEMS_WARDROBE.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_WARDROBE.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))
					ITEMS_WARDROBE = "\n".join(ITEMS_WARDROBE[:4])
				except Exception:
					WARDROBE = "0"
					ITEMS_WARDROBE = "N/A"
					ITEMS_WARDROBE_COUNT = ""



				#Inventory
				try:
					INVENTORY_TOP = []
					INVENTORY=numerize.numerize(TYPES["inventory"]["total"])
					INVENTORY_TOP = TYPES["inventory"]["top_items"]

					ITEMS_INVENTORY = []
					ITEMS_INVENTORY_COUNT2=len(INVENTORY_TOP) -4

					if ITEMS_INVENTORY_COUNT2 < 1:
						ITEMS_INVENTORY_COUNT = ""
					else:
						ITEMS_INVENTORY_COUNT= "..." + str(ITEMS_INVENTORY_COUNT2) + " more items"

					for item in INVENTORY_TOP:
						if item.get("recomb", False):
							ITEMS_INVENTORY.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_INVENTORY.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))

					ITEMS_INVENTORY = "\n".join(ITEMS_INVENTORY[:4])
				except Exception:
					INVENTORY = "0"
					ITEMS_INVENTORY = "N/A"
					ITEMS_INVENTORY_COUNT = ""

				#Enderchest
				try:
					ENDERCHEST_TOP = []
					ENDERCHEST=numerize.numerize(TYPES["enderchest"]["total"])
					ENDERCHEST_TOP = TYPES["enderchest"]["top_items"]

					ITEMS_ENDERCHEST = []
					ITEMS_ENDERCHEST_COUNT2=len(ENDERCHEST_TOP) -4

					if ITEMS_ENDERCHEST_COUNT2 < 1:
						ITEMS_ENDERCHEST_COUNT = ""
					else:
						ITEMS_ENDERCHEST_COUNT= "..." + str(ITEMS_ENDERCHEST_COUNT2) + " more items"

					for item in ENDERCHEST_TOP:
						if item.get("recomb", False):
							ITEMS_ENDERCHEST.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_ENDERCHEST.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))

					ITEMS_ENDERCHEST = "\n".join(ITEMS_ENDERCHEST[:4])
				except Exception:
					ENDERCHEST = "0"
					ITEMS_ENDERCHEST = "N/A"
					ITEMS_ENDERCHEST_COUNT = ""


				#Storage
				try:
					STORAGE=numerize.numerize(TYPES["storage"]["total"])
					STORAGE_TOP = TYPES["storage"]["top_items"]

					ITEMS_STORAGE = []
					ITEMS_STORAGE_COUNT2=len(STORAGE_TOP) -4

					if ITEMS_STORAGE_COUNT2 < 1:
						ITEMS_STORAGE_COUNT = ""
					else:
						ITEMS_STORAGE_COUNT= "..." + str(ITEMS_STORAGE_COUNT2) + " more items"

					for item in STORAGE_TOP:
						if item.get("recomb", False):
							ITEMS_STORAGE.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_STORAGE.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))

					ITEMS_STORAGE = "\n".join(ITEMS_STORAGE[:4])
				except Exception:
					STORAGE = "0"
					ITEMS_STORAGE = "N/A"
					ITEMS_STORAGE_COUNT = ""

				#Pets
				try:
					PETS_TOP = []
					PETS=numerize.numerize(TYPES["pets"]["total"])
					PETS_TOP = TYPES["pets"]["top_items"]

					ITEMS_PETS = []
					ITEMS_PETS_COUNT2=len(PETS_TOP) -4

					if ITEMS_PETS_COUNT2 < 1:
						ITEMS_PETS_COUNT = ""
					else:
						ITEMS_PETS_COUNT= "..." + str(ITEMS_PETS_COUNT2) + " more items"

					for item in PETS_TOP:
						ITEMS_PETS.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))

					ITEMS_PETS = "\n".join(ITEMS_PETS[:4])
				except Exception:
					PETS = "0"
					ITEMS_PETS = "N/A"
					ITEMS_PETS_COUNT = ""

				#Talismans
				try:
					TALISMANS_TOP = []
					TALISMANS=numerize.numerize(TYPES["talismans"]["total"])
					TALISMANS_TOP = TYPES["talismans"]["top_items"]

					ITEMS_TALISMANS = []
					ITEMS_TALISMANS_COUNT2=len(TALISMANS_TOP) -4

					if ITEMS_TALISMANS_COUNT2 < 1:
						ITEMS_TALISMANS_COUNT = ""
					else:
						ITEMS_TALISMANS_COUNT= "..." + str(ITEMS_TALISMANS_COUNT2) + " more items"

					for item in TALISMANS_TOP:
						if item.get("recomb", False):
							ITEMS_TALISMANS.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_TALISMANS.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))

					ITEMS_TALISMANS = "\n".join(ITEMS_TALISMANS[:4])
				except Exception:
					TALISMANS = "0"
					ITEMS_TALISMANS = "N/A"
					ITEMS_TALISMANS_COUNT = ""



				#Personal Vault
				try:
					VAULT_TOP = []
					VAULT=numerize.numerize(TYPES["personal_vault"]["total"])
					VAULT_TOP = TYPES["personal_vault"]["top_items"]

					ITEMS_VAULT = []
					ITEMS_VAULT_COUNT2=len(VAULT_TOP) -4

					if ITEMS_VAULT_COUNT2 < 1:
						ITEMS_VAULT_COUNT = ""
					else:
						ITEMS_VAULT_COUNT= "..." + str(ITEMS_VAULT_COUNT2) + " more items"

					for item in VAULT_TOP:
						if item.get("recomb", False):
							ITEMS_VAULT.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")" + "<:Recombobulator:969666941490970654>"))
						else:
							ITEMS_VAULT.append(item["name"]+ " " + "("+str(numerize.numerize(item["price"])+")"))

					ITEMS_VAULT = "\n".join(ITEMS_VAULT[:4])
				except Exception:
					VAULT = "0"
					ITEMS_VAULT = "N/A"
					ITEMS_VAULT_COUNT = ""





				#Basic temporary implementation.
				embed=discord.Embed(title=f"{IGN} ({PROFILE})\n", description=f"Networth: **{NETWORTH}**",color=0x2ecc71,timestamp=ctx.message.created_at,url=f"https://sky.shiiyu.moe/stats/{IGN}/{PROFILE}")
				embed.set_thumbnail(url=f"https://cravatar.eu/helmavatar/{IGN}/600.png")
				embed.add_field(name=f"<:purse:875400824845647914> Purse:", value=f"**{NETWORTH_PURSE}**", inline=True)
				embed.add_field(name=f"<:bank:875401498459250698> Bank:", value=f"**{NETWORTH_BANK}**", inline=True)
				embed.add_field(name=f"<:armor:968922140550238228> Armor ({ARMOR})", value=ITEMS_ARMOR, inline=False)
				embed.add_field(name=f"<:wardrobe:968961784239239208> Wardrobe ({WARDROBE})", value=f"{ITEMS_WARDROBE} \n {ITEMS_WARDROBE_COUNT}", inline=False)
				embed.add_field(name=f"<:chest:968965278249652295> Inventory ({INVENTORY})", value=f"{ITEMS_INVENTORY} \n {ITEMS_INVENTORY_COUNT}", inline=False)
				embed.add_field(name=f"<:echest:968965295421136926> Enderchest ({ENDERCHEST})", value=f"{ITEMS_ENDERCHEST} \n {ITEMS_ENDERCHEST_COUNT}", inline=False)
				embed.add_field(name=f"<:storage:968965358641893396> Storage ({STORAGE})", value=f"{ITEMS_STORAGE} \n {ITEMS_STORAGE_COUNT}", inline=False)
				embed.add_field(name=f"<:pets:968965570420678666> Pets ({PETS})", value=f"{ITEMS_PETS} \n {ITEMS_PETS_COUNT}", inline=False)
				embed.add_field(name=f"<:talisman:968965395421728778> Talismans ({TALISMANS})", value=f"{ITEMS_TALISMANS} \n {ITEMS_TALISMANS_COUNT}", inline=False)
				embed.add_field(name=f"<:door:969688659391553546> Personal Vault ({VAULT})", value=f"{ITEMS_VAULT} \n {ITEMS_VAULT_COUNT}", inline=False)
				await msg.edit(embed=embed)

			else: #If the SkyHelper API key is not set.
				await ctx.send("To use this command, the host of the bot must set the SKYHELPERAPI environment variable.")
				return 0


		#Catch all errors
		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support Server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the Support Server] ")
			await msg.edit(embed=embed)
			print(traceback.print_exc())



def setup(bot):
	bot.add_cog(nw(bot))
