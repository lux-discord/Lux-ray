from discord.ext.commands import command

from global_object import Inited_cog

class Test(Inited_cog):
	@command()
	async def test(self, ctx):
		pass

def setup(bot):
	bot.add_cog(Test(bot))
