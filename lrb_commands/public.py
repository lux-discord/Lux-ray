import json
import time

import discord
from discord.ext import commands

from inited_cog import Inited_cog
from tools import load_lang

class Public(Inited_cog):
	@commands.command()
	async def member_num(self, ctx):
		await ctx.send(load_lang(ctx.guild.id)["info"]["member_num"].format(member_num = ctx.guild.member_count))

def setup(bot):
	bot.add_cog(Public(bot))
