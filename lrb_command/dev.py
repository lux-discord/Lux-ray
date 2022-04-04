from disnake.ext.commands.core import command, is_owner
from disnake.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded
from core.cog import GeneralCog

@is_owner()
class Dev(GeneralCog):
	@command()
	async def reload(self, ctx, *cog_names):
		for cog_name in cog_names:
			self.bot.reload_extension(cog_name)
		
		await self.send_info(ctx, "Successfully reloaded {cog_names}", cog_names=", ".join(cog_names))

def setup(bot):
	bot.add_cog(Dev(bot))
