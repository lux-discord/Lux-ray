from discord.ext.commands import Cog

from global_object import Inited_cog

from tools.load import load_lang

class Error(Inited_cog):
	@Cog.listener()
	async def on_command_error(self, ctx, error):
		command = ctx.command
		
		if not command:
			await ctx.send(error)
		
		if ctx.command.has_error_handler():
			return
		
		await ctx.send(error)

def setup(bot):
	bot.add_cog(Error(bot))
