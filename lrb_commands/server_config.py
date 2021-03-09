import json

from basic_import import *
from basic_cmd_import import *

from tools.server_setting import server_setting

@commands.has_permissions(administrator = True)
class Server_Config(Inited_cog):
	@commands.command()
	async def config(self, ctx, option_name = 'all'):
		if ctx.author.permissions_in(ctx.channel).administrator:
			with open('setting/setting_global.json', 'r', encoding = 'UTF-8') as config_file:
				config_data = config_file.readlines()
				config_data = config_data[3:-1]
				line_list = []
				option_list = []
				for line in config_data:
					config_option = line.split(':', 1)[0].strip()[1:-1]
					line = line.strip()
					if line[-1] == ',':
						line = line[:-1]
					
					line_list.append(line)
					option_list.append(config_option)
				
				option_dic = dict(zip(option_list, line_list))
			
			if option_name == 'all':
				string = ''
				for line in config_data:
					string = string + line[1:]
				await ctx.send(string)
			elif option_name in option_list:
				await ctx.send(option_dic[option_name])
			else:
				await ctx.send(lang['error']['option_not_found'].format(option_name = f'"{option_name}"'))
		else:
			await ctx.send(lang["error"]["permission_too_low_server_admin"])
	
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
		
		server_setting_data = server_setting(guild_id)
		
		if lang != server_setting_data['lang']:
			server_setting_data['lang'] = lang
			
			with open(f'settings/server/{guild_id}.json', 'w', encoding = 'UTF-8') as server_setting_file:
				json.dump(server_setting_data, server_setting_file, indent = '\t')
			
			await ctx.send(load_lang(guild_id)['action']['set_lang'].format(lang = lang))
		else:
			await ctx.send(lang["info"]["lang_not_change"])
	
	@commands.command()
	async def set_prefix(self, ctx, prefix):
		if ctx.author.permissions_in(ctx.channel).administrator:
			setting['prefix'] = prefix
			with open(f'setting/setting_global.json', 'w', encoding = 'UTF-8') as setting_file:
				json.dump(setting, setting_file, indent = '\t')
			
			await ctx.send(lang["status"]["set_prefix"].format(prefix = f'"{prefix}"'))
		else:
			await ctx.send(lang["error"]["permission_too_low_server_admin"])
	
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