from disnake.ext.commands.core import command, is_owner
from core.cog import GeneralCog


class Dev(GeneralCog):
	@command()
	@is_owner()
	async def reload(self, ctx, *cog_names):
		if not cog_names:
			return await self.send_error(ctx, "At least one cog name must be entered")
		
		for cog_name in cog_names:
			self.bot.reload_extension("lrb_command."+cog_name)
		
		await self.send_info(ctx, "Successfully reloaded {cog_names}", cog_names=", ".join(cog_names))
	
	@command()
	@is_owner()
	async def load(self, ctx, *cog_names):
		if not cog_names:
			return await self.send_error(ctx, "At least one cog name must be entered")
		
		for cog_name in cog_names:
			self.bot.load_extension("lrb_command."+cog_name)
		
		await self.send_info(ctx, "Successfully loaded {cog_names}", cog_names=", ".join(cog_names))
	
	@command()
	@is_owner()
	async def unload(self, ctx, *cog_names):
		if not cog_names:
			return await self.send_error(ctx, "At least one cog name must be entered")
		
		for cog_name in cog_names:
			self.bot.unload_extension("lrb_command."+cog_name)
		
		await self.send_info(ctx, "Successfully unloaded {cog_names}", cog_names=", ".join(cog_names))
	
	@command()
	@is_owner()
	async def reload_all(self, ctx):
		cogs = dict(self.bot.cogs).copy().values()
		
		for cog in cogs:
			if cog.__module__.startswith("lrb_command"):
				self.bot.reload_extension(cog.__module__)
		
		return await self.send_info(ctx, "Successfully reloaded all cogs")
	
	async def test(self, ctx, *args):
		for cog in self.bot.cogs.values():
			await ctx.send(f"`{cog.__module__}`")
			break

def setup(bot):
	bot.add_cog(Dev(bot))
