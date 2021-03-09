import discord
from discord.ext import commands
from core.classes import Inited_cog
from lrb_commands.manage_messages import Manage_messages

class Errors(Inited_cog):
	@Manage_messages.pin.error
	async def pin_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(lang['error']['missing_permissions'].format(permission_name = lang['permission']['manage_messages']))
	
	@Manage_messages.unpin.error
	async def unpin_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(lang['error']['missing_permissions'].format(permission_name = lang['permission']['manage_messages']))
	