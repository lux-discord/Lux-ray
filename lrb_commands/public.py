import json
import time

from basic_import import *
from basic_cmd_import import *

class Public(Inited_cog):
	@commands.command()
	async def member_num(self, ctx):
		await ctx.send(load_lang(ctx.guild.id)["info"]["member_num"].format(member_num = ctx.guild.member_count))
	
	@commands.command()
	@commands.has_permissions(administrator = True)
	async def test(self, ctx):
		webhooks = await ctx.guild.webhooks()
		
		await ctx.send(webhooks[1].url)

def setup(bot):
	bot.add_cog(Public(bot))
