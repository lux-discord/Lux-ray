from discord.ext.commands import command, has_guild_permissions, has_permissions
from discord.permissions import PermissionOverwrite

from tools.load import load_lang
from tools.setting import ExtServerSetting
from tools.token import Token
from global_object import Inited_cog

class ExclCatServerSetting(ExtServerSetting):
	def __init__(self, id):
		super().__init__(id, __file__)

def make_private_channel_overwrites(ctx):
	private_channel_overwrites = {
		ctx.message.author: PermissionOverwrite(view_channel = True, manage_channels = True, send_messages = True, manage_messages = True),
		ctx.guild.default_role: PermissionOverwrite(view_channel = False)
	}
	
	return private_channel_overwrites

class EexclusiveCategory(Inited_cog):
	@command()
	@has_guild_permissions(administrator = True)
	async def register_excl_cat(self, ctx, user_id, cat_id):
		server_id = ctx.guild.id
		server_setting = ExclCatServerSetting(server_id)
		settings = {
			Token(user_id): {
				"category": {
					"id": cat_id,
					"channel": {channel.id: None for channel in self.bot.get_channel(cat_id).channels}
				}
			}
		}
		server_setting.edit(settings, allow_add_key = True)
	
	@command(aliases = ["create_private_ch", "create_priv_channel", "create_priv_ch"])
	@has_permissions(manage_channels = True)
	async def create_private_channel(self, ctx, name):
		await ctx.message.delete()
		category = ctx.channel.category
		overwrites = {
			ctx.message.author: PermissionOverwrite(view_channel = True, manage_channels = True, send_messages = True, manage_messages = True),
			ctx.guild.default_role: PermissionOverwrite(view_channel = False)
		}
		
		if category:
			info_Channel_Create_private_channel: str = ExclCatServerSetting(ctx.guild.id).request_lang("info.channel.create_private_channel")
			channel = await category.create_text_channel(name, overwrites = make_private_channel_overwrites(ctx))
			
			await ctx.send(info_Channel_Create_private_channel.format(channel_name = channel.name), delete_after = 3)
	
	@command()
	@has_permissions(manage_channels = True)
	async def public_private_channel(self, ctx):
		await ctx.message.delete()
		channel = ctx.channel
		category = channel.category
		
		if category:
			info_Channel_Public_private_channel: str = ExclCatServerSetting(ctx.guild.id).request_lang("info.channel.public_private_channel")
			
			await channel.edit(sync_permissions = True)
			await ctx.send(info_Channel_Public_private_channel)
	
	@command()
	@has_permissions(manage_channels = True)
	async def make_private_channel(self, ctx):
		await ctx.message.delete()
		channel = ctx.channel
		category = channel.category
		
		if category:
			info_Channel_Make_private_channel: str = ExclCatServerSetting(ctx.guild.id).request_lang("info.channel.make_private_channel")
			
			await channel.edit(overwrites = make_private_channel_overwrites(ctx))
			await ctx.send(info_Channel_Make_private_channel)

def setup(bot):
	bot.add_cog(EexclusiveCategory(bot))
