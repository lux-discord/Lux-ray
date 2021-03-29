import discord
from discord.ext import commands

from inited_cog import Inited_cog

class Task(Inited_cog):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
	
	async def morning():
		pass

def setup(bot):
	bot.add_cog(Task(bot))
