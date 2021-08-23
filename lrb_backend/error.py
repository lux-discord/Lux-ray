from tool.token import Token
from core import InitedCog, Server
from discord.ext.commands import Cog


class Error(InitedCog):
	@Cog.listener()
	async def on_command_error(self, ctx, error):
		# command not exist
		if not ctx.command:
			server = Server(ctx)
			return await ctx.send(server.lang_request(Token("error.invalid_command.command_not_exist")).format(command_name=ctx.invoked_with))
		
		if ctx.command.has_error_handler():
			return
		
		await ctx.send(error)

def setup(bot):
	bot.add_cog(Error(bot))
