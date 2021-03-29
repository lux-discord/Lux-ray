import discord
from discord.ext import commands

from inited_cog import Inited_cog

@commands.is_owner()
class Test(Inited_cog):
	@commands.command()
	async def test(self, ctx):
		pass

def setup(bot):
	bot.add_cog(Test(bot))