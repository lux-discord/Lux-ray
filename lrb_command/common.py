from re import compile
from discord.ext.commands.core import command

from tools.load import load_lang
from global_object import Inited_cog

class Common(Inited_cog):
	@command()
	async def emoji_link(self, ctx):
		refer_mes = ctx.message.reference
		emoji_regex = compile(r'<a?:.+?:([0-9]{15,21})>')
		
		if refer_mes:
			refer_mes = refer_mes.resolved
		else:
			return await ctx.send(load_lang(ctx.guild.id, "error.no_refernace_message"))
		
		emojis = emoji_regex.findall(refer_mes.content)
		
		if emojis:
			await ctx.send("\n".join({str(self.bot.get_emoji(int(emoji)).url) for emoji in emojis}))
		else:
			await ctx.send(load_lang(ctx.guild.id, "error.no_stickers"))

def setup(bot):
	bot.add_cog(Common(bot))
