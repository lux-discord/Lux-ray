from core import InitedCog, Server
from discord.ext.commands import Cog

class Error(InitedCog):
	@Cog.listener()
	async def on_command_error(self, ctx, error):
		# command not exist
		if not ctx.command:
			return await Server(ctx).send_error("error.invalid_command.command_not_exist", command_name=ctx.invoked_with)
		
		if ctx.command.has_error_handler():
			return
		
		await ctx.send(error)

def setup(bot):
	bot.add_cog(Error(bot))
