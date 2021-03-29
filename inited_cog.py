import discord
from discord.ext import commands

class Inited_cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
