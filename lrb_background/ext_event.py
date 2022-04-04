from disnake.ext.commands import Cog
from core.cog import GeneralCog

class ExtEvent(GeneralCog):
	@Cog.listener()
	async def on_command_error(self, ctx, error):
		# command not exist
		if not ctx.command:
			return await self.send_error(ctx, "Command `{name}` not exists", name=ctx.invoked_with)
		
		if ctx.command.has_error_handler():
			return
		
		await ctx.send(error)

def setup(bot):
	bot.add_cog(ExtEvent(bot))
