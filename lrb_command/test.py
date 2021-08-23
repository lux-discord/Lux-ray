from core import InitedCog
from discord.ext.commands.core import command


class Test(InitedCog):
	@command()
	async def test(self, ctx):
		t = await ctx.channel.fetch_message(879400364498108417)
		await ctx.send(t)

def setup(bot):
	bot.add_cog(Test(bot))
879400364498108417
879401671757819934
