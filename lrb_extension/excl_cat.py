from discord.ext.commands import command, has_guild_permissions

from tools.setting import ExtServerSetting
from global_object import Inited_cog

class ExclCatServerSetting(ExtServerSetting):
	def __init__(self, id):
		"""Excl cat's server setting class"""
		super().__init__(id, __file__)

class EexclusiveCategory(Inited_cog):
	@command()
	async def request_excl_cat(self, ctx):
		pass
	
	@command()
	@has_guild_permissions(administrator = True)
	async def regist_excl_cat(self, ctx, user_id, cat_id):
		server_id = ctx.guild.id
		server_setting = ExclCatServerSetting(server_id)
		settings = {
			user_id: {
				"category": cat_id
			}
		}
		server_setting.edit(settings, True)
	
	@command()
	async def edit_excl_cat(self, ctx):
		pass
	
	@command()
	async def edit_excl_channel(self, ctx):
		pass
	
	@command()
	async def rename_excl_cat(self, ctx):
		pass
	
	@command()
	async def rename_excl_channel(self, ctx):
		pass
	
	@command()
	async def delete_excl_cat(self, ctx):
		pass
	
	@command()
	async def backup_excl_cat(self, ctx):
		pass
	
	@command()
	async def backup_excl_channel(self, ctx):
		pass

def setup(bot):
	bot.add_cog(EexclusiveCategory(bot))
