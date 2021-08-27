from core import InitedCog, Server
from discord.ext.commands.core import command, is_owner
from discord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded


@is_owner()
class Dev(InitedCog):
	@command()
	async def reload(self, ctx, cog_name):
		self.bot.reload_extension(cog_name)
		await Server(ctx).send_info("info.extension.reload", cog_name=cog_name)

def setup(bot):
	bot.add_cog(Dev(bot))
