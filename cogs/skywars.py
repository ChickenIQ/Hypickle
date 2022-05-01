import discord
import typing 
from discord.ext import commands
from discord.ui import Select, View
import requests
from os import getenv
import traceback

class skywars(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['sw'])
	async def skywars(self, ctx, IGN: typing.Optional[str]): 
		if(IGN == None):
			IGN=ctx.author.nick
			if(IGN == None):
				IGN=ctx.author.name 
		try:
			embed=discord.Embed(description=f"Fetching data from API for User: {IGN}", color=0xff0000)
			msg = await ctx.send(embed=embed)
			
			try:
				mojangapi = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{IGN}").json()
				UUID = mojangapi["id"]
				IGN = mojangapi["name"]
			except Exception:
				embed=discord.Embed(description=f"Please enter a valid username", color=0xff0000)
				await msg.edit(embed=embed)
				return 0

			APIKEY = getenv('APIKEY')
			slothpixel = requests.get(f"https://api.slothpixel.me/api/players/{UUID}?key={APIKEY}").json()
			swstats = slothpixel["stats"]["SkyWars"]
			solo = slothpixel["stats"]["SkyWars"]["gamemodes"]["solo"]
			team = slothpixel["stats"]["SkyWars"]["gamemodes"]["team"]
			ranked = slothpixel["stats"]["SkyWars"]["gamemodes"]["ranked"]

			select = Select(placeholder="Select a mode:",options=[
				discord.SelectOption(label="Overall"),
				discord.SelectOption(label="Solo"),
				discord.SelectOption(label="Doubles"),
				discord.SelectOption(label="Ranked"),
        	])
   
			async def click(interaction):
				if select.values[0] == "Overall":
					await msg.edit(embed=embed_overall,view=view)				
				if select.values[0] == "Solo":
					await msg.edit(embed=embed_solo,view=view)
				if select.values[0] == "Doubles":
					await msg.edit(embed=embed_doubles,view=view)
				if select.values[0] == "Ranked":
					await msg.edit(embed=embed_ranked,view=view)
			select.callback = click
			view = View()
			view.add_item(select)

			PREFIX = getenv('PREFIX')

			embed_overall=discord.Embed(title=f"Skywars overall stats | {IGN}",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_overall.set_thumbnail(url="https://cdn.discordapp.com/attachments/855023851855544321/897893382028918864/Skywars.png")
			embed_overall.add_field(name="► Level", value=swstats["level"], inline=True)
			embed_overall.add_field(name="► Souls", value=swstats["souls"], inline=True)
			embed_overall.add_field(name="► Heads", value=swstats["heads"]["total_heads"], inline=True)
			embed_overall.add_field(name="► Wins", value=swstats["wins"], inline=True)
			embed_overall.add_field(name="► Losses", value=swstats["losses"], inline=True)
			embed_overall.add_field(name="► W/L ratio", value=swstats["win_loss_ratio"], inline=True)
			embed_overall.add_field(name="► Kills", value=swstats["kills"], inline=True)
			embed_overall.add_field(name="► Deaths", value=swstats["deaths"], inline=True)
			embed_overall.set_footer(text=f"{PREFIX}skywars <username>")
			embed_overall.add_field(name="► K/D ratio", value=swstats["kill_death_ratio"], inline=True)
			await msg.edit(embed=embed_overall,view=view)
			
			embed_solo=discord.Embed(title=f"Skywars solo's stats | {IGN}",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_solo.set_thumbnail(url="https://cdn.discordapp.com/attachments/855023851855544321/897893382028918864/Skywars.png")
			embed_solo.add_field(name="► Games Played", value=solo["games"], inline=True)
			embed_solo.add_field(name="► Assists", value=solo["assists"], inline=True)
			embed_solo.add_field(name="► Heads", value=solo["heads"], inline=True)
			embed_solo.add_field(name="► Wins", value=solo["wins"], inline=True)
			embed_solo.add_field(name="► Losses", value=solo["losses"], inline=True)
			embed_solo.add_field(name="► W/L ratio", value=solo["win_loss_ratio"], inline=True)
			embed_solo.add_field(name="► Kills", value=solo["kills"], inline=True)
			embed_solo.add_field(name="► Deaths", value=solo["deaths"], inline=True)
			embed_solo.add_field(name="► K/D ratio", value=solo["kill_death_ratio"], inline=True)
			embed_solo.set_footer(text=f"{PREFIX}skywars <username>")
			
			embed_doubles=discord.Embed(title=f"Skywars doubles stats | {IGN}",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_doubles.set_thumbnail(url="https://cdn.discordapp.com/attachments/855023851855544321/897893382028918864/Skywars.png")
			embed_doubles.add_field(name="► Games Played", value=team["games"], inline=True)
			embed_doubles.add_field(name="► Assists", value=team["assists"], inline=True)
			embed_doubles.add_field(name="► Heads", value=team["heads"], inline=True)
			embed_doubles.add_field(name="► Wins", value=team["wins"], inline=True)
			embed_doubles.add_field(name="► Losses", value=team["losses"], inline=True)
			embed_doubles.add_field(name="► W/L ratio", value=team["win_loss_ratio"], inline=True)
			embed_doubles.add_field(name="► Kills", value=team["kills"], inline=True)
			embed_doubles.add_field(name="► Deaths", value=team["deaths"], inline=True)
			embed_doubles.add_field(name="► K/D ratio", value=team["kill_death_ratio"], inline=True)
			embed_doubles.set_footer(text=f"{PREFIX}skywars <username>")
			
			embed_ranked=discord.Embed(title=f"Skywars ranked stats | {IGN}",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_ranked.set_thumbnail(url="https://cdn.discordapp.com/attachments/855023851855544321/897893382028918864/Skywars.png")
			embed_ranked.add_field(name="► Games Played", value=ranked["games"], inline=True)
			embed_ranked.add_field(name="► Fastest Win", value=ranked["fastest_win"], inline=True)
			embed_ranked.add_field(name="► Assists", value=ranked["assists"], inline=True)
			embed_ranked.add_field(name="► Wins", value=ranked["wins"], inline=True)
			embed_ranked.add_field(name="► Losses", value=ranked["losses"], inline=True)
			embed_ranked.add_field(name="► W/L ratio", value=ranked["win_loss_ratio"], inline=True)
			embed_ranked.add_field(name="► Kills", value=ranked["kills"], inline=True)
			embed_ranked.add_field(name="► Deaths", value=ranked["deaths"], inline=True)
			embed_ranked.add_field(name="► K/D ratio", value=ranked["kill_death_ratio"], inline=True)
			embed_ranked.set_footer(text=f"{PREFIX}skywars <username>")
				
		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the support server] ")
			await msg.edit(embed=embed)
			print(traceback.print_exc())

def setup(bot):
	bot.add_cog(skywars(bot))