import json

import discord
from discord.ext import commands

from inited_cog import Inited_cog
from tools import load_lang
from tools.server_setting import request_server_setting, overwrite_server_setting

@commands.has_permissions(administrator = True)
class Server_Config(Inited_cog):
	@commands.command()
	async def set_lang(self, ctx, lang):
		guild_id = ctx.guild.id
		
		with open('lang/lang_list.json', 'r', encoding = 'UTF-8') as lang_list:
			if lang not in json.load(lang_list):
				await ctx.send(load_lang(guild_id)["error"]["lang_not_found"].format(lang = lang))
				return
		
		server_lang = request_server_setting(guild_id, 'lang')
		
		if lang != server_lang:
			overwrite_server_setting(guild_id, 'lang', lang)
			await ctx.send(load_lang(guild_id)['action']['set_lang'].format(lang = lang))
		else:
			await ctx.send(lang["info"]["lang_not_change"])
	
	@commands.command()
	async def set_prefix(self, ctx, prefix):
		guild_id = ctx.guild.id
		server_prefix = request_server_setting(guild_id, 'prefix')
		action_set_prefix, prefix_not_change = load_lang(guild_id, 'action.set_prefix', 'info.prefix_not_change')
		
		if server_prefix != prefix:
			if not self.bot.indev:
				overwrite_server_setting(guild_id, 'prefix', prefix)
			else:
				overwrite_server_setting(guild_id, 'prefix_dev', prefix)
			await ctx.send(action_set_prefix.format(prefix = prefix))
		else:
			await ctx.send(prefix_not_change)

def setup(bot):
	bot.add_cog(Server_Config(bot))