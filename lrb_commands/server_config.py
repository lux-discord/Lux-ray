import json

from basic_import import *
from basic_cmd_import import *

from tools.server_setting import server_setting

@commands.has_permissions(administrator = True)
class Server_Config(Inited_cog):
	@commands.command()
	async def set_channel(self, ctx, channel_type):
		if ctx.author.permissions_in(ctx.channel).administrator:
			channel_list = ctx.message.channel_mentions
			if len(channel_list) == 0:
				await ctx.send(lang['error']['no_channel_mentioned'])
			elif len(channel_list) == 1:
				if channel_type == 'member_join':
					setting['channel']['member_join_message_channel'] = channel_list[0].id
				elif channel_type == 'member_leave':
					setting['channel']['member_leave_message_channel'] = channel_list[0].id
				
				with open('setting/setting_global.json', 'w', encoding = 'UTF-8') as setting_file:
					json.dump(setting, setting_file, indent = '\t')
				
				await ctx.send(lang['status']['channel_set'].format(channel_name = channel_list[0].mention, channel_type = lang['channel_type'][channel_type]))
			else:
				await ctx.send(lang['error']['too_many_channel_mentions'])
		else:
			await ctx.send(lang["error"]["permission_too_low_server_admin"])
	
	@commands.command()
	async def set_lang(self, ctx, lang):
		guild_id = ctx.guild.id
		
		with open('lang/lang_list.json', 'r', encoding = 'UTF-8') as lang_list:
			if lang not in json.load(lang_list):
				await ctx.send(load_lang(guild_id)["error"]["lang_not_found"].format(lang = lang))
				return
		
		server_lang = server_setting(guild_id, 'lang')
		
		if lang != server_lang:
			server_setting(guild_id, 'lang', lang)
			await ctx.send(load_lang(guild_id)['action']['set_lang'].format(lang = lang))
		else:
			await ctx.send(lang["info"]["lang_not_change"])
	
	@commands.command()
	async def set_prefix(self, ctx, prefix):
		guild_id = ctx.guild.id
		server_prefix = server_setting(guild_id, 'prefix')
		action_set_prefix, prefix_not_change = load_lang(guild_id, 'action.set_prefix', 'info.prefix_not_change')
		
		if server_prefix != prefix:
			if not self.bot.indev:
				server_setting(guild_id, 'prefix', prefix)
			else:
				server_setting(guild_id, 'prefix_dev', prefix)
			await ctx.send(action_set_prefix.format(prefix = prefix))
		else:
			await ctx.send(prefix_not_change)
	
	@commands.command()
	async def switch(self, ctx, switch_type: str, switch_value):
		if ctx.author.permissions_in(ctx.channel).administrator:
			value_list = ['on', 'off', 'true', 'false', 'switch']
			if str.lower(switch_value) in value_list:
				pass
			else:
				await ctx.send(lang['error']['invalid_value'].format(''))
		else:
			await ctx.send(lang["error"]["permission_too_low_server_admin"])
		
def setup(bot):
	bot.add_cog(Server_Config(bot))