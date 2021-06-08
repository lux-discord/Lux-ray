from discord.ext.commands import command

from global_object import Inited_cog

class Test(Inited_cog):
	@command()
	async def test(self, ctx):
		await ctx.send(ctx.message.reference.resolved)

def setup(bot):
	bot.add_cog(Test(bot))
