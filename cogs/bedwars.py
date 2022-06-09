import discord
import typing 
from discord.ext import commands
from discord.ui import Select, View
import requests
from os import getenv
import traceback

class bedwars(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['bw'])
	async def bedwars(self, ctx, IGN: typing.Optional[str]):
		if(IGN == None):
			IGN=ctx.author.nick
			if(IGN == None):
					IGN=ctx.author.name
		try:
			embed=discord.Embed(description=f"Fetching data from API for User: {IGN}", color=0xff0000)
			msg = await ctx.send(embed=embed)
			
			try: #Check if the user exists.
				mojangapi = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{IGN}").json()
				IGN = mojangapi["name"]
			except Exception: 
				embed=discord.Embed(description=f"Please enter a valid username", color=0xff0000)
				await msg.edit(embed=embed)
				return 0

			APIKEY = getenv('APIKEY')
			slothpixel = requests.get(f"https://api.slothpixel.me/api/players/{IGN}?key={APIKEY}").json()
			overall = slothpixel["stats"]["BedWars"]
			solo = slothpixel["stats"]["BedWars"]["gamemodes"]["solo"]
			doubles = slothpixel["stats"]["BedWars"]["gamemodes"]["doubles"]
			threes = slothpixel["stats"]["BedWars"]["gamemodes"]["3v3v3v3"]
			fours = slothpixel["stats"]["BedWars"]["gamemodes"]["4v4v4v4"]
			dfours = slothpixel["stats"]["BedWars"]["gamemodes"]["4v4"]

			select = Select(placeholder="Select a mode:",options=[
				discord.SelectOption(label="Overall"),
				discord.SelectOption(label="Solo"),
				discord.SelectOption(label="Doubles"),
				discord.SelectOption(label="Threes"),
				discord.SelectOption(label="Fours"),
				discord.SelectOption(label="4v4"),
			])

			try:
				async def click(interaction):
					if select.values[0] == "Overall":
						await msg.edit(embed=embed_overall,view=view)				
					if select.values[0] == "Solo":
						await msg.edit(embed=embed_solo,view=view)
					if select.values[0] == "Doubles":
						await msg.edit(embed=embed_doubles,view=view)
					if select.values[0] == "Threes":
						await msg.edit(embed=embed_threes,view=view)
					if select.values[0] == "Fours":
						await msg.edit(embed=embed_fours,view=view)
					if select.values[0] == "Dfours":
						await msg.edit(embed=embed_dfours,view=view)

				select.callback = click
				view = View()
				view.add_item(select)
			except Exception:
				pass

			PREFIX = getenv('PREFIX')

			embed_overall=discord.Embed(title=f"```Bedwars overall stats | {IGN}```",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_overall.set_thumbnail(url="https://media.discordapp.net/attachments/968864446418145330/968948529479417906/unknown.png")
			embed_overall.add_field(name="► Level", value=overall["level"], inline=True),    				embed_overall.add_field(name="► Winstreak", value=overall["winstreak"], inline=True)
			embed_overall.add_field(name="► Losses", value=overall["losses"], inline=True),     			embed_overall.add_field(name="► Wins", value=overall["wins"], inline=True)
			embed_overall.add_field(name="► Kills", value=overall["kills"], inline=True),     				embed_overall.add_field(name="► Deaths", value=overall["deaths"], inline=True)
			embed_overall.add_field(name="► Beds broken", value=overall["beds_broken"], inline=True), 		embed_overall.add_field(name="► Beds Lost", value=overall["beds_lost"], inline=True)
			embed_overall.add_field(name="► Finals Kills", value=overall["final_kills"], inline=True),		embed_overall.add_field(name="► Final Deaths", value=overall["final_deaths"], inline=True)
			embed_overall.add_field(name="► K/D Ratio", value=overall["k_d"], inline=True),					embed_overall.add_field(name="► W/L ratio", value=overall["w_l"], inline=True)
			embed_overall.add_field(name="► Bed ratio", value=overall["bed_ratio"], inline=True),			embed_overall.add_field(name="► Final K/D Ratio", value=overall["final_k_d"], inline=True)	
			embed_overall.set_footer(text=f"{PREFIX}skywars <username>")
			await msg.edit(embed=embed_overall,view=view)
			
			embed_solo=discord.Embed(title=f"```Bedwars solo's stats | {IGN}```",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_solo.set_thumbnail(url="https://media.discordapp.net/attachments/968864446418145330/968948529479417906/unknown.png")
			embed_solo.add_field(name="► Games Played", value=solo["games_played"], inline=True),    		embed_solo.add_field(name="► Winstreak", value=solo["winstreak"], inline=True)
			embed_solo.add_field(name="► Losses", value=solo["losses"], inline=True),     					embed_solo.add_field(name="► Wins", value=solo["wins"], inline=True)
			embed_solo.add_field(name="► Kills", value=solo["kills"], inline=True),     					embed_solo.add_field(name="► Deaths", value=solo["deaths"], inline=True)
			embed_solo.add_field(name="► Beds broken", value=solo["beds_broken"], inline=True), 			embed_solo.add_field(name="► Beds Lost", value=solo["beds_lost"], inline=True)
			embed_solo.add_field(name="► Finals Kills", value=solo["final_kills"], inline=True),			embed_solo.add_field(name="► Final Deaths", value=solo["final_deaths"], inline=True)
			embed_solo.add_field(name="► K/D Ratio", value=solo["k_d"], inline=True),						embed_solo.add_field(name="► W/L ratio", value=solo["w_l"], inline=True)			
			embed_solo.add_field(name="► Bed ratio", value=solo["bed_ratio"], inline=True),					embed_solo.add_field(name="► Final K/D Ratio", value=solo["final_k_d"], inline=True)	
			embed_solo.set_footer(text=f"{PREFIX}skywars <username>")
   
			embed_doubles=discord.Embed(title=f"```Bedwars doubles stats | {IGN}```",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_doubles.set_thumbnail(url="https://media.discordapp.net/attachments/968864446418145330/968948529479417906/unknown.png")
			embed_doubles.add_field(name="► Games Played", value=doubles["games_played"], inline=True),     embed_doubles.add_field(name="► Winstreak", value=doubles["winstreak"], inline=True)
			embed_doubles.add_field(name="► Losses", value=doubles["losses"], inline=True),     			embed_doubles.add_field(name="► Wins", value=doubles["wins"], inline=True)
			embed_doubles.add_field(name="► Kills", value=doubles["kills"], inline=True),     				embed_doubles.add_field(name="► Deaths", value=doubles["deaths"], inline=True)
			embed_doubles.add_field(name="► Beds broken", value=doubles["beds_broken"], inline=True), 		embed_doubles.add_field(name="► Beds Lost", value=doubles["beds_lost"], inline=True)
			embed_doubles.add_field(name="► Finals Kills", value=doubles["final_kills"], inline=True),		embed_doubles.add_field(name="► Final Deaths", value=doubles["final_deaths"], inline=True)	
			embed_doubles.add_field(name="► K/D Ratio", value=doubles["k_d"], inline=True),					embed_solo.add_field(name="► W/L ratio", value=doubles["w_l"], inline=True)	
			embed_doubles.add_field(name="► Bed ratio", value=doubles["bed_ratio"], inline=True),			embed_doubles.add_field(name="► Final K/D Ratio", value=doubles["final_k_d"], inline=True)	
			embed_doubles.set_footer(text=f"{PREFIX}skywars <username>")
   
			embed_threes=discord.Embed(title=f"```Bedwars threes stats | {IGN}```",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_threes.set_thumbnail(url="https://media.discordapp.net/attachments/968864446418145330/968948529479417906/unknown.png")
			embed_threes.add_field(name="► Games Played", value=threes["games_played"], inline=True),     	embed_threes.add_field(name="► Winstreak", value=threes["winstreak"], inline=True)
			embed_threes.add_field(name="► Losses", value=threes["losses"], inline=True),     				embed_threes.add_field(name="► Wins", value=threes["wins"], inline=True)
			embed_threes.add_field(name="► Kills", value=threes["kills"], inline=True),     				embed_threes.add_field(name="► Deaths", value=threes["deaths"], inline=True)
			embed_threes.add_field(name="► Beds broken", value=threes["beds_broken"], inline=True), 		embed_threes.add_field(name="► Beds Lost", value=threes["beds_lost"], inline=True)
			embed_threes.add_field(name="► Finals Kills", value=threes["final_kills"], inline=True),		embed_threes.add_field(name="► Final Deaths", value=threes["final_deaths"], inline=True)	
			embed_threes.add_field(name="► K/D Ratio", value=threes["k_d"], inline=True),					embed_threes.add_field(name="► W/L ratio", value=threes["w_l"], inline=True)	
			embed_threes.add_field(name="► Bed ratio", value=threes["bed_ratio"], inline=True),				embed_threes.add_field(name="► Final K/D Ratio", value=threes["final_k_d"], inline=True)	
			embed_threes.set_footer(text=f"{PREFIX}skywars <username>")
   
			embed_fours=discord.Embed(title=f"```Bedwars fours stats | {IGN}```",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_fours.set_thumbnail(url="https://media.discordapp.net/attachments/968864446418145330/968948529479417906/unknown.png")
			embed_fours.add_field(name="► Games Played", value=fours["games_played"], inline=True),     	embed_fours.add_field(name="► Winstreak", value=fours["winstreak"], inline=True)
			embed_fours.add_field(name="► Losses", value=fours["losses"], inline=True),     				embed_fours.add_field(name="► Wins", value=fours["wins"], inline=True)
			embed_fours.add_field(name="► Kills", value=fours["kills"], inline=True),     					embed_fours.add_field(name="► Deaths", value=fours["deaths"], inline=True)
			embed_fours.add_field(name="► Beds broken", value=fours["beds_broken"], inline=True), 			embed_fours.add_field(name="► Beds Lost", value=fours["beds_lost"], inline=True)
			embed_fours.add_field(name="► Finals Kills", value=fours["final_kills"], inline=True),			embed_fours.add_field(name="► Final Deaths", value=fours["final_deaths"], inline=True)	
			embed_fours.add_field(name="► K/D Ratio", value=fours["k_d"], inline=True),						embed_fours.add_field(name="► W/L ratio", value=fours["w_l"], inline=True)	
			embed_fours.add_field(name="► Bed ratio", value=fours["bed_ratio"], inline=True),				embed_fours.add_field(name="► Final K/D Ratio", value=fours["final_k_d"], inline=True)	
			embed_fours.set_footer(text=f"{PREFIX}skywars <username>")
   
			embed_dfours=discord.Embed(title=f"```Bedwars four v four stats | {IGN}```",timestamp=ctx.message.created_at,color=0x2ecc71)
			embed_dfours.set_thumbnail(url="https://media.discordapp.net/attachments/968864446418145330/968948529479417906/unknown.png")
			embed_dfours.add_field(name="► Games Played", value=dfours["games_played"], inline=True),     	embed_dfours.add_field(name="► Winstreak", value=dfours["winstreak"], inline=True)
			embed_dfours.add_field(name="► Losses", value=dfours["losses"], inline=True),     				embed_dfours.add_field(name="► Wins", value=dfours["wins"], inline=True)
			embed_dfours.add_field(name="► Kills", value=dfours["kills"], inline=True),     				embed_dfours.add_field(name="► Deaths", value=dfours["deaths"], inline=True)
			embed_dfours.add_field(name="► Beds broken", value=dfours["beds_broken"], inline=True), 		embed_dfours.add_field(name="► Beds Lost", value=dfours["beds_lost"], inline=True)
			embed_dfours.add_field(name="► Finals Kills", value=dfours["final_kills"], inline=True),		embed_dfours.add_field(name="► Final Deaths", value=dfours["final_deaths"], inline=True)	
			embed_dfours.add_field(name="► K/D Ratio", value=dfours["k_d"], inline=True),					embed_dfours.add_field(name="► W/L ratio", value=dfours["w_l"], inline=True)	
			embed_dfours.add_field(name="► Bed ratio", value=dfours["bed_ratio"], inline=True),				embed_dfours.add_field(name="► Final K/D Ratio", value=dfours["final_k_d"], inline=True)	
			embed_dfours.set_footer(text=f"{PREFIX}skywars <username>")

		except Exception:
			embed=discord.Embed(title="Support Server", description="**An error has occured.**", color=0xff0000,timestamp=ctx.message.created_at,url="https://discord.gg/PrEaXE2dTf")
			embed.set_thumbnail(url="https://gitlab.com/uploads/-/system/project/avatar/32481293/b07b8c25f6b12f217f411b2251617c1f.png")
			embed.add_field(name="Please report this bug in the Support server!", value="Note: This error might be caused by the API.", inline=False)
			embed.set_footer(text="[To report bugs create a ticket in the support server] ")
			await msg.edit(embed=embed)
			print(traceback.print_exc())

def setup(bot):
	bot.add_cog(bedwars(bot))