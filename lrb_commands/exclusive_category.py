import discord
from discord import PermissionOverwrite
from discord.ext import commands

from inited_cog import Inited_cog
from tools.server_setting import request_server_setting

def guild_able_excl_cat():
	def check_config(ctx):
		return request_server_setting(ctx.guild.id, 'config.excl_cat')
	
	return commands.check(check_config)

@guild_able_excl_cat()
class Exclusive_Category(Inited_cog):
	@commands.command()
	async def request_excl_cat(self, ctx):
		guild = ctx.guild
		server_setting_data = server_setting(guild.id)
		excl_cat_role = server_setting_data['excl_cat_role']
		overwrite = {
			guild.default_role: PermissionOverwrite(send_message = False),
			guild.get_role(excl_cat_role): PermissionOverwrite(read_message = True),
			ctx.author: PermissionOverwrite(send_message = True, manage_channels = True)
		}
		
		if server_setting_data['basic_role'] is not None:
			overwrite[guild.default_role] = PermissionOverwrite(read_message = False)
		
		await ctx.guild.create_category(ctx.author.display_name, overwrite = overwrite)

def setup(bot):
	bot.add_cog(Exclusive_Category(bot))
