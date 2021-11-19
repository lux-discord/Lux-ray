from disnake.ext.commands.core import command, is_owner
from disnake.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded
from utils.cog import InitedCog


@is_owner()
class Dev(InitedCog):
	@command()
	async def reload(self, ctx, cog_name):
		self.bot.reload_extension(cog_name)
		await self.send_info(ctx, "info.extension.reload", cog_name=cog_name)

def setup(bot):
	bot.add_cog(Dev(bot))
